from datetime import datetime , timedelta

import jwt
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.authentication import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.settings import SECRET_KEY
from .serializer import *
from .otp import send_otp_mail, create_otp, otp_change_password
from .auth_token import JwtAuthentication, Dispatch

User = get_user_model()

"""
    here user will do query and its data will be stored in cache memory, 
    and a otp is send to email when user re-enter the otp and if its true 
    then it will take the data from cache and will store the data of user 
    into the database.
"""
class Registration(APIView): 

    """_summary_

        Method:
            1. POST()=> here it will get the user email, username, password and user type,
                and then it will store that into a cache memory along with a key and cache
                memory time is 10 minutes, and also a email will be send to the user telling
                him about the Registration Confirmation emil.
    """

    def post(self, request): # no need to give user type
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                key = f'key:{request.data['email']}'
                otp = create_otp()
                data = serializer.data
                data.update({'otp':otp})
                
                cache.set(key, data, timeout=600) # in cache there will be a key, 
                # a value and the time limit of 10 minutesafter which the key will expire
                send_otp_mail(request.data['email'], otp)

                # print('____',cache.get(key)) # checking if the cache return the data or not

            except Exception as e:
                print(e)
                return Response({'message':e}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message':'OTP send to email'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationConfirm(APIView):

    """_summary_

        Method:
            1. POST()=> First it will check wheather the user is giving email and OTP,
                if yes then it will get the otp form the cache(if email is correct).
                then it will verify the otp and then all of the user data will be added
                to the Database. 
    """
    
    def post(self, request): # get otp and email
        try:
            if 'email' in request.data and 'otp' in request.data:
                cache_data = cache.get(f'key:{request.data['email']}')
                if 'otp' in cache_data and cache_data['otp'] == request.data['otp']:
                    cache_data.pop('otp')
                    # print("after cache")    
                    user = User.objects.create(username= cache_data['username'], 
                                            email=cache_data['email'],
                                            user_type=cache_data['user_type'])
                    user.set_password(cache_data['password'])
                    user.save()
                    return Response({'message':"Registration Sucessfull"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return  Response({"message":"email or otp is not provided"})
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):

    """_summary_

        Post: Get the email, password and user type. and if the user is already present
            then it will create and return a jwt(JSON web Token), which can be use to 
            access further api endpoints
    """

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            # as we have made the username field = email
            is_authenticated = authenticate(email = serializer.data['email'],
                                             password = serializer.data['password'])
            if is_authenticated:
                try:
                    payload = {'user_email': serializer.data['email'], 'user_type': data['user_type'],
                            'exp': datetime.utcnow() + timedelta(hours=24)}
                    
                    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')
                    return Response({'message':'login sucessfull', 'token':token}, status=status.HTTP_200_OK)
                except jwt.InvalidKeyError:
                    return Response({"Response": "Key is not valid"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message":"User not authenticated(Invalid Password)"},  status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminOnly(APIView):
    authentication_classes = [JwtAuthentication]
    def get(self, request):
        if request.user.user_type == "admin":
            users = User.objects.all()
            serializer = RegisterSerializer(users, many=True) # -------------------------------------------------------
            return Response(serializer.data)
        else:
            return Response({"Message":"Invaid access"}, status=status.HTTP_400_BAD_REQUEST)
            
class UserDelete(APIView):
    authentication_classes = [JwtAuthentication]
    def delete(self, request):
        try:
            user = User.objects.filter(email = request.data['email']) # user can only delete him/her self
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordOtp(APIView):

    """_summary_

            'When you uncomment the __init__ and dispatch(), then user must need to login
            to change their password', but if you uncomment it know anyone who has to
            change password, can change its password.
        
        Post: Get the user email and verify if the email exists or not, then generate a otp and 
            send that otp to the user email. also add the otp along with key in cache memory as
            well (cache memory time = 10 mins). 
    """

    # def __init__(self):
    #     self.payload = ''

    # def dispatch(self, request, *args, **kwargs):
    #     user, self.payload = Dispatch.get_request(self=self, request=request)
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # email = self.payload.get('user_email')
            email = request.data.get("email")

            user = User.objects.filter(email = email).first()
            if user: 
                key = f'change password {email}'
                otp = create_otp()
                data = otp

                cache.set(key, data, timeout=600)
                otp_change_password(email, otp)
                return Response({"message":f"otp sended to {email} sucessfully"})
            else:
                return Response({"message":"email not found"},status=status.HTTP_404_NOT_FOUND)
        except :
            return Response(serializers.ValidationError)

class ConfirmOtp(APIView):

    """_summary_

        Post: here we will get the otp and email from the user and then we will extract
            the otp from the cache memory, base on the key(key base on user email).
            if the otp is correct then it will say otp is valid, and store a new key 
            cache memory along with the data = True.
    """

    # def __init__(self):
    #     self.payload = ''

    # def dispatch(self, request, *args, **kwargs):
    #     user , self.payload = Dispatch.get_request(self=self, request=request)
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            user_otp = request.data['otp']
            # email = self.payload.get('user_email')
            email = request.data.get("email")
            key = f"change password {email}"
            otp_cache = cache.get(key=key)

            if otp_cache == user_otp:
                key_sucessfull = f"change password {email} sucessfull"
                data = True
                cache.set(key_sucessfull, data, timeout=600)
                return Response({"Message":"OTP matched sucessfully"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"Message":"OTP Invalid"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Message":"Invalid error while varifing otp"})


class ConfirmNewPassowrd(APIView):

    """_summary_

        Here again it will get the email and password and confirm password, checks if the password and 
        confirm password are given or not. If yes are they the same or not. If they are the same then 
        it will save the data.
    """

    # def __init__(self):
    #     self.payload = ''
    #     self.user = ''

    # def dispatch(self, request, *args, **kwargs):
    #     self.user, self.payload = Dispatch.get_request(self=self, request=request)
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if 'password' in request.data and 'confirm_password' in request.data:
            if request.data['password'] == request.data['confirm_password']:
                email = request.data["email"]
                user = User.objects.filter(email = email).first()
                if user:
                    try:
                        # email = self.payload.get("user_email")
                        key = f'change password {email} sucessfull'
                        is_otp_verify = cache.get(key=key)
                        if is_otp_verify:
                            # self.user.set_password(request.data['password'])
                            # self.user.save()

                            user.set_password(request.data["password"])
                            user.save()
                            return Response({"message":"password changed sucessfully"}, status=status.HTTP_202_ACCEPTED)
                            
                        else:
                            return Response({"message":"OTP is not verified"}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response(e, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message":"Password and Confirm passowrd must be the same"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'enter your email or password'}, status=status.HTTP_400_BAD_REQUEST)