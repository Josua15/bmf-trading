from django.urls import path
from . import views
from .controllers.bmf_analysis import ohlcv_analysis_view

urlpatterns = [
    path('', views.home_view, name='home'),  # Maps the home view to the root URL
    path('ohlcv-analysis/', ohlcv_analysis_view, name='ohlcv_analysis'),
]
