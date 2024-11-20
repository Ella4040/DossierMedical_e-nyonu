from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    # path('creer-rendezvous/', views.creer_rendezvous, name='creer_rendezvous'),
    path('annuler-rendezvous/<int:rendezvous_id>/', views.annuler_rendezvous, name='annuler_rendezvous'),
    path('prendre-rendezvous/', views.prendre_rendezvous, name='prendre_rendezvous'),
    path('liste-rendezvous/', views.liste_rendezvous, name='liste_rendezvous'),
    path('consulter_dossier_medical/<int:dossier_id>/', views.consulter_dossier_medical, name='consulter_dossier_medical'),
    # path('gestion-rendezvous/', views.creer_rendezvous, name='gestion_rendezvous'),
    path('rendezvous/', views.rendezvous, name='rendezvous'),
    path('confirmation-rendezvous/', views.rendezvous_confirmation, name='rendezvous_confirmation'),
    path('consulter-historique/<int:patient_id>/', views.consulter_historique, name='consulter_historique'),
    path('creer-dossier/', views.creer_dossier, name='creer_dossier'),
    path('rendezvous-liste/', views.rendezvous_liste, name='rendezvous_liste'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('analyse/', views.analyse, name='analyse'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('echographie/', views.echographie, name='echographie'),
]
