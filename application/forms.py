# forms.py
from django import forms
from .models import RendezVous, DossierMedical, AnnulerRendezVous, Prescription, Echographie, Analyse, Patient


class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'gynecologue', 'date_rendezvous']
        
class AnnulerRendezVousForm(forms.ModelForm):
    class Meta:
        model = AnnulerRendezVous
        fields = ['patient', 'gynecologue', 'secretaire', 'rendezvous', 'infirmier']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_annulation'].disabled = True


class DossierMedicalForm(forms.ModelForm):
    class Meta:
        model = DossierMedical
        fields = ['patient', 'analyse', 'type']  # Assurez-vous que ces champs existent dans votre modèle DossierMedical
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'analyse': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'annee_naissance', 'antecedents_medicals', 'address', 'telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'annee_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'antecedents_medicals': forms.Textarea(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medicament', 'dosage', 'duration']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'medicament': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyse
        fields = ['patient', 'analyse', 'type', 'nom']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'analyse': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EchographieForm(forms.ModelForm):
    class Meta:
        model = Echographie  # Votre modèle associé
        fields = ['patient', 'type_echographie', 'resultat']
        widgets = {
            'patient': forms.Select(),
            'type_echographie': forms.Select(),
            'resultat': forms.Textarea(),
        }



