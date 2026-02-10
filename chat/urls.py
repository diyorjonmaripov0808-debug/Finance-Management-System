from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('admin/', views.admin_chat_list_view, name='admin_chat_list'),
    path('admin/<uuid:conversation_id>/', views.admin_chat_detail_view, name='admin_chat_detail'),
    path('user/<int:user_id>/', views.admin_start_chat_view, name='admin_start_chat'),
]