from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from .models import Status


class StatusesListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses_list"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = "statuses/status_form.html"
    fields = ["name"]
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан.")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = "statuses/status_form.html"
    fields = ["name"]
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно обновлен.")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/status_confirm_delete.html"
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно удален.")
        return super().form_valid(form)
