from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.apps.labels.models import Labels
from task_manager.apps.statuses.models import Status
from task_manager.apps.tasks.models import Task

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
            'autocapitalize': 'none',
            'autocomplete': 'username'}),
        required=True
    )

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'autocomplete': 'current-password'}),
        required=True
    )


class UserEditForm(forms.ModelForm):
    password1_field = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True
    )
    password2_field = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "username", 
            "password1", 
            "password2"
        ]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'executor', 'status', 'labels']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'executor': forms.Select(attrs={'class': 'form-select'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = User.objects.all()
        self.fields['executor'].label_from_instance = (
            lambda obj: obj.get_full_name()
        )
        self.fields['labels'].queryset = Labels.objects.all()


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': _('Name'), }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            }),
        }
        

class LabelForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ['name']
        labels = {'name': _('Name'), }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            })
        }