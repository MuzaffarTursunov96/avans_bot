from rest_framework import serializers
from .models import AvansUser


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AvansUser
        fields = '__all__'


class UserIdsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AvansUser
        fields = ['user_id','chat_id']
        
    