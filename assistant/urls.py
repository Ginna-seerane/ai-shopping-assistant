from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('set-user-type/', views.set_user_type, name='set_user_type'),
    path('chat/', views.chat_message, name='chat_message'),  # Add this line
]