# Generated by Django 3.2 on 2023-03-03 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_patientmedicalhistory_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fcm_token',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
