from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Maps the home view to the root URL
]
