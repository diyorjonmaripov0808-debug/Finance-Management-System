from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login'), name='root_redirect'),
    path('register/', views.register_step1_view, name='register_step1'),
    path('register/step2/', views.register_step2_view, name='register_step2'),
    path('register/step3/', views.register_step3_view, name='register_step3'),
    path('register/resend/', views.resend_otp_view, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_update_view, name='profile'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password/verify/', views.forgot_password_verify_view, name='forgot_password_verify'),
    path('forgot-password/confirm/', views.reset_password_confirm_view, name='reset_password_confirm'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]