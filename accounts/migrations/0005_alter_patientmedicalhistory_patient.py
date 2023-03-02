# Generated by Django 3.2 on 2023-03-02 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20230302_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmedicalhistory',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_history', to=settings.AUTH_USER_MODEL),
        ),
    ]
