from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserViewsTestCase(TestCase):
    fixtures = ["task_manager/apps/user/tests/fixtures/user_test.json"]

    def setUp(self):
        self.user = User.objects.get(username="test_fixture_user")
        
    def test_user_list_view(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_list.html")

    def test_create_view(self):
        response = self.client.post(
            reverse("create"),
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "password1": "TestPass123!",
                "password2": "TestPass123!"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_edit_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("update_user", kwargs={"pk": self.user.pk}),
            {
                "username": "updateduser",
                "first_name": "Updated",
                "last_name": "User"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")

    def test_delete_user_view(self):
        self.client.force_login(self.user)
        url = reverse("delete_user", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
