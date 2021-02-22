from rest_framework import serializers
from user.models import User


class SearchUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    
    class Meta:
        model = User
        fields = ('id', 'full_name')
