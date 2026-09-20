from django.contrib import admin
from .models import Article, Exhibition

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'published_date', 'read_time', 'is_published')
    list_filter = ('tag', 'is_published', 'published_date')
    search_fields = ('title', 'summary', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'venue', 'city', 'exhibition_type', 'status', 'order')
    list_filter = ('status', 'year', 'city')
    search_fields = ('title', 'venue', 'city', 'description')
    list_editable = ('status', 'order')
