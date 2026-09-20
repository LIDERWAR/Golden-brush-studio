from django.contrib import admin
from .models import ProjectCategory, Project

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'area_sqm', 'year', 'duration', 'is_featured', 'order')
    list_filter = ('category', 'is_featured', 'year')
    search_fields = ('title', 'client_name', 'location', 'short_description', 'scope_of_work')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
