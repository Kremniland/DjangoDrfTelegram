from django.urls import path

from src.users.views.users import RegistrationView


app_name = 'users'

urlpatterns = [
    path('users/reg/', RegistrationView.as_view(), name='reg'),
]