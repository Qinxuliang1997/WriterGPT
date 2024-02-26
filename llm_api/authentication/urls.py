from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('register/', views.UserCreate.as_view(), name='user_register'),
]