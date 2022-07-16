from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import re
from django.core.exceptions import ObjectDoesNotExist



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "phone_number",
        )


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source="profile")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_profile']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    avatar = serializers.ImageField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=12)
    first_name = serializers.CharField(required=True, max_length=10,  allow_blank=False)
    last_name = serializers.CharField(required=True, max_length=10,  allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2', 'avatar', 'phone_number')

    def validate(self, attrs):
        if attrs.get('phone_number', False):
            r = re.compile(r'\+1\d\d\d\d\d\d\d\d\d\d')
            if not r.match(attrs['phone_number']):
                raise serializers.ValidationError({"phone_number": "Please enter a valid 10 digit phone number (eg.+19051233211)"})

        else:
             raise serializers.ValidationError(
                    {"phone_number": "Phone number is required"})

        
        if not attrs.get('avatar', False):
             raise serializers.ValidationError(
                    {"avatar": "avatar is required"})


        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "passwords do not match"})

        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        if validated_data.get('avatar', False):
            user.profile.avatar = validated_data['avatar']

        if validated_data.get('phone_number', False):
            user.profile.phone_number = validated_data['phone_number']

        user.save()
        return user


class EditUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    avatar = serializers.ImageField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=12)
    first_name = serializers.CharField(required=True, max_length=10, allow_blank=False)
    last_name = serializers.CharField(required=True, max_length=10, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'phone_number', 'password')

    def validate(self, attrs):
        if attrs.get('phone_number', False):
            r = re.compile(r'\+1\d\d\d\d\d\d\d\d\d\d')
            if not r.match(attrs['phone_number']):
                raise serializers.ValidationError(
                    {"phone_number": "Please enter a valid 10 digit phone number (eg.+19051233211)"})
        
        else:
             raise serializers.ValidationError(
                    {"phone_number": "Phone number is required"})

        if not attrs.get('avatar', False):
             raise serializers.ValidationError(
                    {"avatar": "avatar is required"})

        
        # try:
        #     print(attrs.get("username", ""), attrs.get("password", "") )
        #     User.objects.get(username=attrs.get("username", ""))

        # except ObjectDoesNotExist:
        #     raise serializers.ValidationError({"password": "Please enter you password to update you account"})

        return attrs

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']

        instance.profile.avatar = validated_data.get('avatar', None)
        instance.profile.phone_number = validated_data.get('phone_number', False)

        instance.save()
        return instance
