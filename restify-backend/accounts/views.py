from django.shortcuts import render
from rest_framework.generics import get_object_or_404, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, RegisterSerializer, EditUserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import FileResponse
# Create your views here.


class UserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EditProfileAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EditUserProfileSerializer

    def get_object(self):
        return self.request.user


class RetrieveAvatarAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            img =  open('accounts/pictures/%s' % (self.kwargs['avatar_url']), 'rb')
        except FileNotFoundError:
            print('hello')
            return FileResponse()
        return FileResponse(img)



