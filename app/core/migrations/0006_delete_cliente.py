# Generated by Django 5.0.2 on 2024-04-29 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_cliente_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cliente',
        ),
    ]
