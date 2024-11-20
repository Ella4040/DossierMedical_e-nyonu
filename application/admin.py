from django.contrib import admin
from .models import Profile, Patient, Gynecologue

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'nom', 'telephone']

@admin.register(Gynecologue)
class GynecologueAdmin(admin.ModelAdmin):
    list_display = ['user', 'nom', 'specialiste']


