from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from statuses.models import Status
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskTests(TestCase):

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

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(reverse('task_form'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'executor': self.user.id,
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'executor': self.user.id,
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view(self):
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_view_permission(self):
        self.client.logout()
        self.client.login(username='anotheruser', password='testpassword')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_task_create_view_not_authenticated(self):
        self.client.logout()
        response = self.client.post(reverse('task_form'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'executor': self.user.id,
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/tasks/create/')
