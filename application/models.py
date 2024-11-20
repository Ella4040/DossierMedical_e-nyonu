from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone


# Créer un nouvel utilisateur
try:
    user = User.objects.create_user(
        username='new_user',
        password='password123',
        email='user@example.com',
        first_name='FirstName',
        last_name='LastName'
    )

    # Donner l'accès à l'administration si nécessaire
    user.is_staff = True  # Donne accès à l'administration
    user.save()
    print(f"Utilisateur créé : {user.username}")

    # Créer le profil pour l'utilisateur
    profile = Profile.objects.create(
        user=user,
        role='Patient'  # Assurez-vous de définir le rôle approprié
    )
    print(f"Profil créé : {profile}")

    # Créer le patient associé à l'utilisateur
    patient = Patient.objects.create(
        user=user,
        sexe='F',  # Ou 'M' selon le sexe
        nom='Doe',
        prenom='Jane',
        date_of_birth=timezone.now().date(),  # Remplacez par une date de naissance appropriée
        address='123 Rue Exemple',
        telephone='1234567890',
        email='user@example.com'  # L'email peut être le même ou différent
    )
    print(f"Patient créé : {patient}")

except Exception as e:
    print(f"Erreur lors de la création de l'utilisateur ou du patient : {e}")

# Authentifier l'utilisateur
user = authenticate(username='new_user', password='password123')
if user is not None:
    print(f"Connexion réussie : {user.username}")
else:
    print("Nom d'utilisateur ou mot de passe incorrect.")



"""

# Créer un nouvel utilisateur
try:
    user = User.objects.create_user(
        username='new_user',
        password='password123',
        email='user@example.com',
        first_name='FirstName',
        last_name='LastName'
    )

    # Donner l'accès à l'administration si nécessaire
    user.is_staff = True  # Donne accès à l'administration
    user.save()
    print(f"Utilisateur créé : {user.username}")
except Exception as e:
    print(f"Erreur lors de la création de l'utilisateur : {e}")

# Authentifier l'utilisateur
user = authenticate(username='new_user', password='password123')
if user is not None:
    print(f"Connexion réussie : {user.username}")
else:
    print("Nom d'utilisateur ou mot de passe incorrect.")



"""

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Patient', 'Patient'),
        ('Gynecologue', 'Gynecologue'),
        ('Administrateur', 'Administrateur'),
        ('Secretaire', 'Secretaire'),
        ('Infirmier', 'Infirmier'),
        ('TechnicienLaboratoire', 'TechnicienLaboratoire'),  # Correction ici
        ('Pharmacien', 'Pharmacien'),
        ('TechnicienEchographe', 'TechnicienEchographe'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=22, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    nom = models.CharField(max_length=255, default='Inconnu')
    prenom = models.CharField(max_length=255, default='Inconnu')
    annee_naissance = models.DateField()
    antecedents_medicals = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.nom}"

