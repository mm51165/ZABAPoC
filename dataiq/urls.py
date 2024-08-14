from django.urls import path

from .views import ChunkSearchAPIView

urlpatterns = [
    path("search/", ChunkSearchAPIView.as_view(), name="detail"),
]
