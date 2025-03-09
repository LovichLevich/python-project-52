from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from task_manager.forms import UserLoginForm

class HomePageView(TemplateView):
    template_name = "home.html"

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"

