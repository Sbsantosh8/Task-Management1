from pathlib import __all__
from rest_framework import serializers
from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token["email"] = user.email
        return token

    def validate(self, attrs):
        # Replace 'username' with 'email'
        attrs["email"] = attrs.pop("email", None)
        return super().validate(attrs)
