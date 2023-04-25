from django.urls import path

from . import views

# /reports*
urlpatterns = [
    path('', views.index, name="index"),
    path('test', views.csv_test, name="csv"),
]
