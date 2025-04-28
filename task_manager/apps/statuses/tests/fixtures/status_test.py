from django.contrib.auth import get_user_model
from django.test import TestCase
from task_manager.apps.statuses.models import Status

User = get_user_model()


class StatusFixtureMixin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)
        self.status = Status.objects.create(name="Test Status")
