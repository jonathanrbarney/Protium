# Generated by Django 2.1.1 on 2019-01-17 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='period_slot',
            old_name='cas',
            new_name='schedule',
        ),
    ]