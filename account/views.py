from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import User, Otp , Profile
import random
from rest_framework.views import APIView
from .serializers import UserLoginSerializer, OtpVerificationSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        otp_code = random.randint(100000, 999999)
        Otp.objects.create(phone=phone, code=otp_code)
        print(f"OTP for {phone}: {otp_code}")

        return Response({"detail": "otp has been sent to your phone"}, status=status.HTTP_200_OK)


class OtpVerificationView(generics.GenericAPIView):
    serializer_class = OtpVerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        try:
            otp = Otp.objects.get(phone=phone, code=code)
            otp.delete()

            User.objects.create(
                phone=phone,
                password=make_password(serializer.validated_data['password'])
            )
            return Response({"detail": "user registered successfully"}, status=status.HTTP_201_CREATED)
        except Otp.DoesNotExist:
            return Response({"detail": "invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(phone=request.user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = ProfileSerializer(profile)
        return Response(ser.data)

    def post(self, request):
        try:
            profile = Profile.objects.get(phone=request.user)
            ser = ProfileSerializer(profile, data=request.data, partial=True)
        except Profile.DoesNotExist:

            ser = ProfileSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save(phone=request.user)
            return Response(ser.data, status=status.HTTP_201_CREATED)

        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)