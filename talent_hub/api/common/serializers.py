from rest_framework import serializers

from user.models import User, Profile, Account, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'platform_type',
            'password',
            'location',
            'recovery_email',
            'url'
        )
    

class ProfileSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, source='account_set')

    class Meta:
        model = Profile
        fields = (
            'id',
            'profile_type',
            'first_name',
            'last_name',
            'address',
            'country',
            'dob',
            'gender',
            'accounts',
        )


class UserDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    profiles = ProfileSerializer(many=True, source='profile_set')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'role',
            'team',
            'profiles',
        )
