# Generated by Django 4.0.6 on 2022-08-13 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nyamki', '0004_alter_article_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookingingredient',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание'),
        ),
    ]
