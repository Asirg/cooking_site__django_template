# Generated by Django 4.0.6 on 2022-09-01 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nyamki', '0014_category_for_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='for_article',
            field=models.BooleanField(verbose_name='Для статей'),
        ),
    ]
