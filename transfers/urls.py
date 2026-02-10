from django.urls import path
from . import views

urlpatterns = [
    path('', views.transfer_list_view, name='transfer_list'),
    path('create/', views.transfer_create_view, name='transfer_create'),
    path('<uuid:pk>/delete/', views.transfer_delete_view, name='transfer_delete'),
]