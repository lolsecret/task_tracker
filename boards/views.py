from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, Q, When
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, Notification
from .permissions import CanViewTasks, IsAuthorOrReadOnly
from .serializers import (NotificationSerializer,
                          TaskSerializer)


class TaskList(ListAPIView):

    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Task.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        pk = self.kwargs.get('pk')
        item = get_object_or_404(Task, pk=pk)
        return item


class TaskDetailView(viewsets.ReadOnlyModelViewSet, UpdateModelMixin):
    lookup_field = 'id'
    lookup_url_kwarg = 'task_id'
    permission_classes = (permissions.AllowAny,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class NotificationList(APIView):
    def get(self, *args, **kwargs):
        notifications = Notification.objects.filter(
            recipient=self.request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):  # Mark all as read
        Notification.objects.filter(
            recipient=self.request.user, unread=True).update(unread=False)
        return Response(status=status.HTTP_204_NO_CONTENT)
