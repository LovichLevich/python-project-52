from django.urls import path
from tasks.views import (
    TasksView, TaskCreateView, TaskView, TaskUpdateView, TaskDeleteView
)

urlpatterns = [
    path('', TasksView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='task_form'),
    path('<int:pk>/', TaskView.as_view(), name='task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
