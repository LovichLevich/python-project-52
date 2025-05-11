from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView

from task_manager.forms import CustomUserCreationForm, UserEditForm

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "user_list"


@method_decorator(login_required, name="dispatch")
class UpdateProfileView(View):
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, _("You do not have permission to modify another user"))
            return redirect(reverse_lazy("home"))
        form = UserEditForm(instance=user)
        return render(request, "users/create.html", {"form": form, "is_create": False})

    def post(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, _("You do not have permission to modify another user"))
            return redirect(reverse_lazy("home"))
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile successfully updated"))
            return redirect(reverse_lazy("user_list"))
        messages.error(request, _("Profile update error. Check the data"))
        return render(request, "users/create.html", {"form": form, "is_create": False})


@method_decorator(login_required, name="dispatch")
class DeleteUserView(View):
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        context = {
            "title": _("Remove a user"),
            "message": _('Are you sure you want to remove') + f' "{user.username}"?',
            "cancel_url": reverse_lazy("user_list")
            }
        if request.user != user:
            messages.error(request, _("You can't delete this profile"))
            return redirect(reverse_lazy("home"))
        return render(request, "confirm_delete.html", context)

    def post(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, _("You don't have the privileges to change another user"))
            return redirect(reverse_lazy("home"))
        user.delete()
        messages.success(request, _("User successfully deleted"))
        return redirect(reverse_lazy("user_list"))


class CreateView(FormView):
    template_name = "users/create.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("You have successfully registered"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Registration error. Check the entered data"))
        return self.render_to_response(self.get_context_data(form=form))
