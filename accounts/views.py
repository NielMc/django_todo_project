from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serialisers import RegistrationSerialiser

# Create your views here.
class RegistrationView(APIView):
    serialiser_class = RegistrationSerialiser

    def post(self, request):
        serialiser = RegistrationSerialiser(data=request.data)
        if not serialiser.is_valid():
            return Response(serialiser.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        data = serialiser.data

        user = User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save()

        return Response(serialiser.data, status=status.HTTP_201_CREATED)