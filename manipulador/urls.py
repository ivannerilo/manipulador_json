from django.urls import path
from . import views


app_name = "manipulador"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:archive_num>", views.show_json, name="show_json"),
    path("edit/<int:archive_num>", views.edit_json, name="edit_json")
]