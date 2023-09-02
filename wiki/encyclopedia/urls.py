from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit"),
    path("edit_2/<str:title>", views.edit_2, name="edit_2"),
    path("random", views.random, name="random")
]
