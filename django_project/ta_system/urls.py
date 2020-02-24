from django.urls import path
from . import views

app_name = 'ta_system'
urlpatterns = [
    path('', views.home, name='home')
]
