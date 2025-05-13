from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import CreateView, UpdateView

from task_manager.forms import LabelForm

from .models import Labels


@method_decorator(login_required, name="dispatch")
class LabelListView(View):
    def get(self, request):
        labels = Labels.objects.all()
        return render(request, 'labels/label_list.html', {'labels': labels})


@method_decorator(login_required, name="dispatch")
class LabelCreateView(CreateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("The label was created successfully."))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Label creation error. Check the data"))
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class LabelUpdateView(UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        messages.success(self.request, _("Label is successfully changed"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Label update error. Check the data"))
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class LabelDeleteView(View):
    def get(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        context = {
            "title": _("Remove a label"),
            "message": (
                _('Are you sure you want to remove') + f' "{label.name}"?'
            ),
            "cancel_url": reverse_lazy("label_list")
        }
        return render(request, "confirm_delete.html", context)

    def post(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        if label.tasks.exists():
            messages.error(
                request, _("Unable to delete a label because it is in use")
            )
            return redirect(reverse_lazy("label_list"))

        label.delete()
        messages.success(request, _("Label is successfully deleted"))
        return redirect(reverse_lazy("label_list"))
