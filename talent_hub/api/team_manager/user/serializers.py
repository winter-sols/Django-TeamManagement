from user.models import User, Team
from rest_framework import serializers


class TeamUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name',)
