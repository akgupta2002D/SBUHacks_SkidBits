from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("record/", views.record_page, name="record")
]
