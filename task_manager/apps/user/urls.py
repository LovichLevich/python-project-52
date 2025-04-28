from django.urls import path

from .views import DeleteUserView, EditProfileView, RegisterView, UserListView

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>/update/", EditProfileView.as_view(), name="update_user"),
    path("<int:pk>/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("register/", RegisterView.as_view(), name="register"),
]