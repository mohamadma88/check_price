from rest_framework import serializers
from .models import User, Otp , Profile


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)


class OtpVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.IntegerField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('name','last_name','birthday','melicode','bank')
        read_only_fields = ['phone']
