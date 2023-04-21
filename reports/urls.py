from django.urls import path

from . import views

# /reports*
urlpatterns = [
    path('', views.index, name="index"),
]
