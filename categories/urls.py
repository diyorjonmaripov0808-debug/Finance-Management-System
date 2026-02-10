from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list_view, name='category_list'),
    path('create/', views.category_create_view, name='category_create'),
    path('update/<uuid:pk>/', views.category_update_view, name='category_update'),
    path('delete/<uuid:pk>/', views.category_delete_view, name='category_delete'),
]