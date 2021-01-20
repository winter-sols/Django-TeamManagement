from rest_framework import serializers
from finance.models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'type', 'full_name', 'company_name')
 