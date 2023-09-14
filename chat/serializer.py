from rest_framework import serializers
from .models import Room, Message
from base.serializer import CustomUserSerializer
from base.models import CustomUser

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'created_at','image')
        
        

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = Message
        fields = ['id', 'author', 'content', 'timestamp']


class MessageListViewSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    class Meta:
        model = Message
        fields = ['id', 'author', 'content', 'timestamp']