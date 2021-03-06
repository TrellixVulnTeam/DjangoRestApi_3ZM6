from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions, validators
from rest_framework.serializers import ModelSerializer, Serializer

from core.serializers import BaseModelSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(BaseModelSerializer):

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "username")




"""class UserBaseSerialiazer(Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=30, allow_blank=False, allow_null=True)
    last_name = serializers.CharField(max_length=30, allow_blank=False)
    email = serializers.EmailField(required=True,
                                   validators=[
                                       validators.UniqueValidator(
                                           queryset=User.objects.all(),

                                       )
                                   ]
                                   )
    password = serializers.CharField()

    def validate_password(self, password):
        if not validate_password(password):
            return exceptions.ValidationError(detail="Password invalid")
        return password

    def validate_email(self, email):
        if email.endswith(('@datawiz.io', "@gmail.com")):
            return exceptions.ValidationError("Такі емейли не є доступні")
        return email

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return  attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()

    class Meta:
        model = User"""
