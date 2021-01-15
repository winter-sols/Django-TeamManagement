from rest_framework import serializers

from user.models import User, Profile, Account, Team
from user.serializer import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'platform_type',
            'password',
            'location',
            'recovery_email',
            'url'
        )
    
# Handle nested Serializer : I give up!

class ProfileSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, source='account_set', required=False)
    user = UserSerializer(required=False, )
    read_only_fields = ('user')
    def create(self, validated_data):
        print(validated_data)
        accounts = validated_data.pop('account_set', None)
        instance = super().create(validated_data)
        if accounts is not None:
            accounts_ser = AccountSerializer(data=accounts, many=True)
            accounts_ser.is_valid(raise_exception=True)
            instance.account_set.all().delete()
            accounts_ser.save(profile=instance)
        return instance
    
    def validate(self, data):
        user_id = self.initial_data['user_id']
        user = User.objects.get(pk=user_id)
        data.update({ 'user': user })
        return data

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
            'user_id',
            'accounts',
            'user'
        )


class UserDetailSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    profiles = ProfileSerializer(many=True, source='profile_set', required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'team',
            'profiles',
        )

# Handle nested Serializer : I give up!
class UserDetailUpdateSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, source='profile_set', required=False)

    def update(self, instance, validated_data):
        # # Update team data
        # team = validated_data.pop('team', None)
        # if team is not None:
        #     team_ser = TeamSerializer(data=team)
        #     team_ser.is_valid(raise_exception=True)
        #     validated_data['team'] = team_ser.save()

        # Update profile data
        profiles = validated_data.pop('profile_set', None)
        if profiles is not None:
            profiles_ser = ProfileSerializer(data=profiles, many=True)
            profiles_ser.is_valid(raise_exception=True)
            instance.profile_set.all().delete()
            profiles_ser.save(user=instance)

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'team_id',
            'profiles',
        )
