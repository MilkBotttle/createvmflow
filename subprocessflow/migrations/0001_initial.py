# Generated by Django 2.0.2 on 2018-02-13 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viewflow', '0007_subprocess_subprocesstask'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('text', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='MainTask',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Task')),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.task',),
        ),
        migrations.CreateModel(
            name='SubP',
            fields=[
                ('subprocess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.SubProcess')),
                ('text', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.subprocess',),
        ),
        migrations.CreateModel(
            name='SubT',
            fields=[
                ('subprocesstask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.SubProcessTask')),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.subprocesstask',),
        ),
    ]