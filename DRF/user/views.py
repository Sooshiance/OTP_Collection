from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import permissions, response, status, generics
from rest_framework_simplejwt import tokens

from .models import User, OTP
from .serializers import (CustomTokenSerializer,
                          OTPSerializer,
                          ProfileSerializer,)
from .utils import sendToken


class RequestOtpAPIView(generics.GenericAPIView):
    """
    An endpoint for users to request OTP tokens
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenSerializer(data=request.data)
        if serializer.is_valid():
            
            phone = serializer.validated_data["phone"]
            
            if phone:
                user = User.objects.get_or_create(phone=phone)
                
                if user is not None:
                    
                    user = get_object_or_404(User, phone=phone)

                    # TODO: Check if user has already otp token in OTP model
                    try:
                        if not OTP.objects.get(user=user):
                            result = sendToken(user=user)
                            otp    = result['otp']
                            error  = result['error']
                            if otp:
                                print(f"The OTP is ======= {otp}")
                                return response.Response({"mobile": user.phone[-4:]}, status=status.HTTP_200_OK)
                            else:
                                # TODO: OTP Does not exist!
                                return response.Response({"waite": error}, status=status.HTTP_201_CREATED)
                        else:
                            # TODO: OTP exist!
                            user_otp = OTP.objects.filter(user=user)
                            for obj in user_otp:
                                # TODO: Delete user otp tokens that created
                                # 2 minutes ago or later
                                # 2 min = 1 min (token expire time) + 1 min(cool down for requesting new token)
                                if timedelta(minutes=2) >= timezone.now() - obj.created_at:
                                    # TODO: Delete expired otp token
                                    obj.delete()
                            return response.Response({"otp exist"}, status=status.HTTP_200_OK)
                    except:
                            result = sendToken(user=user)
                            otp    = result['otp']
                            error  = result['error']
                            print(f"The OTP is ======= {otp}")
                            return response.Response({"mobile": user.phone[-4:]}, status=status.HTTP_200_OK)
            else:
                return response.Response({"error":"no username"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CheckOtpAPIView(generics.GenericAPIView):
    """
    An endpoint for users to send their OTP tokens
    If OTP is right they get access & refresh tokens
    """

    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data["otp"]
            phone = serializer.validated_data["phone"]

            # TODO: Need both `phone` and `otp`
            if not otp or not phone:
                return response.Response({"error":"need both"}, status=status.HTTP_400_BAD_REQUEST)

            # TODO: Check if user and also its otp are exist!
            try:
                user = User.objects.get(phone=phone)
                user_otp = OTP.objects.get(user=user)
            except:
                return response.Response({"error":"User or OTP Not Right"}, status=status.HTTP_401_UNAUTHORIZED)
            
            counter = user_otp.counter

            try:
                if user_otp.otp == otp and counter > 0:
                    # TODO : conflict error between datetime object and
                    #  timedelta object
                    """
                    access_time = (datetime.timedelta(minutes=10)
                    + otp.created_at).timestamp()
                    delta_time = access_time - timezone.now().timestamp()
                    """
                    otp_created_time = user_otp.created_at
                    current_time = timezone.now()
                    time_difference = current_time - otp_created_time
                    if time_difference < timezone.timedelta(minutes=10):
                        user = user_otp.user
                        token = tokens.RefreshToken.for_user(user)
                        data = {"refresh": str(token),
                                "access": str(token.access_token)}
                        user_otp.delete()
                        return response.Response(data, status=status.HTTP_200_OK)
                else:
                    if counter == 0:
                        user_otp.delete()
                        return response.Response({"error":"Counter is zero and got locked"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user_otp.counter -= 1
                        user_otp.save()
                        return response.Response({"counter":user_otp.counter}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return response.Response({'error': "Token is not Right"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                return response.Response({"error": "OTP Not match!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            # TODO: Serializer has errors
            return response.Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint for User's to manage their Profiles
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
