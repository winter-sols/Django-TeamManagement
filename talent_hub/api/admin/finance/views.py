from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from api.common.finance.serializers import FinancialRequestDetailSerializer, FinancialRequestSerializer
from finance.models import FinancialRequest
from finance.constants import FINANCIAL_STATUS_APPROVED, FINANCIAL_STATUS_DECLINED

class ApproveFinanicalRequestView(UpdateAPIView):
    serializer_class = FinancialRequestDetailSerializer
    queryset = FinancialRequest.objects.all()

    def update(self, request, pk):
        instance = self.get_object()
        instance.status = FINANCIAL_STATUS_APPROVED
        serializer = self.get_serializer(instance)
        instance.save()
        return Response(serializer.data)

class DeclineFinanicalRequestView(UpdateAPIView):
    serializer_class = FinancialRequestDetailSerializer
    queryset = FinancialRequest.objects.all()

    def update(self, request, pk):
        instance = self.get_object()
        instance.status = FINANCIAL_STATUS_DECLINED
        serializer = self.get_serializer(instance)
        instance.save()
        return Response(serializer.data)
