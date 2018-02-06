# Generated by Django 2.0.1 on 2018-02-06 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewflow', '0006_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatevmProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                     parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('username', models.CharField(max_length=150)),
                ('cpu_cores', models.PositiveIntegerField(default=0)),
                ('disk_size', models.PositiveIntegerField(default=0)),
                ('memory_size', models.PositiveIntegerField(default=0)),
                ('os_type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'CreateVM process list',
                'permissions': [('can_start_request', 'Can start createvm request'), ('can_assign_approver', 'Can assign approver'), ('can_approve_request', 'Can approve request')],
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='ProcessApproverAndAns',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.BooleanField(default=True)),
                ('process', models.ForeignKey(blank=True, null=True,
                                              on_delete=django.db.models.deletion.CASCADE, to='createvmflow.CreatevmProcess')),
            ],
        ),
        migrations.CreateModel(
            name='CreatvmTask',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('viewflow.task',),
        ),
        migrations.AddField(
            model_name='processapproverandans',
            name='task',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='createvmflow.CreatvmTask'),
        ),
        migrations.AddField(
            model_name='processapproverandans',
            name='user',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
