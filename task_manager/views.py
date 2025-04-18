from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _
from task_manager.forms import UserLoginForm
from django.contrib.auth.views import LogoutView

class HomePageView(TemplateView):
    template_name = "home.html"

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, _("You are logged in"))
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)

