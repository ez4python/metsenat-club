# Generated by Django 5.1.6 on 2025-03-12 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shared', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('bachelor', 'Bakalavr'), ('master', 'Magistr')], default='bachelor', max_length=10)),
                ('full_name', models.CharField(max_length=255)),
                ('contract_amount', models.PositiveIntegerField()),
                ('donated_amount', models.PositiveIntegerField(default=0)),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='shared.university')),
            ],
            options={
                'verbose_name': 'Talaba',
                'verbose_name_plural': 'Talabalar',
                'db_table': 'students',
            },
        ),
    ]
