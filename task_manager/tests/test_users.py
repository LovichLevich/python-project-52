from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTestCase(TestCase):
    fixtures = ["user/fixtures/test_user.json"]

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1user",
            first_name="Test",
            last_name="User",
            password="testpassword"
        )

    def test_user_list_view(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_list.html")

    def test_register_view(self):
        response = self.client.post(
            reverse("register"),
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
        response = self.client.post(reverse("delete_user", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
