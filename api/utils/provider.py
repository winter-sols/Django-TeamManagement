import pandas as pd
from datetime import date, timedelta
from django.db.models import Sum
from finance.models import Project, FinancialRequest, Transaction
from finance import constants as cs
from user.constants import ROLE_ADMIN, ROLE_TEAM_MANAGER, ROLE_DEVELOPER
from api.common.finance.serializers import (
    FinancialRequestDetailSerializer
)


def get_ongoing_projects(viewer, team, user):
    if viewer.is_admin:
        if user is not None:
            queryset = user.projects.ongoing_projects()
        elif team is not None:
            queryset = Project.objects.ongoing_projects().filter(participants__in=team.user_set.all())
        else:
            queryset = Project.objects.ongoing_projects()
    elif viewer.is_team_manager:
        if user is not None:
            queryset = user.projects.ongoing_projects()
        else:
            queryset = Project.objects.ongoing_projects().filter(participants__in=viewer.team_members)
    else:
        queryset = viewer.projects.ongoing_projects()
    return queryset

def get_incomes_of_period(viewer, team, user, start, end ):
    """
    calculate incomes of given period according to start and end date
    """
    queryset = get_ongoing_projects(viewer, team, user)
    period_index = pd.date_range(start, end)
    income_series = pd.Series(0, index=period_index)
    for item in queryset:
        start_date = max(start, item.started_at)
        end_date = min(end, item.ended_at) if item.ended_at is not None else end
        if item.type == cs.PROJECT_TYPE_BUDGET:
            if item.ended_at <= end and item.ended_at >= start:
                start_date = item.ended_at
            else:
                continue
            proj_date_index = pd.date_range(start_date, end_date)
            working_hours_series = pd.Series(1, index=proj_date_index)     
        else:
            proj_date_index = pd.bdate_range(start_date, end_date, freq='B')
            working_hours_series = pd.Series((item.weekly_limit or 0) / 5, index=proj_date_index) 
            
        working_rate_series = pd.Series(item.price, index=proj_date_index)
        income_series = income_series.add(working_hours_series * working_rate_series, fill_value=0)
    return income_series

def get_weekly_income(viewer, team, user):
    today = date.today()
    week_of_today = today.weekday()
    w_start_date = today - timedelta(days=week_of_today)
    w_end_date = today + timedelta(days=6-week_of_today)
    return get_incomes_of_period(viewer, team, user, w_start_date, w_end_date)


def get_pending_financial_requests(viewer, team, user):
    if viewer.is_admin:
        if user is not None:
            queryset = user.financialrequest_set.pending_requests()
        elif team is not None:
            queryset = FinancialRequest.objects.pending_requests().filter(requester__in=team.user_set.all())
        else:
            queryset = FinancialRequest.objects.pending_requests()
    elif viewer.is_team_manager:
        if user is not None:
            queryset = user.financialrequest_set.pending_requests()
        else:
            queryset = FinancialRequest.objects.pending_requests().filter(requester__in=viewer.team_members)
    else:
        queryset = viewer.financialrequest_set.pending_requests()
    return queryset


def get_last_wednesday_of_month(month):
    week_of_month = month.weekday()
    return month - timedelta(days=week_of_month) + timedelta(days=2)

def get_this_month_expectation(viewer, team, user):
    """
    calculate incomes of this month expectation
    """
    last_month = (date.today() - pd.tseries.offsets.BMonthEnd(1)).date()
    start_date = get_last_wednesday_of_month(last_month) - timedelta(days=9)
    this_month = (date.today() + pd.tseries.offsets.BMonthEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_month) - timedelta(days=10)
    return get_incomes_of_period(viewer, team, user, start_date, end_date).sum()

def get_this_month_earning(viewer, team=None, user=None):
    """
    calculate current earning of month as a developer or team-manger or developer
    """
    start_date = (date.today() - pd.tseries.offsets.MonthEnd(1)).date() + timedelta(days=1)
    end_date = this_month = (date.today() + pd.tseries.offsets.BMonthEnd(0)).date()

    if viewer.is_admin:
        if user is not None:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date,financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
        elif team is not None:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester__team=team, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
        else:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    elif viewer.is_team_manager:
        if user is not None:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date,financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
        else:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester__team=viewer.team, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    else:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester=viewer, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    return sum['net_amount__sum'] or 0


