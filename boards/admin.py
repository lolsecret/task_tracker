from django.contrib import admin
from .models import Task, Notification, ChangeStatus

admin.site.register(Task)
admin.site.register(Notification)
admin.site.register(ChangeStatus)

