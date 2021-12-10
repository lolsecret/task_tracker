from django.urls import path, include
from .views import TaskList, TaskDetailView


urlpatterns = [
    path('task/', TaskList.as_view()),
    path('task/<int:task_id>/', TaskDetailView.as_view({'get': 'retrieve', 'put': 'update'}),  name='trip-detail'),
]
