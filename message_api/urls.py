from django.contrib import admin
from django.urls import path
from .views import SignUpAPIView, LoginAPIView, MessageListCreateAPIView, MessageRetrieveDestroyAPIView, UnreadMessagesAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('messages/unread', UnreadMessagesAPIView.as_view(), name='unread-message-list'),
    path('messages/<int:pk>/', MessageRetrieveDestroyAPIView.as_view(), name='message-detail'),
]
