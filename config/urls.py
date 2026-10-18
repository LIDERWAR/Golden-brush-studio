"""
URL configuration for Popykin Studio & Atelier project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from main import views as main_views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico', permanent=True)),
    path('robots.txt', main_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', main_views.sitemap_xml, name='sitemap_xml'),
    path('admin/', admin.site.urls),
    path('materials/', include('materials.urls')),
    path('portal/', include('portal.urls')),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
