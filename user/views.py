from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from task_manager.forms import CustomUserCreationForm, UserEditForm

User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "user_list"


@method_decorator(login_required, name="dispatch")
class EditProfileView(View):
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, "Вы не можете редактировать этот профиль.")
            return redirect(reverse_lazy("home"))
        form = UserEditForm(instance=user)
        return render(request, "users/create.html", {"form": form})

    def post(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, "Вы не можете редактировать этот профиль.")
            return redirect(reverse_lazy("home"))
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return redirect(reverse_lazy("user_list"))
        messages.error(request, "Ошибка обновления профиля. Проверьте данные.")
        return render(request, "users/create.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class DeleteUserView(View):
    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, "Вы не можете удалить этот профиль.")
            return redirect(reverse_lazy("home"))
        return render(request, "users/delete.html", {"user": user})

    def post(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        if request.user != user:
            messages.error(request, "Вы не можете удалить этот профиль.")
            return redirect(reverse_lazy("home"))
        user.delete()
        messages.success(request, "Пользователь успешно удалён.")
        return redirect(reverse_lazy("home"))


class RegisterView(FormView):
    template_name = "users/create.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегистрировались.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка регистрации. Проверьте введённые данные.")
        return self.render_to_response(self.get_context_data(form=form))
