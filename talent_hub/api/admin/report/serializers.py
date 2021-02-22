import numpy as np
from rest_framework import serializers
from user.models import User, Team
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning,
    get_this_month_project_earning
)


class DeveloperMonthlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()
    project_earnings = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_this_month_earning(obj)

    def get_project_earnings(self, obj):
        return get_this_month_project_earning(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')


class DeveloperQuarterlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_this_quarter_earning(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning')


class DeveloperWeeklyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_this_week_earning(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning')


class TeamMonthlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            team_earnings[member_index] = get_this_month_earning(member_set[member_index])
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'earning')


class TeamQuarterlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            team_earnings[member_index] = get_this_quarter_earning(member_set[member_index])
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'earning')


class TeamWeeklyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            team_earnings[member_index] = get_this_week_earning(member_set[member_index])
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'earning')
