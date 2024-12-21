from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    user_type = serializers.CharField()

    def validate(self, data):
        if 'username' not in data:
            raise serializers.ValidationError('Username not porvided')
        if 'email' not in data:
            raise serializers.ValidationError('email not provided')
        if 'password' not in data:
            raise serializers.ValidationError('password not provided')
        if 'user_type' not in data:
            raise serializers.ValidationError('user type not provided')
        
        user = User.objects.filter(email = data['email'])
        if not user.exists(): # means user if good to go for registration
            return data
        else:
            raise serializers.ValidationError('user already exists')
        
    def create(self, validated_data):
        try:
            user = User.objects.create(username = validated_data['username'], 
                                       email = validated_data['email'], 
                                       user_type=validated_data['user_type'])
            user.set_password(raw_password=validated_data['password'])
            user.save()
            return validated_data
        except Exception as e:
            return e

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    user_type = serializers.CharField()

    def validate(self, data):
        is_user = User.objects.filter(email = data['email'], user_type=data['user_type']).first()
        if is_user:
            return data
        else:
            raise serializers.ValidationError('invalid username or user type')