class Gynecologue(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialiste = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    nom = models.CharField(max_length=255, default='Inconnu')
    prenom = models.CharField(max_length=255, default='Inconnu')
    email = models.EmailField()


class Administrateur(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    office_number = models.CharField(max_length=20)


class Secretaire(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, default='Inconnu')
    prenom = models.CharField(max_length=255, default='Inconnu')
    poste = models.CharField(max_length=255)


class TechnicienEchographe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, default='Inconnu')
    prenom = models.CharField(max_length=255, default='Inconnu')
    specialiste = models.CharField(max_length=100)


class Pharmacien(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255, default='Inconnu')
    prenom = models.CharField(max_length=255, default='Inconnu')
    specialiste = models.CharField(max_length=100)


class TechnicienLaboratoire(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    specialiste = models.CharField(max_length=100)


class Infirmier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    poste = models.CharField(max_length=100)


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    gynecologue = models.ForeignKey(Gynecologue, on_delete=models.SET_NULL, null=True, blank=True)
    pharmacien = models.ForeignKey(Pharmacien, on_delete=models.SET_NULL, null=True, blank=True)
    technicienLaboratoire = models.ForeignKey(TechnicienLaboratoire, on_delete=models.SET_NULL, null=True, blank=True)
    technicienEchographe = models.ForeignKey(TechnicienEchographe, on_delete=models.SET_NULL, null=True, blank=True)
    medicament = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    duration = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return f'Prescription pour {self.patient.nom} {self.patient.prenom} - {self.medicament}'
    
    
class Analyse(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    gynecologue = models.ForeignKey(Gynecologue, on_delete=models.SET_NULL, null=True, blank=True)
    pharmacien = models.ForeignKey(Pharmacien, on_delete=models.SET_NULL, null=True, blank=True)
    technicienLaboratoire = models.ForeignKey(TechnicienLaboratoire, on_delete=models.SET_NULL, null=True, blank=True)
    technicienEchographe = models.ForeignKey(TechnicienEchographe, on_delete=models.SET_NULL, null=True, blank=True)
    analyse = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f'Analyse pour {self.patient.nom} {self.patient.prenom} - {self.analyse}'



"""

class DossierMedical(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    gynecologue = models.ForeignKey(Gynecologue, on_delete=models.CASCADE)
    secretaire = models.ForeignKey(Secretaire, on_delete=models.SET_NULL, null=True, blank=True)
    infirmier = models.ForeignKey('Infirmier', on_delete=models.SET_NULL, null=True, blank=True)
    prescriptions = models.ManyToManyField(Prescription)
    type = models.CharField(max_length=100)  # Ajoutez ce champ si nécessaire
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Dossier Médical"
        verbose_name_plural = "Dossiers Médicaux"

    def __str__(self):
        return f"Dossier médical de {self.patient.nom} {self.patient.prenom}"
    
    
    """

class DossierMedical(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    gynecologue = models.ForeignKey(Gynecologue, on_delete=models.CASCADE)
    secretaire = models.ForeignKey(Secretaire, on_delete=models.SET_NULL, null=True, blank=True)
    infirmier = models.ForeignKey('Infirmier', on_delete=models.SET_NULL, null=True, blank=True)
    prescriptions = models.ManyToManyField(Prescription)
    date_creation = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=100)
    analyse = models.ManyToManyField(Analyse)

    class Meta:
        verbose_name = "Dossier Médical"
        verbose_name_plural = "Dossiers Médicaux"

    def __str__(self):
        return f"Dossier médical de {self.patient.nom} {self.patient.prenom}"


class Echographie(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    technicien_echographe = models.ForeignKey(TechnicienEchographe, on_delete=models.SET_NULL, null=True, blank=True)
    date_echographie = models.DateField(auto_now_add=True)
    type_echographie = models.CharField(max_length=255, null=True, blank=True)
    dossier_medical = models.ForeignKey(DossierMedical, on_delete=models.CASCADE)
    resultat = models.CharField(max_length=255)

    def __str__(self):
        return f'Échographie pour {self.patient.nom} {self.patient.prenom} le {self.date}'

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    gynecologue = models.ForeignKey(Gynecologue, on_delete=models.SET_NULL, null=True, blank=True)
    secretaire = models.ForeignKey(Secretaire, on_delete=models.SET_NULL, null=True, blank=True)
    infirmier = models.ForeignKey(Infirmier, on_delete=models.SET_NULL, null=True, blank=True)
    date_rendezvous = models.DateTimeField() 
    status = models.CharField(max_length=20, choices=[('Confirme', 'Confirme'), ('Annule', 'Annule')])

    def __str__(self):
        return f'Rendez-vous le {self.date_rendezvous} avec {self.patient.nom} {self.patient.prenom}'

class AnnulerRendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    gynecologue = models.ForeignKey(Gynecologue, on_delete=models.SET_NULL, null=True)
    secretaire = models.ForeignKey(Secretaire, on_delete=models.SET_NULL, null=True)
    rendezvous = models.ForeignKey(RendezVous, on_delete=models.SET_NULL, null=True)
    infirmier = models.ForeignKey(Infirmier, on_delete=models.SET_NULL, null=True)
    raison_annulation = models.TextField()
    date_annulation = models.DateTimeField()


class HistoriqueMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    dossier_medical = models.ForeignKey(DossierMedical, on_delete=models.SET_NULL, null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    details = models.TextField()

    def __str__(self):
        return f'Historique pour {self.patient} de {self.date_debut} à {self.date_fin}'


def envoyer_notification_rendezvous(rendezvous):
    subject = 'Rappel de Rendez-vous'
    message = f"Bonjour {rendezvous.patient.nom},\n\nVotre rendez-vous avec {rendezvous.medecin.nom} est prévu pour le {rendezvous.date_rendezvous}.\n\nCordialement,\nL'équipe de l'hôpital."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [rendezvous.patient.email])

