from django.urls import path
from . import views


app_name = "manipulador"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:archive_num>/<str:archive_name>", views.show_json, name="show_json"),
    path("edit/<int:archive_num>/<str:archive_name>", views.edit_json, name="edit_json"),
    path("create", views.create_json, name="create_json"),
    path("append/<str:archive_name>", views.append_json, name="append_json"),
    path("download/<str:archive_name>", views.download_json, name="download_json"),
    path("delete/<str:archive_name>", views.delete_json, name="delete_json")
]