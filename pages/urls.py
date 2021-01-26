from django.urls import path
from .views import HomePage, Dashboard


urlpatterns = [
    path('', HomePage.as_view(), name="home"),
    path('dashboard/', Dashboard.as_view(), name="dashboard")
]