# Generated by Django 4.0.6 on 2022-08-16 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.profile'),
        ),
    ]
