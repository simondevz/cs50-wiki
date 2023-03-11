from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("wiki/", views.search, name="search"),
    path("wiki/<str:title>", views.content, name="content")
]
