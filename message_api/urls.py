from django.contrib import admin
from django.urls import path
from .views import SignUpAPIView, LoginAPIView, MessageListCreateAPIView, MessageRetrieveDestroyAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveDestroyAPIView.as_view(), name='message-detail'),
]
