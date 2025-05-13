from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.forms import StatusForm
from task_manager.mixins import DeleteViewContextMixin

from .models import Status


class StatusesListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses_list"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = "statuses/status_form.html"
    form_class = StatusForm
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, _("Status is successfully created"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = "statuses/status_form.html"
    fields = ["name"]
    success_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        messages.success(self.request, _("Status is successfully changed"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteViewContextMixin, DeleteView):
    model = Status
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("statuses_list")
    title = _("Remove a status")
    cancel_url = reverse_lazy("statuses_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, _("Status is successfully deleted"))
            return response
        except ProtectedError:
            messages.error(
                self.request,
                _("Can't delete status because it's in use")
            )
            return redirect(self.success_url)
