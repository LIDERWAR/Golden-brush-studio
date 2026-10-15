from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_dashboard, name='dashboard'),
    path('profile/', views.portal_profile, name='profile'),
    path('login/', views.portal_login, name='login'),
    path('register/', views.portal_register, name='register'),
    path('logout/', views.portal_logout, name='logout'),
]
