from django.contrib import admin
from .models import Article, ArticleImage, Exhibition

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 2
    fields = ('image', 'image_url', 'caption', 'order')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'tag', 'published_date', 'read_time', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published', 'published_date')
    search_fields = ('title', 'summary', 'author_quote', 'content')
    list_editable = ('category', 'is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'tag', 'published_date', 'read_time', 'is_featured', 'is_published')
        }),
        ('Визуал и анонс', {
            'fields': ('summary', 'author_quote', 'image', 'image_url')
        }),
        ('Текст публикации (поддерживает HTML)', {
            'fields': ('content',)
        }),
    )

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'venue', 'city', 'exhibition_type', 'status', 'order')
    list_filter = ('status', 'year', 'city')
    search_fields = ('title', 'venue', 'city', 'description')
    list_editable = ('status', 'order')
