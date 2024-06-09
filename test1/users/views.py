from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import serialize
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import datetime,jwt
# Create your views here.

class RegisterView(APIView):

    def post(self,request):
        
        serializer=serialize(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

            

class LoginView(APIView):

    def post(self,request):
        email=request.data['email']
        password=request.data['password']

        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('user not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('passworword incorrect')
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token=jwt.encode(payload,'secret',algorithm='HS256')

        response=Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        return response


class UserView(APIView):

    def get(self,request):
        token=request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthoried')
        
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthoried error")
        
        user=User.objects.filter(id=payload['id']).first()
        serialiser=serialize(user)
    
        return Response(serialiser.data)