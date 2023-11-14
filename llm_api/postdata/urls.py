from django.urls import path
from postdata import views


urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('finish_upload/', views.finish_upload, name='finish_upload'),
    path('delete_all_files', views.delete_all_files, name='delete_all_files'),
]