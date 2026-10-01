from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("color/<int:pk>/", views.color, name="color"),
    path("combinations/", views.combinations, name="combinations"),
]
