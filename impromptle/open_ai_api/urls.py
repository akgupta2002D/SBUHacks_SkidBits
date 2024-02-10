from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.openai_form, name='openai_ask'),
]
