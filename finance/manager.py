from django.db.models import QuerySet
from .constants import (
    PROJECT_STATUS_ONGOING,
    FINANCIAL_STATUS_PENDING,
    FINANCIAL_STATUS_APPROVED,
    FINANCIAL_TYPE_RCV_PAYMENT,
    FINANCIAL_STATUS_DECLINED
)
from utils.helpers import get_dates_from_period


class ProjectQuerySet(QuerySet):
    def ongoing_projects(self):
        return self.filter(status=PROJECT_STATUS_ONGOING)


class FinancialRequestQuerySet(QuerySet):
    def pending_requests(self):
        return self.filter(status=FINANCIAL_STATUS_PENDING)
    
    def approved_requests(self):
        return self.filter(status=FINANCIAL_STATUS_APPROVED)
        
    def declined_requests(self):
        return self.filter(status=FINANCIAL_STATUS_DECLINED)


class TransactionQuerySet(QuerySet):
    def filter_by_period(self, query_params, **kwargs):
        period = query_params.get('period')
        dates = get_dates_from_period(period)
        if dates is not None:
            start_date = dates.get('start_date')
            end_date = dates.get('end_date')
        elif period == 'custom':
            default_dates = get_dates_from_period('this-month')
            start_date = query_params.get('from') or default_dates.get('start_date')
            end_date = query_params.get('to') or default_dates.get('end_date')
        else:
            return self

        return self.filter(created_at__gte=start_date, created_at__lte=end_date)
