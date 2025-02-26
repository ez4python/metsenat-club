# Generated by Django 5.1.6 on 2025-02-25 09:19

import apps.shared.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'Yangi'), ('moderation', 'Moderatsiyada'), ('approved', 'Tasdiqlangan'), ('canceled', 'Bekor qilingan')], default='new', max_length=20)),
                ('sponsor_type', models.CharField(choices=[('legal', 'Jismoniy shaxs'), ('individual', 'Yuridik shaxs')], default='individual', max_length=10)),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20, unique=True, validators=[apps.shared.validators.validate_phone_number])),
                ('organization_name', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000000)])),
                ('payment_type', models.CharField(choices=[('cash', 'Naqd pul'), ('card', 'Plastik karta'), ('transfer', "Pul o'tkazmasi")], default='transfer', max_length=20)),
                ('spent_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Homiy',
                'verbose_name_plural': 'Homiylar',
                'db_table': 'sponsors',
            },
        ),
    ]
