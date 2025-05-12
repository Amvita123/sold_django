from users.serializers.user_serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.service import send_otp_email
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.service import  generate_otp, verify_otp
from .service import extract_ip, get_country_from_ip


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            ip_address = extract_ip(request)
            country = get_country_from_ip(ip_address) or "IN"
            user.country = country
            user.save()

            otp = generate_otp(user.id)
            send_otp_email(user.email, otp)

            response_data = RegisterSerializer(user).data
            refresh = RefreshToken.for_user(user)

            return Response({"message": "Account created successfully", "user": response_data,
                             'access_token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)


class VerificationOtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                if verify_otp(user.id, otp):
                    user.is_active=True
                    user.is_email_verified = True
                    user.save()
                    return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": "User  with this email not found"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError({'password': 'Invalid password'})

                if not user.is_active:
                    return Response({"message": "Please verify OTP first."}, status=status.HTTP_403_FORBIDDEN)

                response_data = LoginSerializer(user).data

                is_verified = response_data.pop('is_verified', False)
                status_response = response_data.pop('status', False)

                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Account logged in successfully',"user": response_data, 'is_verified': is_verified,
                    'access_token': str(refresh.access_token),
                    'status': status_response,
                    # 'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            otp=serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                if verify_otp(user.id, otp):
                    user.is_email_verified=True
                    user.save()
                    return Response({"message": "OTP verified"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"message": "User with this email not found"}, status=status.HTTP_400_BAD_REQUEST)


class RequestOtpView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp = generate_otp(user.id)
                send_otp_email(user.email, otp)
                return Response({"message": "OTP sent successfully."})
            except User.DoesNotExist:
                return Response({"message": "User with this email not found."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSuperUserView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = CreateSuperUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            response_data=CreateSuperUserSerializer(user).data
            status_response = response_data.pop('status', False)
            return Response({"message": "Superuser created successfully", "data":response_data, "status": status_response}, status=status.HTTP_200_OK)
