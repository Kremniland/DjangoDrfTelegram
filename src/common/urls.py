from django.urls import path

from src.common.views.views import UserLoginView, UserRegistrationView, UserUpdateView, EmailVerificationView


app_name = 'common'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='verify'),
]
