from django.urls import path

from .views import DeleteUserView, UpdateProfileView, CreateView, UserListView

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>/update/", UpdateProfileView.as_view(), name="update_user"),
    path("<int:pk>/delete/", DeleteUserView.as_view(), name="delete_user"),
    path("create/", CreateView.as_view(), name="create"),
]