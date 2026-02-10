from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list_view, name='transaction_list'),
    path('income/create/', views.income_create_view, name='income_create'),
    path('expense/create/', views.expense_create_view, name='expense_create'),
    path('delete/<uuid:pk>/', views.transaction_delete_view, name='transaction_delete'),
    path('statistics/', views.statistics_view, name='statistics'),
]