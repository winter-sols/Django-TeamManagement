import pandas as pd
from datetime import date, timedelta
from django.db.models import Sum
from finance.models import Project, FinancialRequest, Transaction
from finance import constants as cs

def get_ongoing_projects(user):
    if user.is_admin:
        queryset = Project.objects.ongoing_projects()
    elif user.is_team_manager:
        queryset = Project.objects.ongoing_projects().filter(participants__in=user.team.user_set.all())
    elif user.is_developer:
        queryset = user.projects.ongoing_projects()
    return queryset

def get_incomes_of_period(user, start, end):
    """
    calculate incomes of given period according to start and end date
    """
    queryset = get_ongoing_projects(user)
    period_index = pd.date_range(start, end)
    income_series = pd.Series(0, index=period_index)
    for item in queryset:
        start_date = max(start, item.started_at)
        if item.type == cs.PROJECT_TYPE_BUDGET:
            if item.ended_at <= end and item.ended_at >= start:
                start_date = item.ended_at
            else:
                continue
        end_date = min(end, item.ended_at) if item.ended_at is not None else end
        if item.type == cs.PROJECT_TYPE_BUDGET:
            proj_date_index = pd.date_range(start_date, end_date)
        else:
            proj_date_index = pd.bdate_range(start_date, end_date, freq='B')
        if item.type != cs.PROJECT_TYPE_BUDGET:
            working_hours_series = pd.Series((item.weakly_limit or 0) / 5, index=proj_date_index) 
        else:
            working_hours_series = pd.Series(1, index=proj_date_index)     
        working_rate_series = pd.Series(item.price, index=proj_date_index)
        income_series = income_series.add(working_hours_series * working_rate_series, fill_value=0)
    return income_series

def get_weekly_income(user):
    today = date.today()
    week_of_today = today.weekday()
    w_start_date = today - timedelta(days=week_of_today)
    w_end_date = today + timedelta(days=6-week_of_today)
    return get_incomes_of_period(user, w_start_date, w_end_date)

def get_pending_financial_requests(user):
    if user.is_admin:
        return FinancialRequest.objects.pending_requests()
    elif user.is_team_manager:
        return FinancialRequest.objects.pending_requests().filter(requester__in=user.team.user_set.all())
    elif user.is_developer:
        return user.financialrequest_set.pending_requests()

def get_last_wednesday_of_month(month):
    week_of_month = month.weekday()
    return month - timedelta(days=week_of_month) + timedelta(days=2)

def get_this_month_expectation(user):
    """
    calculate incomes of this month expectation
    """
    last_month = (date.today() - pd.tseries.offsets.BMonthEnd(1)).date()
    start_date = get_last_wednesday_of_month(last_month) - timedelta(days=9)
    this_month = (date.today() + pd.tseries.offsets.BMonthEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_month) - timedelta(days=10)
    return get_incomes_of_period(user, start_date, end_date).sum()

def get_this_month_earning(user):
    """
    calculate current earning of developer
    """
    last_month = (date.today() - pd.tseries.offsets.BMonthEnd(1)).date()
    start_date = get_last_wednesday_of_month(last_month) - timedelta(days=9)
    this_month = (date.today() + pd.tseries.offsets.BMonthEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_month) - timedelta(days=10)
    sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
    return sum['net_amount__sum']

def get_this_quarter_expectation(user):
    """
    expect this quater incomes
    """
    prev_quarter_end = (date.today() - pd.tseries.offsets.BQuarterEnd(1)).date()
    start_date = get_last_wednesday_of_month(prev_quarter_end) - timedelta(days=9)

    this_quarter_end = (date.today() + pd.tseries.offsets.BQuarterEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_quarter_end) - timedelta(days=10)

    return get_incomes_of_period(user, start_date, end_date).sum()

def get_this_quarter_earning(user):
    """
    calculate current earning of this quarter
    """
    prev_quarter_end = (date.today() - pd.tseries.offsets.BQuarterEnd(1)).date()
    start_date = get_last_wednesday_of_month(prev_quarter_end) - timedelta(days=9)

    this_quarter_end = (date.today() + pd.tseries.offsets.BQuarterEnd(0)).date()
    end_date = get_last_wednesday_of_month(this_quarter_end) - timedelta(days=10)
    sum = Transaction.objects.filter(created_at__gte=start_date, created_at__lte=end_date, financial_request__requester=user, financial_request__type__in=[cs.FINANCIAL_TYPE_RCV_PAYMENT, cs.FINANCIAL_TYPE_REFUND_PAYMENT]).aggregate(Sum('net_amount'))
    return sum['net_amount__sum']
