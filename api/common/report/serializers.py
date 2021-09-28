import numpy as np
from rest_framework import serializers
from user.models import User, Team
from user.constants import ROLE_DEVELOPER, ROLE_TEAM_MANAGER
from api.utils.provider import (
    get_earnings,
    get_user_project_earnings,
)


class IndividualDeveloperProjectSerializer(serializers.ModelSerializer):
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
        return get_user_project_earnings( obj, period)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')



class DeveloperMonthlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_earnings( obj, 'this-month', None, obj)


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning')

class DeveloperQuarterlyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_earnings(obj, 'this-quarter', None, obj)


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning')


class DeveloperWeeklyReportSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    def get_earning(self, obj):
        return get_earnings(obj, 'this-week',  None, obj)


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'earning')


class DeveloperReportSerializer(serializers.ModelSerializer):
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

# class DeveloperCustomReportSerializer(serializers.ModelSerializer):
#     earning = serializers.SerializerMethodField()
#     project_earnings = serializers.SerializerMethodField()

#     def get_earning(self, obj , date_from, date_to):
#         print("Here print")
#         return get_custom_earning(obj, date_from, date_to)

#         return get_custom_project_earning(obj, date_from, date_to)
#     def get_project_earnings(self, obj, date_from, date_to):

#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'earning', 'project_earnings')
      

class TeamReportSerializer(serializers.ModelSerializer):
    team_earnings = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_team_earnings(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = {
                "id": member.id,
                "full_name": member.first_name + " " + member.last_name,
                "earning": get_earnings(member_set[member_index], period, None, member_set[member_index], start_date, end_date)
            }
        return team_earnings

    def get_total(self, obj):
        context = self.context
        period = context.get('period')
        start_date = context.get('start_date')
        end_date = context.get('end_date')
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_earnings(member_set[member_index], period, None, member_set[member_index], start_date, end_date)
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'team_earnings', 'total') 


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
                "earning": get_earnings(member_set[member_index], 'this-month', None, member_set[member_index])
            }
        return team_earnings

    def get_total(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_earnings(member_set[member_index], 'this-month', None, member_set[member_index])
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
                "earning": get_earnings(member_set[member_index],'this-quarter',  None, member_set[member_index])
            }
        return team_earnings

    def get_total(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_earnings(member_set[member_index],'this-quarter',  None, member_set[member_index])
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
                "earning": get_earnings(member_set[member_index], 'this-week', None, member_set[member_index])
            }
        return team_earnings
   
    def get_total(self, obj):
        member_set = obj.user_set.all()
        member_cnt = member_set.count()
        team_earnings = list(range(member_cnt))
        for member_index in range(member_cnt):
            member = member_set[member_index]
            team_earnings[member_index] = get_earnings(member_set[member_index], 'this-week', None, member_set[member_index])
        return np.sum(team_earnings)

    class Meta:
        model = Team
        fields = ('id', 'name', 'team_earnings', 'total')

