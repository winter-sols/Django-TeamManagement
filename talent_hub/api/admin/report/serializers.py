from rest_framework import serializers
from user.models import User

class DeveloperReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

