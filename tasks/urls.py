from django.urls import path

from tasks.views import (
    TaskCreateView,
    TaskDeleteView,
    TasksView,
    TaskUpdateView,
    TaskView,
)

urlpatterns = [
    path('', TasksView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='task_form'),
    path('<int:pk>/', TaskView.as_view(), name='task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
