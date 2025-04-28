from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.apps.labels.models import Labels
from task_manager.apps.statuses.models import Status

User = get_user_model()


class LabelFixtureMixin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.status = Status.objects.create(name="New")
        self.client.login(username="testuser", password="password123")
        self.label = Labels.objects.create(name="Test Label", author=self.user)
