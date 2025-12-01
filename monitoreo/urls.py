from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('municipios/', views.municipios_view, name='municipios'),
    path('api/datos/', views.api_datos, name='api_datos'),
    path('exportar/',views.exportar_csv, name='exportar_csv'),
    path('register/', views.register, name='register'),

]