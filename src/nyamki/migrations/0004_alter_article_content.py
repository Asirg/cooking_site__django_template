# Generated by Django 4.0.6 on 2022-08-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nyamki', '0003_alter_article_date_alter_article_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Контент'),
        ),
    ]