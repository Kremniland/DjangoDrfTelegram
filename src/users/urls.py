from django.urls import path

from src.users.views.users import RegistrationView, ChangePasswordView, MeView


app_name = 'users'

urlpatterns = [
    path('users/reg/', RegistrationView.as_view(), name='reg'),
    path('users/changepass/', ChangePasswordView.as_view(), name='changepass'),
    path('users/me/', MeView.as_view(), name='me'),

]