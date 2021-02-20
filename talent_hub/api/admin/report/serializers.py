from rest_framework import serializers
from user.models import User, Team

class DeveloperReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class TeamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')
