from django.urls import path
from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.get_data, name='homepage'),
    path('cgu', views.cgu, name='cgu'),
]
