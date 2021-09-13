from django.db.models import QuerySet
from .constants import (
    PROJECT_STATUS_ONGOING,
    FINANCIAL_STATUS_PENDING,
    FINANCIAL_STATUS_APPROVED,
    FINANCIAL_TYPE_RCV_PAYMENT,
    FINANCIAL_STATUS_DECLINED
)


class ProjectManager(QuerySet):
    def ongoing_projects(self):
        return self.filter(status=PROJECT_STATUS_ONGOING)


class FinancialRequestMangager(QuerySet):
    def pending_requests(self):
        return self.filter(status=FINANCIAL_STATUS_PENDING)
    
    def approved_requests(self):
        return self.filter(status=FINANCIAL_STATUS_APPROVED)
        
    def declined_requests(self):
        return self.filter(status=FINANCIAL_STATUS_DECLINED)
