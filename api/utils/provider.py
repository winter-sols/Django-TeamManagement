import pandas as pd
from datetime import date, timedelta
from django.db.models import Sum, Q

from finance.models import Project, FinancialRequest, Transaction
from finance import constants as cs
from user.constants import ROLE_ADMIN, ROLE_TEAM_MANAGER, ROLE_DEVELOPER
from api.common.finance.serializers import (
    FinancialRequestDetailSerializer
)
from api.common.report.constants import PERIOD_CUSTOM, REVIEW_WEEKDAY


def get_review_end_date_of_month(month_last_dt):
    last_dt_weekday = month_last_dt.weekday()
    if last_dt_weekday >= REVIEW_WEEKDAY:
        return month_last_dt - timedelta(days=last_dt_weekday) + timedelta(days=REVIEW_WEEKDAY)
    else:
        return month_last_dt - timedelta(days=last_dt_weekday + (7 - REVIEW_WEEKDAY))


def get_review_start_date_of_month(month_first_dt):
    first_dt_weekday = month_first_dt.weekday()
    if first_dt_weekday >= REVIEW_WEEKDAY + 1:
        return month_first_dt - timedelta(days=first_dt_weekday) + timedelta(days=REVIEW_WEEKDAY+1)
    else:
        return month_first_dt - timedelta(days=first_dt_weekday + (6 - REVIEW_WEEKDAY))


def get_dates_from_period(period):
    if period == 'this-month':
        first_day_of_this_month = (date.today() - pd.tseries.offsets.MonthEnd(1)).date() + timedelta(days=1)
        last_day_of_this_month = (date.today() + pd.tseries.offsets.MonthEnd(0)).date()
        start_date = get_review_start_date_of_month(first_day_of_this_month)
        end_date = get_review_end_date_of_month(last_day_of_this_month)
    elif period == 'this-quarter':
        first_day_of_this_quarter = (date.today() - pd.tseries.offsets.QuarterEnd(1)).date() + timedelta(days=1)
        last_day_of_this_quarter = (date.today() + pd.tseries.offsets.QuarterEnd(0)).date()
        start_date = get_review_start_date_of_month(first_day_of_this_quarter)
        end_date = get_review_end_date_of_month(last_day_of_this_quarter)
    elif period == 'this-week':
        today = date.today()
        week_of_today = today.weekday()
        start_date = today - timedelta(days=week_of_today)
        end_date = today + timedelta(days=6-week_of_today)
    else: return None
    return { 'start_date': start_date, 'end_date': end_date }


def get_ongoing_projects(viewer, team, user):
    if viewer.is_anonymous:
        queryset = user.projects.none()
    elif viewer.is_admin:
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


def get_pending_financial_requests(viewer, team, user):
    if viewer.is_anonymous:
        queryset = FinancialRequest.objects.none()
    elif viewer.is_admin:
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


def get_weekly_income(viewer, team, user, period):
    dates = get_dates_from_period(period)
    start_date = dates.get('start_date')
    end_date = dates.get('end_date')
    return get_incomes_of_period(viewer, team, user, start_date, end_date)


def get_expectations(viewer,team, user, period):
    """
    calculate incomes of this month expectation
    """
    dates = get_dates_from_period(period)
    start_date = dates.get('start_date')
    end_date = dates.get('end_date')
    return get_incomes_of_period(viewer, team, user, start_date, end_date).sum()


def get_queryset_with_developer_earnings(queryset, query_params):
    period = query_params.get('period')

    if period is not None and period != PERIOD_CUSTOM:
        dates = get_dates_from_period(period)
        start_date = dates.get('start_date')
        end_date = dates.get('end_date')
    else:
        start_date = query_params.get('from')
        end_date = query_params.get('to')

    return queryset.annotate(
        total=Sum('financialrequest__transaction__net_amount',
        filter=Q(
            financialrequest__transaction__created_at__gte=start_date,
            financialrequest__transaction__created_at__lte=end_date,
            financialrequest__type__in=[
                cs.FINANCIAL_TYPE_RCV_PAYMENT,
                cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                cs.FINANCIAL_TYPE_SND_PAYMENT
            ]
        )))


def get_queryset_with_team_earnings(queryset, query_params):
    period = query_params.get('period')

    if period is not None and period != PERIOD_CUSTOM:
        dates = get_dates_from_period(period)
        start_date = dates.get('start_date')
        end_date = dates.get('end_date')
    else:
        start_date = query_params.get('from')
        end_date = query_params.get('to')

    return queryset.annotate(
        total=Sum('user__financialrequest__transaction__net_amount',
        filter=Q(
            user__financialrequest__transaction__created_at__gte=start_date,
            user__financialrequest__transaction__created_at__lte=end_date,
            user__financialrequest__type__in=[
                cs.FINANCIAL_TYPE_RCV_PAYMENT,
                cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                cs.FINANCIAL_TYPE_SND_PAYMENT
            ]
        )))
    

