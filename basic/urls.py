from django.urls import path
from .views import CustomLogoutView, CustomLoginView, UserRegistration, welcome_page

urlpatterns = [
    path('sign-up/', UserRegistration.as_view(), name='register'),
    path('sign-out/', CustomLogoutView.as_view(), name='logout'),
    path('sign-in/', CustomLoginView.as_view(), name='login'),
    path('welcome-page/', welcome_page, name='welcome-page')
]
