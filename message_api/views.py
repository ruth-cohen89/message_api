from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .models import Message
from .serializers import MessageSerializer

def get_or_create_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


class SignUpAPIView(APIView):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = get_or_create_token(user)
            
            return Response({'message': 'User created successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            token = get_or_create_token(user)
            
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class MessageListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        
        
# class MessageListCreateAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         messages = Message.objects.filter(receiver=request.user)
        
#         if not messages.exists():
#             return Response({"detail": "No messages found for this user."})
        
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(sender=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnreadMessagesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        unread_messages = Message.objects.filter(receiver=request.user, is_read=False)
        
        if not unread_messages.exists():
            return Response({"detail": "No unread messages found for this user."})
        
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
    

class MessageRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_object(self):
        return get_object_or_404(Message, pk=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user == instance.receiver:
            instance.is_read = True
            instance.save()
            
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user == instance.sender or request.user == instance.receiver:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You do not have permission to delete this message.")
 
    # def perform_destroy(self, instance):
    #     instance.delete()

    
    
#  authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get_object(self, pk):
        return get_object_or_404(Message, pk=pk)

    def get(self, request, pk):
        try:
            message = self.get_object(pk)
            
            if request.user == message.receiver:
                message.is_read = True
                message.save()
                
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        except Http404:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            message = self.get_object(pk)
            message.delete()
            return Response({'message': 'Message deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)   