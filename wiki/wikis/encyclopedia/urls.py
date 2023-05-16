from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:contentName>", views.getContent, name="detail"),
    path("wiki/action/search-page", views.search, name="searched-content"),
    path("wiki/action/create-page", views.create_page, name="new-page"),
    path("wiki/action/edit-page/<contentName>", views.edit_article, name="edit-page"),
    path("wiki/action/edit-page/", views.index, name="edit-page-list"),
]
