# Generated by Django 2.1.1 on 2018-10-22 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sections_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='instructor',
            field=models.ManyToManyField(related_name='section_instructed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='period',
            field=models.ManyToManyField(related_name='sections', to='academics.Period'),
        ),
        migrations.AddField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(through='academics.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='section',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='academics.Term'),
        ),
        migrations.AddField(
            model_name='program',
            name='cadets',
            field=models.ManyToManyField(related_name='programs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='program',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.Department'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enrollments', to='academics.Section'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='admins',
            field=models.ManyToManyField(related_name='department_faculty', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='instructors',
            field=models.ManyToManyField(related_name='department_instructor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course_requirement',
            name='courses_satisfy',
            field=models.ManyToManyField(related_name='requirements_satisfied', to='academics.Course'),
        ),
        migrations.AddField(
            model_name='course_requirement',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.Program'),
        ),
        migrations.AddField(
            model_name='course',
            name='admins',
            field=models.ManyToManyField(related_name='managed_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='coerequisites',
            field=models.ManyToManyField(blank=True, related_name='coerequisite_of', to='academics.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(related_name='instructed_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, related_name='prerequisite_for', to='academics.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='terms_offered',
            field=models.ManyToManyField(blank=True, related_name='courses', to='academics.Term'),
        ),
    ]
