import numpy as np
from rest_framework import serializers
from user.models import User, Team
from user.constants import ROLE_DEVELOPER, ROLE_TEAM_MANAGER
from api.utils.provider import (
    get_earnings,
    get_user_project_earnings,
)


class ReportProjectEarningsSerializer(serializers.ModelSerializer):
    project_earnings = serializers.SerializerMethodField()

    def get_project_earnings(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        return get_user_project_earnings(obj, period, start_date, end_date)

    class Meta:
        model = User
        fields = ('id', 'project_earnings')


class ReportDeveloperSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        return get_earnings(obj, period,  None, obj, start_date, end_date)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning')


class ReportDeveloperProjectSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()
    project_earnings = serializers.SerializerMethodField()

    def get_earning(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        return get_earnings( obj, period, None, obj, start_date, end_date)

    def get_project_earnings(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        return get_user_project_earnings( obj, period, start_date, end_date)

    class Meta:
        model = User
        fields = ('id', 'earning', 'project_earnings')


class ReportTeamSerializer(serializers.ModelSerializer):
    earnings = serializers.SerializerMethodField()

    def get_earnings(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        viewer = context.get('viewer')
        earnings = get_earnings(viewer, period, obj, None, start_date, end_date)
        return earnings

    class Meta:
        model = Team
        fields = ('id', 'name', 'earnings') 
