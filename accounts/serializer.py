from rest_framework import serializers
from .models import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import auth
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['username','email','password','is_verified']



class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email = serializers.EmailField()
    password=serializers.CharField()
    password_confirm=serializers.CharField()
    def validate(self,data):
        if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
            raise serializers.ValidationError('Username or Email is taken')
        elif data['password']!=data['password_confirm']:
            raise serializers.ValidationError('Passwords did not match!')
        else:
            return data
            
    def create(self,validated_data):
        user= User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password_confirm']
        )
        return validated_data

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    email_verification_token = serializers.CharField() 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields= "__all__"

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self,data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(f"Account not found.")
        return data
    
    def get_jwt_token(self,data):
        user = auth.authenticate(username=data['username'],password=data['password'])
        if not user:
            return {'message':"Invalid Credentials",'data':{}}
        
        refresh=RefreshToken.for_user(user)
        return  {
            'messsage':'Login Success!',
            'data':{
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                }
            }

