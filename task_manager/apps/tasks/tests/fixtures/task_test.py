from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.apps.statuses.models import Status
from task_manager.apps.tasks.models import Task

User = get_user_model()


class TaskTestFixture(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.another_user = User.objects.create_user(username='anotheruser', password='testpassword')

        self.status = Status.objects.create(name='In Progress')

        self.task = Task.objects.create(
            name="Test Task",
            description="Test Task Description",
            executor=self.user,
            status=self.status,
            author=self.user
        )

        self.client.login(username='testuser', password='testpassword')
