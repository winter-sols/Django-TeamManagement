from user.models import User
from rest_framework import serializers


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role')
