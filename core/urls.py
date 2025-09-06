from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("player/", views.video_player, name="video_player"),
    path("video/<int:pk>/", views.video_detail, name="video_detail"),
]
