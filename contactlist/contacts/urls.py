from django.urls import path

from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),
    path("search/", views.search, name="search"),
    path("edit/", views.pick, {"mode": "edit"}, name="pick_edit"),
    path("edit/<int:pk>/", views.edit, name="edit"),
    path("remove/", views.pick, {"mode": "remove"}, name="pick_remove"),
    path("remove/<int:pk>/", views.delete, name="delete"),
    path("exit/", views.exit_page, name="exit"),
]
