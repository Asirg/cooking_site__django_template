# Generated by Django 4.0.6 on 2022-09-01 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nyamki', '0012_remove_article_content_af_remove_article_content_ar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='description_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
