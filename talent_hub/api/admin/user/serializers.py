from user.models import User, Team
from rest_framework import serializers


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role',)


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'pk')
