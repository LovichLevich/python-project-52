from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from task_manager.forms import LabelForm

from .models import Labels

User = get_user_model()


class LabelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.label = Labels.objects.create(name="Test Label", author=self.user)
    
    def test_label_list_view(self):
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_list.html")
        self.assertContains(response, "Test Label")
    
    def test_label_create_view_get(self):
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_form.html")
        self.assertIsInstance(response.context["form"], LabelForm)
    
    def test_label_create_view_post(self):
        data = {"name": "New Label"}
        response = self.client.post(reverse("label_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertTrue(Labels.objects.filter(name="New Label").exists())
    
    def test_label_update_view_get(self):
        response = self.client.get(reverse("label_update", kwargs={"pk": self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_form.html")
        self.assertContains(response, self.label.name)
    
    def test_label_update_view_post(self):
        data = {"name": "Updated Label"}
        response = self.client.post(reverse("label_update", kwargs={"pk": self.label.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")
    
    def test_label_delete_view_get(self):
        response = self.client.get(reverse("label_delete", kwargs={"pk": self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_confirm_delete.html")
        self.assertContains(response, self.label.name)
    
    def test_label_delete_view_post(self):
        response = self.client.post(reverse("label_delete", kwargs={"pk": self.label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertFalse(Labels.objects.filter(pk=self.label.pk).exists())
    
    def test_label_delete_view_post_with_tasks(self):
        Status.objects.create(name="Test Status")
        self.label.tasks.create(name="Test Task", author=self.user)
        
        response = self.client.post(reverse("label_delete", kwargs={"pk": self.label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertContains(response, "Невозможно удалить метку, которая используется в задачах.")
        self.assertTrue(Labels.objects.filter(pk=self.label.pk).exists())
