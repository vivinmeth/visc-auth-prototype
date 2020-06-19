from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from authenticator import models


class UserSerializer(serializers.ModelSerializer):
    """Serializes a User Object"""
    class Meta:
        model = models.Users
        fields = ('id', 'uname', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """ Create and return a new user"""
        user = models.Users.objects.create_user(
            uname=validated_data['uname'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        """ update and return the user"""
        

class AuthTokenSerializer(serializers.Serializer):
    """ Serailezes User AuthToken OBJ"""
    uname= serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """ Validate and Auth an User"""
        uname = attrs.get('uname')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),username=uname,password=password)
        if not user:
            msg = _('Authentication Failed. Check Credentials!')
            raise serializers.ValidationError(msg, code="authentication")

        attrs['user']= user
        return attrs


class ManageUserSerializer(serializers.ModelSerializer):
    """Serializes a User Object"""

    class Meta:
        model = models.Users
        fields = ('id', 'uname', 'password', 'is_omega', 'is_alpha', 'is_beta', 'is_superuser', )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }


    def update(self, instance, validated_data):
        """ update and return the user"""
        password = validated_data.pop('password',None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user