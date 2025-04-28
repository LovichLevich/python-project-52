from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.forms import LabelForm

from .models import Labels


@method_decorator(login_required, name="dispatch")
class LabelListView(View):
    def get(self, request):
        labels = Labels.objects.all()
        return render(request, 'labels/label_list.html', {'labels': labels})


@method_decorator(login_required, name="dispatch")
class LabelCreateView(View):
    def get(self, request):
        form = LabelForm()
        return render(request, 'labels/label_form.html', {'form': form})

    def post(self, request):
        form = LabelForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.author = request.user
            label.save()
            messages.success(request, _("The label was created successfully."))
            return redirect(reverse_lazy('label_list'))
        return render(request, 'labels/label_form.html', {'form': form})


@method_decorator(login_required, name="dispatch")
class LabelUpdateView(View):
    def get(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        form = LabelForm(instance=label)
        return render(request, 'labels/label_form.html', {'form': form})

    def post(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _("Label is successfully changed"))
            return redirect(reverse_lazy('label_list'))
        return render(request, 'labels/label_form.html', {'form': form})


@method_decorator(login_required, name="dispatch")
class LabelDeleteView(View):
    def get(self, request, pk):
        label = get_object_or_404(Labels, pk=pk)
        context = {
            "title": _("Remove a label"),
            "message": _('Are you sure you want to remove') + f' "{label.name}"?',
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
