from django.urls import reverse

from task_manager.apps.labels.models import Labels
from task_manager.apps.labels.tests.fixtures.label_test import LabelFixtureMixin
from task_manager.apps.tasks.models import Task
from task_manager.forms import LabelForm



class LabelTests(LabelFixtureMixin):

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
        response = self.client.post(
            reverse("label_update", kwargs={"pk": self.label.pk}), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")

    def test_label_delete_view_get(self):
        response = self.client.get(reverse("label_delete", kwargs={"pk": self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confirm_delete.html")
        self.assertContains(response, self.label.name)

    def test_label_delete_view_post(self):
        response = self.client.post(reverse("label_delete", kwargs={"pk": self.label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertFalse(Labels.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_view_post_with_tasks(self):
        task = Task.objects.create(
            name="Test Task",
            author=self.user,
            status=self.status
        )
        task.labels.add(self.label)
        self.assertIn(self.label, task.labels.all())

        response = self.client.post(
            reverse("label_delete", kwargs={"pk": self.label.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Labels.objects.filter(pk=self.label.pk).exists())
