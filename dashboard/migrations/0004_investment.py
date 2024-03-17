# Generated by Django 5.0.3 on 2024-03-13 11:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_proof'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('basic', 'Basic Plan'), ('standard', 'Standard Plan'), ('professionl', 'Professional Plan'), ('expert', 'Expert Plan'), ('executive', 'Executice Plan')], max_length=255)),
                ('asset', models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT', 'USDT'), ('LTC', 'Litecoin'), ('USDC', 'USDC'), ('DOGE', 'Dogecoin')], max_length=255)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]