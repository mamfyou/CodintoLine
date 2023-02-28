from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase

from core.serializers import LoginSerializer, SMSTokenCheckingSerializer, RefreshTokenSerializer


class LoginViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(data={'response: کد با موفقیت ارسال شد'}, status=status.HTTP_201_CREATED, headers=headers)


class SMSTokenCheckingViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = SMSTokenCheckingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'access': serializer.data['access'], 'refresh': serializer.data['refresh']},
                        status=status.HTTP_201_CREATED, headers=headers)


class RefreshTokenViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RefreshTokenSerializer

