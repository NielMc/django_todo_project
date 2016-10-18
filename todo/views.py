from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serialisers import TodoSerialiser
from .models import Todo
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Create your views here.
class TodoView(APIView):


    permission_classes = (IsAuthenticated,)
    serialiser_class = TodoSerialiser

    def get(self, request, pk):
        if "username" in request.query_params:
            if pk is not None:
                todo = Todo.objects.get(id=pk)
                serialiser = TodoSerialiser(todo)
            else:
                user = User.objects.get(username=request.query_params["username"])
                todos = Todo.objects.filter()
                serialiser = TodoSerialiser(todos, many=True)
            return Response(serialiser.data)

    def post(self, request):
        serialiser = TodoSerialiser(data=request.data)
        if not serialiser.is_valid():
            return Response(serialiser.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        data = serialiser.data
        user = User.objects.get(username = data["username"])

        Todo.objects.create(user=user, title=data["title"],
        description=data["description"], status=data["status"])

        return Response(serialiser.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        todo = Todo.objects.get(id=pk)
        serialiser = TodoSerialiser(todo, data=request.data)
        if not serialiser.is_valid():
            return Response(serialiser.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serialiser.save()
        return Response(serialiser.data)

    def delete(self, request,pk):
        todo = Todo.objects.get(id=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)