from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetDoneView
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # je spécifie success_url ici
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("password-change/", auth_views.PasswordChangeView.as_view(), name='password_change'),
    path("password-change/done/", PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("password-reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password-reset/complete", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # autres routes
    path("login/", auth_views.LoginView.as_view(success_url='dashboard'), name='login'), 
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
]
