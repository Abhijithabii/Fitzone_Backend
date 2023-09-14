from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Message
from .serializer import RoomSerializer, MessageSerializer, MessageListViewSerializer
from adminside.models import *
from adminside.serializer import TrainerViewSerializer


class RoomListView(APIView):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)    
        if Trainer.objects.filter(user=user).exists():
            rooms = Room.objects.filter(name=user.username)
        else:
            purchased_trainers = PurchasedOrder.objects.filter(user=user)
            trainer_names = [purchase.selected_trainer.user.username for purchase in purchased_trainers]
            rooms = Room.objects.filter(name__in=trainer_names)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = RoomSerializer(data=request.data)
    #     if serializer.is_valid():
    #         room = serializer.save()
    #         return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class TrainerRoomListView(APIView):
#     def get(self, request):
#         print("inside trainer rom")
#         room = Trainer.objects.all()
#         serializer = TrainerViewSerializer(room, many=True)
#         return Response(serializer.data)


class RoomDetailView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    # Add logic for updating and deleting a room if needed


class MessageListView(APIView):
    def get(self, request, room_id):
        print(room_id)
        try:
            room = Room.objects.get(id=room_id)
            print('inside MessageListView..............')
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        messages = room.messages.all().select_related('author')
        serializer = MessageListViewSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = MessageSerializer(data=request.data)
   
        if serializer.is_valid():
            message = serializer.save(room=room)
            print(message)
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    def get(self, request, room_id, message_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            message = room.messages.get(id=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

class RoomCreateAPIView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)