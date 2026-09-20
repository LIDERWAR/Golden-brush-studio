from django.contrib import admin
from .models import ArtworkCategory, Artwork

@admin.register(ArtworkCategory)
class ArtworkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'dimensions', 'status', 'price', 'is_featured', 'order')
    list_filter = ('category', 'status', 'year', 'is_featured')
    search_fields = ('title', 'medium', 'curator_note')
    list_editable = ('status', 'price', 'is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
