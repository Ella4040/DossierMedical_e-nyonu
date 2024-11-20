from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RendezVousForm, PrescriptionForm, EchographieForm, DossierMedicalForm, AnnulerRendezVousForm, AnalyseForm, DossierMedicalForm, PatientForm
from .models import RendezVous, AnnulerRendezVous, DossierMedical, HistoriqueMedical, Profile, Patient, Prescription, Analyse, Gynecologue, Pharmacien
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from twilio.rest import Client
from django.conf import settings


@login_required
def dashboard(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    # Si l'utilisateur est un patient, récupérer ses rendez-vous
    if profile.role == 'Patient':
        try:
            patient = Patient.objects.get(user=user)
            rendezvous_list = RendezVous.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            rendezvous_list = None
            messages.error(request, "Aucun profil de patient trouvé pour cet utilisateur.")
    else:
        rendezvous_list = None

    context = {
        'role': profile.role,
        'rendezvous_list': rendezvous_list,
    }
    return render(request, 'dashboard.html', context)


@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')


@login_required
def gynecologue_dashboard(request):
    return render(request, 'gynecologue_dashboard.html')

"""
@login_required
def creer_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendezvous = form.save(commit=False)
            # Associer le rendez-vous au patient via le profil
            rendezvous.patient = request.user.profile
            rendezvous.save()
            messages.success(request, 'Votre rendez-vous a été créé avec succès.')
            return redirect('rendezvous_liste')  # Rediriger vers la liste des rendez-vous
    else:
        form = RendezVousForm()
    return render(request, 'creer_rendezvous.html', {'form': form})

"""

@login_required
def prendre_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            # Récupérer le profil utilisateur
            profile = get_object_or_404(Profile, user=request.user)

            try:
                patient = Patient.objects.get(user=profile.user)
                print("Patient trouvé:", patient)  # Ajoutez cette ligne
            except Patient.DoesNotExist:
                patient = None
                print("Aucun patient trouvé pour cet utilisateur.")  # Ajoutez cette ligne

            if patient:
                rendezvous = form.save(commit=False)
                rendezvous.patient = patient  # Associe bien le patient au rendez-vous
                rendezvous.save()
                return redirect('dashboard')
            else:
                messages.error(request, "Cet utilisateur n'est pas un patient.")
    else:
        form = RendezVousForm()

    return render(request, 'prendre_rendezvous.html', {'form': form})


@login_required
def liste_rendezvous(request):
    profile = get_object_or_404(Profile, user=request.user)
    patient = get_object_or_404(Patient, user=profile.user)

    # Récupérer la liste des rendez-vous associés à ce patient
    liste_rendezvous = RendezVous.objects.filter(patient=patient)

    return render(request, 'liste_rendezvous.html', {'liste_rendezvous': liste_rendezvous})


@login_required
def annuler_rendezvous(request, rendezvous_id):
    rendezvous = get_object_or_404(RendezVous, id=rendezvous_id, patient=request.user.profile)

    if request.method == 'POST':
        raison = request.POST.get('raison_annulation')
        annulation = AnnulerRendezVous(rendezvous=rendezvous, raison_annulation=raison)
        annulation.save()
        rendezvous.status = 'Annule'
        rendezvous.save()
        messages.success(request, 'Votre rendez-vous a été annulé.')
        return redirect('rendezvous_liste')

    return render(request, 'annuler_rendezvous.html', {'rendezvous': rendezvous})


@login_required
def consulter_historique(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    historique = HistoriqueMedical.objects.filter(patient=patient)
    return render(request, 'consulter_historique.html', {
        'patient': patient,
        'historique': historique,
    })

@login_required
def contact(request):
    return render(request, 'contact.html')


def envoyer_sms_rendezvous(rendezvous):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = f"Bonjour {rendezvous.patient.user.first_name}, votre rendez-vous avec {rendezvous.doctor.user.first_name} est prévu pour le {rendezvous.date_rendezvous}."
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=rendezvous.patient.telephone
    )

def consulter_dossier_medical(request, dossier_id):
    dossier = get_object_or_404(DossierMedical, id=dossier_id)
    return render(request, 'consulter_dossier_medical.html', {'dossier': dossier})

def rendezvous_confirmation(request):
    return render(request, 'rendezvous_confirmation.html')

def rendezvous(request):
    return render(request, 'rendezvous.html')


@login_required
def rendezvous_liste(request):
    rendezvous_list = RendezVous.objects.filter(patient=request.user.profile)
    return render(request, 'rendezvous_liste.html', {'rendezvous_list': rendezvous_list})


@login_required
def prescriptions(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Vérification du rôle de l'utilisateur pour la prescription
    if profile.role not in ['Gynecologue', 'Pharmacien']:
        return redirect('dashboard')  # Rediriger si l'utilisateur n'a pas le bon rôle

    gynecologue_instance = None
    pharmacien_instance = None

    if profile.role == 'Gynecologue':
        gynecologue_instance = get_object_or_404(Gynecologue, user=profile.user)
    elif profile.role == 'Pharmacien':
        try:
            pharmacien_instance = Pharmacien.objects.get(user=profile.user)
        except Pharmacien.DoesNotExist:
            messages.error(request, "Aucun pharmacien associé à cet utilisateur.")
            return redirect('dashboard')  # Ou rediriger vers une autre page

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            # Associer le gynécologue ou pharmacien selon le rôle
            if profile.role == 'Gynecologue':
                prescription.gynecologue = gynecologue_instance
            elif profile.role == 'Pharmacien':
                prescription.pharmacien = pharmacien_instance

            prescription.save()
            return redirect('dashboard')
        else:
            form.add_error(None, "Le formulaire contient des erreurs.")
    else:
        form = PrescriptionForm()

    # Afficher les prescriptions déjà faites par l'utilisateur
    prescriptions_list = Prescription.objects.filter(
        gynecologue=gynecologue_instance) if profile.role == 'Gynecologue' else Prescription.objects.filter(pharmacien=pharmacien_instance)

    return render(request, 'prescriptions.html', {
        'form': form,
        'prescriptions': prescriptions_list,
    })

def analyse(request):
    if request.method == 'POST':
        form = AnalyseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('analyse.html')  # Remplacez par le nom de la vue ou l'URL de redirection
    else:
        form = AnalyseForm()
    
    analyses = Analyse.objects.all()  # Récupérer toutes les analyses pour affichage
    context = {
        'form': form,
        'analyses': analyses,
    }
    return render(request, 'analyse.html', context)


@login_required
def echographie(request):
    return render(request, 'echographie.html')


@login_required
def echographie_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Vérifier si l'utilisateur est un technicien d'échographie
    if profile.role != 'TechnicienEchographe':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EchographieForm(request.POST)
        if form.is_valid():
            echographie = form.save(commit=False)
            echographie.technicien_echographe = profile.user
            echographie.save()
            messages.success(request, "L'échographie a été enregistrée avec succès.")
            return redirect('dashboard')
    else:
        form = EchographieForm()

    return render(request, 'echographie.html', {'form': form})


def creer_dossier(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        dossier_form = DossierMedicalForm(request.POST)
        
        if patient_form.is_valid() and dossier_form.is_valid():
            # Créer l'utilisateur
            username = patient_form.cleaned_data.get('email')  # Par exemple, utilisez l'email comme nom d'utilisateur
            password = 'defaultpassword'  # Vous pouvez générer un mot de passe ou demander à l'utilisateur
            user = User.objects.create_user(username=username, password=password)
            
            # Enregistrez le patient
            patient = patient_form.save(commit=False)
            patient.user = user  # Associez l'utilisateur au patient
            patient.save()

            # Créez le dossier médical
            dossier = dossier_form.save(commit=False)
            dossier.patient = patient  # Associez le dossier au patient
            dossier.save()

            return redirect('consulter_dossier_medical', dossier_id=dossier.id)
    else:
        patient_form = PatientForm()
        dossier_form = DossierMedicalForm()
    
    return render(request, 'creer_dossier.html', {
        'patient_form': patient_form,
        'dossier_form': dossier_form,
    })