from django.urls import path
from . import views

app_name = 'ta_system'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('get_lab_hour_preferences/',
        views.get_lab_hour_preferences,
        name='get_lab_hour_preferences'),
    path('get_lab_hour_constraints/',
        views.get_lab_hour_constraints,
        name='get_lab_hour_constraints'),
]