def get_this_quarter_expectation(viewer, team, user):
    """
    expect this quater incomes
    """
    prev_quarter_end = (date.today() - pd.tseries.offsets.BQuarterEnd(1)).date()
    start_date = get_last_wednesday_of_month(prev_quarter_end) - timedelta(days=9)

    this_quarter_end = (date.today() + pd.tseries.offsets.BQuarterEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_quarter_end) - timedelta(days=10)

    return get_incomes_of_period(viewer, team, user, start_date, end_date).sum()


def get_this_quarter_earning(viewer, team=None, user=None):
    """
    calculate current earning of this quarter
    """
    prev_quarter_end = (date.today() - pd.tseries.offsets.BQuarterEnd(1)).date()
    start_date = prev_quarter_end + timedelta(days=1)
    end_date = (date.today() + pd.tseries.offsets.BQuarterEnd(0)).date()

    if viewer.is_admin:
        if user is not None:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date,financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
        elif team is not None:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester__team=team, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
        else:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    elif viewer.is_team_manager:
        if user is not None:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date,financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
        else:
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester__team=viewer.team, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    else:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester=viewer, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    return sum['net_amount__sum'] or 0


def get_approved_financial_requests(viewer, team, user):
    """
    report approved financial requests
    """
    if viewer.is_admin:
        if user is not None:
            queryset = user.financialrequest_set.approved_requests()
        elif team is not None:
            queryset = FinancialRequest.objects.approved_requests().filter(requester__in=team.user_set.all())
        else:
            queryset = FinancialRequest.objects.approved_requests()
    elif viewer.is_team_manager:
        if user is not None:
            queryset = user.financialrequest_set.approved_requests()
        else:
            queryset = FinancialRequest.objects.approved_requests().filter(requester__in=viewer.team_members)
    else:
        queryset = viewer.financialrequest_set.approved_requests()
    return queryset


def get_this_week_earning(user, user_role):
    today = date.today()
    week_of_today = today.weekday()
    start_date = today - timedelta(days=week_of_today)
    end_date = today + timedelta(days=6-week_of_today)
    if user_role == ROLE_DEVELOPER:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    elif user_role == ROLE_TEAM_MANAGER:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester__team=user.team, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    elif user_role == ROLE_ADMIN:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    return sum['net_amount__sum'] or 0

def get_this_month_project_earning(user):
    """
    calculate current earning of developer by projects
    """
    start_date = (date.today() - pd.tseries.offsets.MonthEnd(1)).date() + timedelta(days=1)
    end_date = this_month = (date.today() + pd.tseries.offsets.BMonthEnd(0)).date()

    my_projects = Project.objects.filter(project_starter=user)
    project_count = my_projects.count()
    project_earning = list(range(project_count))

    for index in range(project_count):
        project = my_projects[index]
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__project=project, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
        project_earning[index] = {
            'id': project.id,
            'project_title': project.title,
            'earning': sum['net_amount__sum'] or 0
        }

    return project_earning

def get_this_quarter_project_earning(user):
    """
    calculate current earning of this quarter
    """
    
    prev_quarter_end = (date.today() - pd.tseries.offsets.BQuarterEnd(1)).date()
    start_date = prev_quarter_end + timedelta(days=1)
    end_date = (date.today() + pd.tseries.offsets.BQuarterEnd(0)).date()

    my_projects = Project.objects.filter(project_starter=user)
    project_count = my_projects.count()
    project_earning = list(range(project_count))

    for index in range(project_count):
        project = my_projects[index]
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__project=project, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
        project_earning[index] = {
            'id': project.id,
            'project_title': project.title,
            'earning': sum['net_amount__sum'] or 0
        }

    return project_earning

