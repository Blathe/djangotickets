from django.urls import path

from . import views

# /tickets/*
urlpatterns = [
    path('details/<int:pk>', views.details, name="details"),
    path('create/', views.create, name="create"),
    path('delete/<int:pk>', views.delete, name="delete"),
    path('close/<int:pk>', views.close, name="close"),
    #this should probably be moved into a Comments app instead of going through tickets.
    path('comment/<int:pk>', views.comment, name="comment"),
]
