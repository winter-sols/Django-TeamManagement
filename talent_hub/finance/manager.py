from django.db.models import QuerySet
from .constants import PROJECT_STATUS_ONGOING

class OngoingProjectQuerySet(QuerySet):
    def ongoing_projects(self):
        return self.filter(status=PROJECT_STATUS_ONGOING)
