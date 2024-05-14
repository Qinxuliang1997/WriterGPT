from django.urls import path
from .views import GenerateView
from .views import ModifyView

urlpatterns = [
    path('ask/', GenerateView.as_view(), name='generate_view'),
    path('modify/', ModifyView.as_view(), name='modify_view'),
]