from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('djoser/', include('djoser.urls.jwt')),
]
