import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.models import Token
from .tasks import send_sms


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def create(self, validated_data):
        try:
            user = get_user_model().objects.get_or_create(phone_number=validated_data['phone_number'])
            send_sms.delay(validated_data['phone_number'], user[0].id)
            return validated_data
        except Exception:
            serializers.ValidationError(Exception)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        if not re.match(r'^09\d{9}$', phone_number):
            raise serializers.ValidationError("شماره تلفن وارد شده صحیح نمی باشد!")
        return attrs


class SMSTokenCheckingSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    Token = serializers.CharField(style={"input_type": "password"})
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_data):
        token_object = Token.objects.get(token=validated_data['Token'],
                                         user__phone_number=validated_data['phone_number'])
        user = token_object.user
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        token_object.delete()
        return {'access': str(access), 'refresh': str(refresh), 'Token': validated_data['Token'],
                'phone_number': validated_data['phone_number']}

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        if not re.match(r'^09\d{9}$', phone_number):
            raise serializers.ValidationError("شماره تلفن وارد شده صحیح نمی باشد!")
        elif attrs.get('Token') is None:
            raise serializers.ValidationError('کد تایید را وارد کنید!')
        elif not re.match(r'^\d+$', attrs.get('Token')):
            raise serializers.ValidationError('کد تایید باید عدد باشد!')
        elif len(attrs.get('Token')) != 6:
            raise serializers.ValidationError('کد تایید باید 6 رقم باشد!')
        elif not Token.objects.filter(token=attrs.get('Token'), user__phone_number=attrs.get('phone_number')).exists():
            raise serializers.ValidationError('کد تایید اشتباه است!')
        return attrs
