from django.urls import reverse

from task_manager.apps.statuses.models import Status
from task_manager.apps.statuses.tests.fixtures.status_test import (
    StatusFixtureMixin,
)


class StatusCRUDTests(StatusFixtureMixin):

    def test_status_create_view(self):
        response = self.client.post(reverse("create_status"), {
            "name": "New Status"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name="New Status").exists())

    def test_status_update_view(self):
        response = self.client.post(
            reverse("update_status", args=[self.status.id]), {
                "name": "Updated Status"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

    def test_status_delete_view(self):
        url = reverse("delete_status", kwargs={"pk": self.label.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_status_delete_protected(self):
        url = reverse("delete_status", kwargs={"pk": self.label.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
