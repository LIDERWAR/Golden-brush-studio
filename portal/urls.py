from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_dashboard, name='dashboard'),
    path('login/', views.portal_login, name='login'),
    path('logout/', views.portal_logout, name='logout'),
]
