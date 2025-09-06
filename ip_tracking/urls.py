from django.urls import path
from .views import try_caching

urlpatterns = [
    path('student/', try_caching, name="try_caching"),
]