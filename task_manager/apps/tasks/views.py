from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.apps.labels.models import Labels
from task_manager.apps.statuses.models import Status
from task_manager.apps.tasks.models import Task
from task_manager.apps.user.models import User
from task_manager.mixins import DeleteViewContextMixin


class TasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()
        status_id = self.request.GET.get('status')
        executor_id = self.request.GET.get('executor')
        label_id = self.request.GET.get('labels')
        self_tasks = self.request.GET.get('self_tasks') == "on"

        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        if self_tasks and self.request.user.is_authenticated:
            queryset = queryset.filter(author_id=self.request.user.id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Labels.objects.all() 
        return context


class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'executor', 'status', 'labels']
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _('Task is successfully created'))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'executor', 'status', 'labels']
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, _('Task is successfully changed'))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteViewContextMixin, DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    title = _("Remove a task")
    cancel_url = reverse_lazy("tasks_list")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, _('The task can be deleted only by its author'))
        return redirect(self.success_url)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Task is successfully deleted'))
        return response