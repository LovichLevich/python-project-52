from django.urls import reverse

from task_manager.apps.tasks.models import Task
from task_manager.apps.tasks.tests.fixtures.task_test import TaskTestFixture


class TaskTests(TaskTestFixture):

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
        url = reverse('task_update', args=[self.task.id])
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'executor': self.user.id,
            'status': self.status.id,
        }
        response = self.client.post(url, data)
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
