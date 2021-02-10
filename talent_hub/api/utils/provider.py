import pandas as pd
from datetime import date, timedelta
from finance.models import Project, FinancialRequest
from finance import constants as cs

def get_ongoing_projects(user):
    if user.is_admin:
        queryset = Project.objects.ongoing_projects()
    elif user.is_team_manager:
        queryset = Project.objects.ongoing_projects().filter(participants__in=user.team.user_set.all())
    elif user.is_developer:
        queryset = user.projects.ongoing_projects()
    return queryset

def get_weekly_income(user):
    """
    calculate weekly incomes and return it with series
    """
    queryset = get_ongoing_projects(user)
    today = date.today()
    week_of_today = today.weekday()
    w_start_date = today - timedelta(days=week_of_today)
    w_end_date = today + timedelta(days=6-week_of_today)
    now_week_dates = pd.date_range(w_start_date, periods=7)
    weekly_income_series = pd.Series(0, index=now_week_dates)
    for item in queryset:
        start_date = max(w_start_date, item.started_at)
        if item.type == cs.PROJECT_TYPE_BUDGET:
            if item.ended_at <= w_end_date and item.ended_at >= w_start_date:
                start_date = item.ended_at
            else:
                continue
        end_date = min(w_end_date, item.ended_at) if item.ended_at is not None else w_end_date
        if item.type == cs.PROJECT_TYPE_BUDGET:
            proj_week_dates = pd.date_range(start_date, end_date)
        else:
            proj_week_dates = pd.bdate_range(start_date, end_date, freq='B')
        if item.type != cs.PROJECT_TYPE_BUDGET:
            weekly_working_hours_series = pd.Series((item.weakly_limit or 0) / 5, index=proj_week_dates) 
        else:
            weekly_working_hours_series = pd.Series(1, index=proj_week_dates)     
        weekly_working_rate_series = pd.Series(item.price, index=proj_week_dates)
        weekly_income_series = weekly_income_series.add(weekly_working_hours_series * weekly_working_rate_series, fill_value=0)
    return weekly_income_series

def get_pending_financial_requests(user):
    if user.is_admin:
        return FinancialRequest.objects.pending_requests()
    elif user.is_team_manager:
        return FinancialRequest.objects.pending_requests().filter(requester__in=user.team.user_set.all())
    elif user.is_developer:
        print(dir(user))
        return user.financialrequest_set.pending_requests()