def get_earnings(viewer, period=None, team=None, user=None, start_date=None, end_date=None):
    """
    calculate current earning of month as a developer or team-manger or developer
    """
    if period is not None and period!= PERIOD_CUSTOM:
        dates = get_dates_from_period(period)
        start_date = dates.get('start_date')
        end_date = dates.get('end_date')
        
    if viewer.is_anonymous:
        sum = 0
    elif viewer.is_admin:
        if user is not None:
            sum = Transaction.objects \
                .filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date,
                    financial_request__requester=user,
                    financial_request__type__in=[
                        cs.FINANCIAL_TYPE_RCV_PAYMENT,
                        cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                        cs.FINANCIAL_TYPE_SND_PAYMENT
                    ]
                ) \
                .aggregate(Sum('net_amount'))
        elif team is not None:
            sum = Transaction.objects \
                .filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date,
                    financial_request__requester__team=team,
                    financial_request__type__in=[
                        cs.FINANCIAL_TYPE_RCV_PAYMENT,
                        cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                        cs.FINANCIAL_TYPE_SND_PAYMENT
                    ]
                ) \
                .aggregate(Sum('net_amount'))
        else:
            sum = Transaction.objects \
                .filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date,
                    financial_request__type__in=[
                        cs.FINANCIAL_TYPE_RCV_PAYMENT,
                        cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                        cs.FINANCIAL_TYPE_SND_PAYMENT
                    ]
                ) \
                .aggregate(Sum('net_amount'))
    elif viewer.is_team_manager:
        if user is not None:
            sum = Transaction.objects \
                .filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date,
                    financial_request__requester=user,
                    financial_request__type__in=[
                        cs.FINANCIAL_TYPE_RCV_PAYMENT,
                        cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                        cs.FINANCIAL_TYPE_SND_PAYMENT
                    ]
                ) \
                .aggregate(Sum('net_amount'))
        else:
            sum = Transaction.objects \
                .filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date,
                    financial_request__requester__team=viewer.team,
                    financial_request__type__in=[
                        cs.FINANCIAL_TYPE_RCV_PAYMENT,
                        cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                        cs.FINANCIAL_TYPE_SND_PAYMENT
                    ]
                ) \
                .aggregate(Sum('net_amount'))
    else:
        sum = Transaction.objects \
            .filter(
                created_at__gte=start_date,
                created_at__lte=end_date,
                financial_request__requester=viewer,
                financial_request__type__in=[
                    cs.FINANCIAL_TYPE_RCV_PAYMENT,
                    cs.FINANCIAL_TYPE_REFUND_PAYMENT,
                    cs.FINANCIAL_TYPE_SND_PAYMENT
                ]
            ) \
            .aggregate(Sum('net_amount'))
    return sum['net_amount__sum'] or 0


def get_approved_financial_requests(viewer, team, user):
    """
    report approved financial requests
    """
    if viewer.is_anonymous:
        queryset = FinancialRequest.objects.none()
    elif viewer.is_admin:
        if user is not None:
            queryset = user.financialrequest_set.approved_requests()
        elif team is not None:
            queryset = FinancialRequest.objects.approved_requests().filter(
                requester__in=team.user_set.all()
            )
        else:
            queryset = FinancialRequest.objects.approved_requests()
    elif viewer.is_team_manager:
        if user is not None:
            queryset = user.financialrequest_set.approved_requests()
        else:
            queryset = FinancialRequest.objects.approved_requests().filter(
                requester__in=viewer.team_members
            )
    else:
        queryset = viewer.financialrequest_set.approved_requests()
    return queryset


def get_user_project_earnings(user, period=None, start_date=None, end_date=None):
    """
    calculate current earning of developer by projects
    """
    if start_date is None and end_date is None:
        dates = get_dates_from_period(period)
        start_date = dates.get('start_date')
        end_date = dates.get('end_date')

    my_projects = Project.objects.filter(project_starter=user)
    project_count = my_projects.count()
    project_earning = list(range(project_count))

    for index in range(project_count):
        project = my_projects[index]
        sum = Transaction.objects \
            .filter(
                created_at__gte=start_date,
                created_at__lte=end_date,
                financial_request__project=project,
                financial_request__requester=user,
                financial_request__type__in=[
                    cs.FINANCIAL_TYPE_RCV_PAYMENT,
                    cs.FINANCIAL_TYPE_REFUND_PAYMENT
                ]
            ) \
            .aggregate(Sum('net_amount'))
        project_earning[index] = {
            'id': project.id,
            'project_title': project.title,
            'earning': sum['net_amount__sum'] or 0
        }

    return project_earning

def get_queryset_with_project_earnings(viewer, queryset, query_params):
    period = query_params.get('period')

    if period is not None and period != PERIOD_CUSTOM:
        dates = get_dates_from_period(period)
        start_date = dates.get('start_date')
        end_date = dates.get('end_date')
    else:
        start_date = query_params.get('from')
        end_date = query_params.get('to')
    return queryset.annotate(
        earning=Sum('financialrequest__transaction__net_amount',
        filter=Q(
            financialrequest__transaction__created_at__gte=start_date,
            financialrequest__transaction__created_at__lte=end_date,
            financialrequest__type__in=[
                cs.FINANCIAL_TYPE_RCV_PAYMENT,
                cs.FINANCIAL_TYPE_REFUND_PAYMENT
            ]
        )))
