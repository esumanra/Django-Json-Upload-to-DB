from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_json, name="upload"),
    path("info/", views.InfoView.as_view(), name="info"),
    path("login", views.login, name="login"),
]
