# Generated by Django 4.1.2 on 2023-06-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_alter_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionrequest',
            name='demand_status',
            field=models.CharField(choices=[('en_verification', 'En vérification'), ('approuvee', 'Approuvée'), ('rejetee', 'Rejetée')], default='en_verification', max_length=50, verbose_name='Statut de la demande'),
        ),
    ]
