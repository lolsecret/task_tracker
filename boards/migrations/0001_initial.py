# Generated by Django 4.0 on 2021-12-10 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('order', models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('planned_due_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PLANNED', 'Планируется'), ('ACTIVE', 'Активная'), ('CONTROL', 'Контроль'), ('COMPLETED', 'Завершена')], default='PLANNED', max_length=25)),
                ('assigned_to', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                ('spectators', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='users.user')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('recipient', models.ManyToManyField(related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='boards.task')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
        migrations.CreateModel(
            name='ChangeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_status', models.CharField(choices=[('PLANNED', 'Планируется'), ('ACTIVE', 'Активная'), ('CONTROL', 'Контроль'), ('COMPLETED', 'Завершена')], max_length=255)),
                ('next_status', models.CharField(choices=[('PLANNED', 'Планируется'), ('ACTIVE', 'Активная'), ('CONTROL', 'Контроль'), ('COMPLETED', 'Завершена')], max_length=255)),
                ('by_changed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_statuses', to='users.user')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_statuses', to='boards.task')),
            ],
            options={
                'verbose_name': 'Изменение статуса',
                'verbose_name_plural': 'Изменения статуса',
            },
        ),
    ]