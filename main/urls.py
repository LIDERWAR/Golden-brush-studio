from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/<slug:slug>/', views.article_detail, name='journal_detail'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),  # legacy alias
    path('api/quiz-lead/', views.submit_quiz_lead, name='quiz_lead'),
    path('api/sample-box/', views.submit_sample_box, name='sample_box'),
    path('api/art-inquiry/', views.submit_art_inquiry, name='art_inquiry'),
    path('api/art-fitting/', views.submit_art_fitting, name='art_fitting'),
    path('api/calculator-lead/', views.submit_calculator_lead, name='calculator_lead'),
]

