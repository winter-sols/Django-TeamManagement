import numpy as np
from rest_framework import serializers
from user.models import User, Team
from user.constants import ROLE_DEVELOPER, ROLE_TEAM_MANAGER
from api.utils.provider import (
    get_this_month_earning,
    get_this_quarter_earning,
    get_this_week_earning,
    get_this_month_project_earning,
    get_this_quarter_project_earning,
    get_this_week_project_earning,
)


class DeveloperMonthlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()
    project_earnings = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_this_month_earning(obj, None, obj)

    def get_project_earnings(self, obj):
        return get_this_month_project_earning(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')


class DeveloperQuarterlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()
    project_earnings = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_this_quarter_earning(obj, None, obj)

    def get_project_earnings(self, obj):
        return get_this_quarter_project_earning(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')


class DeveloperWeeklyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()
    project_earnings = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_this_week_earning(obj, ROLE_DEVELOPER)

    def get_project_earnings(self, obj):
        return get_this_week_project_earning(obj)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')


# class DeveloperCustomReportSerializer(serializers.ModelSerializer):
#     earning = serializers.SerializerMethodField()
#     project_earnings = serializers.SerializerMethodField()

#     def get_earning(self, obj , date_from, date_to):
#         print("Here print")
#         return get_custom_earning(obj, date_from, date_to)

#     def get_project_earnings(self, obj, date_from, date_to):
#         return get_custom_project_earning(obj, date_from, date_to)

#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')
      
      
class TeamMonthlyReportSerializer(serializers.ModelSerializer):
    team_earnings = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_team_earnings(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = {
                "id": member.id,
                "full_name": member.first_name + " " + member.last_name,
                "earning": get_this_month_earning(member_set[member_index], None, member_set[member_index])
            }
        return team_earnings

    def get_total(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_this_month_earning(member_set[member_index], None, member_set[member_index])
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'team_earnings', 'total')


class TeamQuarterlyReportSerializer(serializers.ModelSerializer):
    team_earnings = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_team_earnings(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = {
                "id": member.id,
                "full_name": member.first_name + " " + member.last_name,
                "earning": get_this_quarter_earning(member_set[member_index], None, member_set[member_index])
            }
        return team_earnings

    def get_total(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_this_quarter_earning(member_set[member_index], None, member_set[member_index])
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'team_earnings', 'total')


class TeamWeeklyReportSerializer(serializers.ModelSerializer):
    team_earnings = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_team_earnings(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = {
                "id": member.id,
                "full_name": member.first_name + " " + member.last_name,
                "earning": get_this_week_earning(member_set[member_index], ROLE_DEVELOPER)
            }
        return team_earnings
   
    def get_total(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_this_week_earning(member_set[member_index], ROLE_DEVELOPER)
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'team_earnings', 'total')

