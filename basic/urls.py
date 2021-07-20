from django.urls import path
from .views import CustomLogoutView, CustomLoginView, UserRegistration, main

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', main, name='start-page')
]
