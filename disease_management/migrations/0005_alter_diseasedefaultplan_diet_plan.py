# Generated by Django 3.2 on 2023-03-02 13:17

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disease_management', '0004_auto_20230302_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasedefaultplan',
            name='diet_plan',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
