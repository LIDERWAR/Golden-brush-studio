from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('journal/', views.journal_list, name='journal_list'),
    path('journal/<slug:slug>/', views.article_detail, name='journal_detail'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),  # legacy alias
    path('fonts/', views.fonts_presentation, name='fonts_presentation'),
    path('partners/', views.partners_view, name='partners'),
    path('api/quiz-lead/', views.submit_quiz_lead, name='quiz_lead'),
    path('api/sample-box/', views.submit_sample_box, name='sample_box'),
    path('api/art-inquiry/', views.submit_art_inquiry, name='art_inquiry'),
    path('api/art-fitting/', views.submit_art_fitting, name='art_fitting'),
    path('api/calculator-lead/', views.submit_calculator_lead, name='calculator_lead'),
    path('api/partner-inquiry/', views.submit_partner_inquiry, name='partner_inquiry'),
    path('api/paint-order/', views.submit_paint_order, name='paint_order'),
]

