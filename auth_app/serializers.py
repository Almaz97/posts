import json

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import requests


from .tasks import save_user_sign_up_date_info


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):

        # check if email is valid
        email = attrs["email"]
        url = f"{settings.EMAIL_CHECK_URL}/?api_key={settings.EMAIL_API_KEY}&email={email}"
        response = requests.get(url)

        # Probably unreliable condition. There might be a case, when third party service
        # is just crashed, but since this is a test task will keep logic simple
        if response.status_code != 200:
            raise serializers.ValidationError("Enter a valid email address.")

        response_body = json.loads(response.content)
        if response_body["is_valid_format"]["value"] is False:
            raise serializers.ValidationError("Enter a valid email address.")

        if response_body["deliverability"] in ["RISKY", "UNKNOWN"]:
            raise serializers.ValidationError("Your email is unknown or risky. Please enter a valid one")

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        save_user_sign_up_date_info.delay(user.id)
        return user
