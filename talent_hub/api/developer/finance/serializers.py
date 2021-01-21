from rest_framework import serializers
from finance.models import Client, Partner, Project

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'type', 'full_name', 'company_name', 'started_at')
 

class PartnerSerializer(serializers.ModelSerializer):
    contact_method = serializers.JSONField()

    class Meta:
         model = Partner
         fields = ('id', 'full_name', 'email', 'address', 'dob', 'phone_num', 'contact_method')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = ('id', 'title', 'type', 'price', 'client', 'participants', 'project_starter', 'started_at', 'ended_at', 'status')
        fields = '__all__'
