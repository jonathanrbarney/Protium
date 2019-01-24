# Generated by Django 2.1.1 on 2019-01-24 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AMI',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cadet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='amis', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PAI',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cadet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pais', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('is_cadet_job', models.BooleanField(default=True)),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ManyToManyField(blank=True, related_name='_position_supervisor_+', to='military.Position')),
            ],
        ),
        migrations.CreateModel(
            name='SAMI',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cadet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aamis', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('commanders', models.ManyToManyField(related_name='units_commanded', to='military.Position')),
                ('members', models.ManyToManyField(related_name='units', to=settings.AUTH_USER_MODEL)),
                ('positions', models.ManyToManyField(related_name='units', to='military.Position')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='military.Unit'),
        ),
    ]
