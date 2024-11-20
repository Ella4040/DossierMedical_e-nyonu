from django.db import models
from django.conf import settings  # Ajoutez cet import
from django.contrib.auth import get_user_model


class Profile(models.Model):
    ROLE_CHOICES = [
        ('Patient', 'Patient'),
        ('Gynecologue', 'Gynecologue'),
        ('Administrateur', 'Administrateur'),
        ('Secretaire', 'Secretaire'),
        ('Infirmier', 'Infirmier'),
        ('TTechnicienLaboratoire', 'TechnicienLaboratoire'),
        ('Pharmacien', 'Pharmacien'),
        ('TechnicienEchographe', 'TechnicienEchographe'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_account')
    role = models.CharField(max_length=22, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'


    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

