from rest_framework.generics import ListAPIView, UpdateAPIView
from api.permission import IsAdminOrManager
from rest_framework.permissions import IsAuthenticated
from api.common.notification.serializers import NotificationListSerializer, NotificationUpdateSerializer
from notification.models import Notification
from rest_framework import mixins


class NotificationListView(ListAPIView):
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        return Notification.objects.unread_items(self.request.user)


class NotificationUpdateView(UpdateAPIView):
    serializer_class = NotificationUpdateSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Notification.objects.unread_items(self.request.user)
    def perform_update(self, serializer):
        print(serializer.instance)
        serializer.instance.mark_as_read()
