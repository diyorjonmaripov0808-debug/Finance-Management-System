from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet_list_view, name='wallet_list'),
    path('create/', views.wallet_create_view, name='wallet_create'),
    path('update/<uuid:pk>/', views.wallet_update_view, name='wallet_update'),
    path('delete/<uuid:pk>/', views.wallet_delete_view, name='wallet_delete'),
]