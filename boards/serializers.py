from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import transaction
from django.urls import Resolver404
from django.urls.base import resolve, reverse
from django.utils.module_loading import import_string
from rest_framework import serializers
from rest_framework.fields import Field
from users.models import User
from users.serializers import UserSerializer

from .models import Task, Notification
from .utils import send_email


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'order', 'id')

    @transaction.atomic
    def create(self, validated_data):
        task = Task.objects.create(
            **validated_data
        )
        status = validated_data.get('status')
        email = task.assigned_to.email
        if status:
            send_email("Change Status", f"Change status to {status}", [email])

        return task


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['__all__']
