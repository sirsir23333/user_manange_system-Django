import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .serializer import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime, timedelta


# Create your views here.

'''UserView is for user/, specifically for login and register. Since we are using restful api,
we do not want any verb like login or register inside our link. So we just differentiate by a param.
 The param is action=login or action=register.
    So if user use GET method to access the url, which they have to at the very start, we return the 
     two different params for front-end so that user can be direct to login or register
     Both login and register eventually will need to use POST as the data will be more secured. Once
      the user register, we can also return a param: action=Login for front-end to direct user. Once the
      user login, we also pass a JWT using the module simple jwt to the request head. '''


class UserView(APIView):
    def get(self, request):
        response_data = {
            "login_url": "/user/?action=login",
            "register_url": "/user/?action=register"
        }
        return JsonResponse(response_data)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        action = request.META.get('QUERY_STRING', '')
        if action == "action=login":

            user = authenticate(request, email=email, password=password)
            if user is not None:
                # login(request, user)
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                request.session['email'] = email
                return Response({'email': user.email, 'token': token})
            else:
                return Response({'success': False, 'message': 'Invalid credentials'})

        elif action == "action=register":
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"login_url": "/user/?action=login"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''SingleUserView is for user/1/. In this url, the user should be all login, so we add the JWT Authentication
to specified which kind of method we using for authentication and use the permission inside drf to enforce the 
check. Then we just write the get put delete as usual. Note that we only need to validate the serializer after deserializing
the data, but not for instance.'''


class SingleUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.session.get("email")
        user = User.objects.get(email=email)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request):
        email = request.session.get("email")
        user = User.objects.get(email=email)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'method': 'put'})
        else:
            return Response({'success': False, 'message': serializer.errors})

    def delete(self, request):
        email = request.session.get("email")
        user = User.objects.get(email=email)
        user.delete()
        return Response({'success': True, 'method': 'delete'})


'''The AdminUserView is for the url AdminUser/. Same as the previous view-class, we also use jwt authentication and
permission at the very top, just that for this time we add a IsAdminUser in permission. Note that Admin user means staff 
or superuser. In our case, all the ADMIN role are staff and there is only one superuser which is me :)
 I also add a GetUser method since it is use quite a couple of times(and to make the code look nicer)'''

class AdminUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def GetUser(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        return user

    def get(self, request):
        user = self.GetUser(request)

        serializer = UserSerializer(user)
        return Response(serializer.data)


    def put(self, request):
        user = self.GetUser(request)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.GetUser(request)
        user.delete()
        return Response({'success': True, 'method': 'delete'},status=status.HTTP_204_NO_CONTENT)
