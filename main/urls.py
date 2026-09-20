from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('api/quiz-lead/', views.submit_quiz_lead, name='quiz_lead'),
    path('api/sample-box/', views.submit_sample_box, name='sample_box'),
]
