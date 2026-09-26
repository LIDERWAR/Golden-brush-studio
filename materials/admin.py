from django.contrib import admin
from .models import MaterialCategory, DecorativeMaterial, MaterialSampleImage

class MaterialSampleImageInline(admin.TabularInline):
    model = MaterialSampleImage
    extra = 2
    fields = ('image', 'title', 'order')


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(DecorativeMaterial)
class DecorativeMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price_per_sqm',
        'speed_sqm_per_day',
        'badge',
        'show_in_calculator',
        'is_active',
        'order'
    )
    list_filter = ('category', 'show_in_calculator', 'is_active')
    list_editable = ('price_per_sqm', 'badge', 'show_in_calculator', 'is_active', 'order')
    search_fields = ('name', 'short_desc', 'full_desc', 'composition')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MaterialSampleImageInline]

    fieldsets = (
        ('Основные параметры покрытия', {
            'fields': (
                'name',
                'slug',
                'category',
                'badge',
                'order',
                'is_active',
                'show_in_calculator'
            )
        }),
        ('Ценообразование и калькулятор', {
            'fields': (
                'price_per_sqm',
                'material_cost_ratio',
                'speed_sqm_per_day'
            ),
            'description': 'Параметры, используемые в интерактивном калькуляторе сметы на главной странице.'
        }),
        ('Описания и эстетика', {
            'fields': (
                'short_desc',
                'full_desc'
            )
        }),
        ('Технические характеристики', {
            'fields': (
                'composition',
                'application_areas',
                'fire_rating',
                'moisture_resistance'
            )
        }),
        ('Визуальные материалы', {
            'fields': (
                'image',
                'image_url'
            )
        }),
    )
