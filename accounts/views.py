from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_backends
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.backends import ModelBackend




class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

@csrf_protect
@login_required
def dashboard_redirect(request: HttpRequest) -> HttpResponse:
    user = request.user
    if hasattr(user, 'profile'):
        role = user.profile.role

        # Redirection en fonction du rôle
        redirect_mapping = {
            'Patient': 'patient_dashboard',
            'Gynecologue': 'gynecologue_dashboard',
            'Administrateur': 'admin_dashboard',
            'Secretaire': 'secretaire_dashboard',
            'Infirmiere': 'infirmiere_dashboard',
            'Laboratin': 'laboratin_dashboard',
            'Pharmacien': 'pharmacien_dashboard',
            'Echographe': 'echographe_dashboard',
        }
        return redirect(redirect_mapping.get(role, 'default_dashboard'))
    return redirect('default_dashboard')
