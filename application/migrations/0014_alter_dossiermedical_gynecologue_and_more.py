# Generated by Django 4.2.4 on 2024-11-04 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_alter_dossiermedical_gynecologue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossiermedical',
            name='gynecologue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='application.gynecologue'),
        ),
        migrations.AlterField(
            model_name='dossiermedical',
            name='type',
            field=models.CharField(max_length=100),
        ),
    ]
