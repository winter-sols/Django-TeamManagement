from rest_framework import serializers
from reporting.models import Log
from user.serializer import UserSerializer

class LogDetailSerializer(serializers.ModelSerializer):
  owner = UserSerializer()
  
  class Meta:
    model = Log
    fields = ('id', 'owner', 'plan', 'achievements', 'log_type', 'created_at', 'updated_at', 'interval')
