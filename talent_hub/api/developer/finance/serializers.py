from rest_framework import serializers
from finance.models import Client, Partner

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'type', 'full_name', 'company_name')
 
class PartnerSerializer(serializers.ModelSerializer):
    contact_method = serializers.JSONField()

    class Meta:
         model = Partner
         fields = ('id', 'full_name', 'email', 'address', 'dob', 'phone_num', 'contact_method')
