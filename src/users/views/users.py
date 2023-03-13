from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from src.users.serializers.api.users import RegistrationSerializer


User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Регистрация', tags=['Аутентификация и регистрация']),
)
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer



