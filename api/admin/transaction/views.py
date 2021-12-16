from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.permission import IsAdmin
from api.common.finance.serializers import TransactionDetailSerializer, TransactionCreateSerializer
from .filters import TransactionFilter
from finance.models import Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransactionFilter
    queryset = Transaction.objects.all()

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Transaction.objects.none()
        elif self.request.user.is_admin:
            return Transaction.objects.all()
        elif self.request.user.is_team_manager:
            return Transaction.objects.filter(owner__in=self.request.user.team_members)
        elif self.request.user.is_developer:
            return Transaction.objects.filter(owner=self.request.user)
        elif self.request.method in ['GET']:
            return Transaction.objects \
            .filter_by_period(self.request.query_params) \
            .order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'POST', 'PATCH']:
            return TransactionCreateSerializer
        return TransactionDetailSerializer
