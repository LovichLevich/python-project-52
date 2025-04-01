from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tasks.models import Task
from django.shortcuts import render
from user.models import User
from statuses.models import Status
from django.contrib import messages
from django.shortcuts import redirect

class TasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()
        status_id = self.request.GET.get('status')
        executor_id = self.request.GET.get('executor')
        self_tasks = self.request.GET.get('self_tasks') == "on"

        print(f"self_tasks: {self_tasks}, user: {self.request.user}")

        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        if self_tasks and self.request.user.is_authenticated:
            queryset = queryset.filter(author_id=self.request.user.id)

        print(queryset.query)
        print(list(queryset))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        return context



class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'executor', 'status']
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'executor', 'status']
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно обновлена.")
        return super().form_valid(form)



class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author
    
    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор.")
        return redirect('tasks_list')
