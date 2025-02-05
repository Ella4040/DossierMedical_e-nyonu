# Generated by Django 4.2.4 on 2024-09-25 22:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_alter_profile_role_alter_profile_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dossiermedical',
            options={'verbose_name': 'Dossier Médical', 'verbose_name_plural': 'Dossiers Médicaux'},
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='medecin',
        ),
        migrations.RemoveField(
            model_name='rendezvous',
            name='medecin',
        ),
        migrations.AddField(
            model_name='annulerrendezvous',
            name='gynecologue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.gynecologue'),
        ),
        migrations.AddField(
            model_name='annulerrendezvous',
            name='infirmier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.infirmier'),
        ),
        migrations.AddField(
            model_name='annulerrendezvous',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.patient'),
        ),
        migrations.AddField(
            model_name='annulerrendezvous',
            name='secretaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.secretaire'),
        ),
        migrations.AddField(
            model_name='dossiermedical',
            name='date_creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='dossiermedical',
            name='infirmier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.infirmier'),
        ),
        migrations.AddField(
            model_name='dossiermedical',
            name='secretaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.secretaire'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='gynecologue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.gynecologue'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='pharmacien',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.pharmacien'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='technicienEchographe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.technicienechographe'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='technicienLaboratoire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.technicienlaboratoire'),
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='gynecologue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.gynecologue'),
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='infirmier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.infirmier'),
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='secretaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.secretaire'),
        ),
        migrations.AlterField(
            model_name='annulerrendezvous',
            name='date_annulation',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='annulerrendezvous',
            name='rendezvous',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.rendezvous'),
        ),
        migrations.AlterField(
            model_name='dossiermedical',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.patient'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.patient'),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.patient'),
        ),
        migrations.CreateModel(
            name='HistoriqueMedical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('details', models.TextField()),
                ('dossier_medical', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.dossiermedical')),
                ('patient', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.patient')),
            ],
        ),
    ]
