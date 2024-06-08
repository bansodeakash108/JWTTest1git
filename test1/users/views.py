from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import serialize
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
# Create your views here.

class Register(APIView):


    def post(self,request):
        
        serializer=serialize(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

            