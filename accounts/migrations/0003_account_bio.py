# Generated by Django 2.1.1 on 2019-03-09 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190128_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio',
            field=models.TextField(default='I am an account'),
            preserve_default=False,
        ),
    ]