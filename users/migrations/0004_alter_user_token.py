# Generated by Django 5.0.7 on 2024-08-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='токен'),
        ),
    ]