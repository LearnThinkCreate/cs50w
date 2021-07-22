from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:TITLE>', views.wiki, name="wiki"),
    path("newPage/", views.newPage, name="newPage"),
    path("editPage/", views.edit, name="editPage"),
    path("savePage/", views.save, name="savePage")
]
