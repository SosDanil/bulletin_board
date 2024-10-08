# Generated by Django 5.0.7 on 2024-08-02 16:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad', to=settings.AUTH_USER_MODEL, verbose_name='автор объявления'),
        ),
        migrations.AlterField(
            model_name='review',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='ads.ad', verbose_name='объявление'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='автор отзыва'),
        ),
    ]
