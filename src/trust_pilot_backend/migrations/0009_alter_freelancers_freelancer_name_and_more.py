# Generated by Django 5.1 on 2024-08-13 23:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trust_pilot_backend', '0008_rename_freelancer_freelancers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancers',
            name='freelancer_name',
            field=models.CharField(default='', max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='freelancer',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='trust_pilot_backend.freelancers'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='trust_pilot_backend.users'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(default='', max_length=70, unique=True),
        ),
    ]
