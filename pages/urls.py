from django.urls import path
from .views import login_view, callback_view, playlist_view

app_name = 'pages'

urlpatterns = [
    path('', login_view),
    path('login', login_view),
    path('callback/<str:pk>', callback_view, name='callback'),
    path('playlist/<str:id>', playlist_view, name='playlist')
]