from django.db.models import QuerySet
from .constants import (
    PROJECT_STATUS_ONGOING,
    FINANCIAL_STATUS_PENDING,
    FINANCIAL_TYPE_RCV_PAYMENT
)

class ProjectManager(QuerySet):
    def ongoing_projects(self):
        return self.filter(status=PROJECT_STATUS_ONGOING)


class FinancialRequestMangager(QuerySet):
    def pending_requests(self):
        return self.filter(status=FINANCIAL_STATUS_PENDING)
