from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max
from django.utils import timezone

from boards import TaskStatusTypes
from users.models import User


class Task(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    order = models.DecimalField(max_digits=30,decimal_places=15, blank=True, null=True)
    spectators = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True, related_name="tasks")
    assigned_to = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    planned_due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        choices=TaskStatusTypes.choices,
        default=TaskStatusTypes.PLANNED
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.id
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

class ChangeStatus(models.Model):
    prev_status = models.CharField(max_length=255, blank=False, null=False, choices=TaskStatusTypes.choices)
    next_status =models.CharField(max_length=255, blank=False, null=False, choices=TaskStatusTypes.choices)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='change_statuses')
    by_changed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='change_statuses')

    def __str__(self):
        return self.task, self.by_changed

    class Meta:
        verbose_name = "Изменение статуса"
        verbose_name_plural = "Изменения статуса"


class Notification(models.Model):
    recipient = models.ManyToManyField(
        User, related_name='notifications')
    text = models.CharField(max_length=255, blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"