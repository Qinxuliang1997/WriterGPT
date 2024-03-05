from django.urls import path
from .views import GenerateView

urlpatterns = [
    path('ask/', GenerateView.as_view(), name='generate_view'),
]