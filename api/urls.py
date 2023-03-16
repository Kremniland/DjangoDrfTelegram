from django.urls import path
from rest_framework import routers

from api.views.views_bot import UserTgView, MessageView


router = routers.SimpleRouter()
router.register(r'user_tg', UserTgView)

app_name = 'api'

urlpatterns = [
    path('message/<int:pk>/', MessageView.as_view()),
    path('message/', MessageView.as_view()),
]

urlpatterns += router.urls