def get_this_week_project_earning(user):
    today = date.today()
    week_of_today = today.weekday()
    w_start_date = today - timedelta(days=week_of_today)
    w_end_date = today + timedelta(days=6-week_of_today)
    
    my_projects = Project.objects.filter(project_starter=user)
    project_count = my_projects.count()
    project_earning = list(range(project_count))

    for index in range(project_count):
        project = my_projects[index]
        sum = Transaction.objects.filter(created_at__gte=w_start_date, created_at__lte=w_end_date, financial_request__project=project, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
        project_earning[index] = {
            'id': project.id,
            'project_title': project.title,
            'earning': sum['net_amount__sum'] or 0
        }

    return project_earning

def get_this_month_team_project_earning(team_instance):
    """
    calculate this month team earnings of developer by projects
    """
    last_month = (date.today() - pd.tseries.offsets.BMonthEnd(1)).date()
    start_date = get_last_wednesday_of_month(last_month) - timedelta(days=9)
    this_month = (date.today() + pd.tseries.offsets.BMonthEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_month) - timedelta(days=10)
    
    members = team_instance.user_set.all()
    n_members = members.count()
    reports = []
    for idx in range(n_members):
        member = members[idx]
        my_projects = Project.objects.filter(project_starter=member)
        n_projects = my_projects.count()

        for proj_idx in range(n_projects):
            project = my_projects[proj_idx]
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__project=project, financial_request__requester=member, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
            reports.append({
                'full_name':member.first_name + ' ' + member.last_name, 
                'project_title': project.title, 
                'earning': sum['net_amount__sum'] or 0
            })

    return reports

def get_this_quarter_team_project_earning(team_instance):
    """
    calculate this quarter team earnings of developer by projects
    """
    prev_quarter_end = (date.today() - pd.tseries.offsets.BQuarterEnd(1)).date()
    start_date = get_last_wednesday_of_month(prev_quarter_end) - timedelta(days=9)

    this_quarter_end = (date.today() + pd.tseries.offsets.BQuarterEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_quarter_end) - timedelta(days=10)
    
    members = team_instance.user_set.all()
    n_members = members.count()
    reports = []
    for idx in range(n_members):
        member = members[idx]
        my_projects = Project.objects.filter(project_starter=member)
        n_projects = my_projects.count()

        for proj_idx in range(n_projects):
            project = my_projects[proj_idx]
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__project=project, financial_request__requester=member, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
            reports.append({
                'full_name':member.first_name + ' ' + member.last_name, 
                'project_title': project.title, 
                'earning': sum['net_amount__sum'] or 0
            })

    return reports

def get_this_week_team_project_earning(team_instance):
    """
    calculate this week team earnings of developer by projects
    """
    today = date.today()
    week_of_today = today.weekday()
    start_date = today - timedelta(days=week_of_today)
    end_date = today + timedelta(days=6-week_of_today)
    
    members = team_instance.user_set.all()
    n_members = members.count()
    reports = []
    for idx in range(n_members):
        member = members[idx]
        my_projects = Project.objects.filter(project_starter=member)
        n_projects = my_projects.count()

        for proj_idx in range(n_projects):
            project = my_projects[proj_idx]
            sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__project=project, financial_request__requester=member, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
            reports.append({
                'full_name':member.first_name + ' ' + member.last_name, 
                'project_title': project.title, 
                'earning': sum['net_amount__sum'] or 0
            })

    return reports

def get_custom_earning(user,user_role, start_date, end_date):
    """
    returns earning by given period as a developer or team-manager or admin
    """
    if user_role == ROLE_DEVELOPER:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    elif user_role == ROLE_TEAM_MANAGER:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester__team=user.team, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    elif user_role == ROLE_ADMIN:
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT, cs.FINANCIAL_TYPE_SND_PAYMENT]).aggregate(Sum('net_amount'))
    return sum['net_amount__sum'] or 0

def get_custom_project_earning(user, start_date, end_date):
    """
    calculate current earning of developer by projects according to given period
    """
    my_projects = Project.objects.filter(project_starter=user)
    project_count = my_projects.count()
    project_earning = list(range(project_count))

    for index in range(project_count):
        project = my_projects[index]
        sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__project=project, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
        project_earning[index] = {
            'id': project.id,
            'project_title': project.title,
            'earning': sum['net_amount__sum'] or 0
        }

    return project_earning