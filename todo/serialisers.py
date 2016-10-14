from rest_framework import serializers
from .models import Todo

class TodoSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'status', 'updated')