from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

"'this is a typical Serializer in drf, we override the create method to hash the password'"


class UserSerializer(serializers.ModelSerializer):  # for Serializing when passing instance to front end
    password = serializers.CharField(write_only=True)  # ensure that pwd cannot give back

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'firstName', 'lastName', 'company', 'designation', 'password']

    def create(self, validated_data):  # ensure that the password is hashed
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
#