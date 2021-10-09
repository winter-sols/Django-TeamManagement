from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from api.common.finance.serializers import FinancialRequestDetailSerializer, FinancialRequestSerializer, TransactionCreateSerializer
from api.permission import IsAdmin
from finance.models import FinancialRequest, Transaction
from finance.constants import (
    FINANCIAL_STATUS_APPROVED,
    FINANCIAL_STATUS_DECLINED,
    FINANCIAL_TYPE_SND_INVOICE,
    FINANCIAL_STATUS_PENDING,
    FINANCIAL_TYPE_RCV_PAYMENT
)


class ApproveFinanicalRequestView(UpdateAPIView):
    serializer_class = FinancialRequestDetailSerializer
    permission_classes = [IsAdmin]
    queryset = FinancialRequest.objects.all()

    def update(self, request, pk):
        financial_request = FinancialRequest.objects.get(id=pk)
        if financial_request.type != FINANCIAL_TYPE_SND_INVOICE:
            transaction_data = request.data
            transaction_data['financial_request'] = pk
            transaction_ser = TransactionCreateSerializer(data=transaction_data)
            transaction_ser.is_valid(raise_exception=True)
            transaction_ser.save()
        instance = self.get_object()
        instance.status = FINANCIAL_STATUS_APPROVED
        serializer = self.get_serializer(instance)
        instance.save()
        
        if financial_request.type == FINANCIAL_TYPE_SND_INVOICE:
            instance.pk = None
            instance.status = FINANCIAL_STATUS_PENDING
            instance.type = FINANCIAL_TYPE_RCV_PAYMENT
            instance.save()

        return Response(serializer.data)

class DeclineFinanicalRequestView(UpdateAPIView):
    serializer_class = FinancialRequestDetailSerializer
    permission_classes = [IsAdmin]
    queryset = FinancialRequest.objects.all()

    def update(self, request, pk):
        instance = self.get_object()
        instance.status = FINANCIAL_STATUS_DECLINED
        serializer = self.get_serializer(instance)
        instance.save()
        return Response(serializer.data)
