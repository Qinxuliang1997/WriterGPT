from django.urls import path
from .views import UploadView, FinishUploadView


urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('finish_upload/', FinishUploadView.as_view(), name='finish_upload'),
]