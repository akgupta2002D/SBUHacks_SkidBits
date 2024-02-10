from django.urls import path
from .views import record_video

urlpatterns = [
    path('record/', record_video, name='record_video'),
]