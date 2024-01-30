from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404


from .models import Message
from .serializers import MessageSerializer


class SignUpAPIView(APIView):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after sign up
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class MessageListCreateAPIView(APIView):
    def get(self, request):
        messages = Message.objects.filter(sender=request.user)
        
        if not messages.exists():
            return Response({"detail": "No messages found for this user."})
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageRetrieveDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Message, pk=pk)

    def get(self, request, pk):
        try:
            message = self.get_object(pk)
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
