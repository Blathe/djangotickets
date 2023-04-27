from django.urls import path

from . import views

# /reports*
urlpatterns = [
    path('', views.index, name="index"),
    path('csv', views.csv_test, name="csv"),
]
