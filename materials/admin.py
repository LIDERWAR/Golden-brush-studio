from django.contrib import admin
from django.utils.html import mark_safe
from .models import MaterialCategory, DecorativeMaterial, MaterialSampleImage

class MaterialSampleImageInline(admin.TabularInline):
    model = MaterialSampleImage
    extra = 2
    fields = ('image_thumb', 'image', 'title', 'order')
    readonly_fields = ('image_thumb',)

    @admin.display(description='Миниатюра')
    def image_thumb(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 35px; object-fit: cover; border-radius: 4px; border: 1px solid #c5a059;" />')
        return '—'


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(DecorativeMaterial)
class DecorativeMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'name',
        'category',
        'price_per_sqm',
        'speed_sqm_per_day',
        'badge',
        'show_in_calculator',
        'is_active',
        'order'
    )
    list_display_links = ('image_preview', 'name')
    list_filter = ('category', 'show_in_calculator', 'is_active')
    list_editable = ('price_per_sqm', 'badge', 'show_in_calculator', 'is_active', 'order')
    search_fields = ('name', 'short_desc', 'full_desc', 'composition')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('display_preview',)
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
        ('Описания и эстетика (отображается при наведении в калькуляторе)', {
            'fields': (
                'short_desc',
                'full_desc'
            ),
            'description': '«Краткое описание» — текст, который выводится на карточке и при наведении мыши в калькуляторе. «Подробное описание» — полный текст на странице материала.'
        }),
        ('Технические характеристики', {
            'fields': (
                'composition',
                'application_areas',
                'fire_rating',
                'moisture_resistance'
            )
        }),
        ('Визуальные материалы (фотография / выкрас)', {
            'fields': (
                'display_preview',
                'image',
                'image_url'
            ),
            'description': 'Загрузите фотографию реального выкраса (Image) или укажите URL/путь. При загрузке файла он автоматически имеет приоритет на сайте.'
        }),
    )

    @admin.display(description='Образец')
    def image_preview(self, obj):
        if obj.display_image:
            return mark_safe(f'<img src="{obj.display_image}" style="width: 52px; height: 38px; object-fit: cover; border-radius: 4px; border: 1px solid rgba(197, 160, 89, 0.6); display: block;" />')
        return '—'

    @admin.display(description='Текущий образец на сайте')
    def display_preview(self, obj):
        if obj.display_image:
            return mark_safe(
                f'<div style="margin-bottom: 8px;">'
                f'<img src="{obj.display_image}" style="max-width: 260px; max-height: 170px; object-fit: cover; border-radius: 6px; border: 1px solid #c5a059; box-shadow: 0 4px 15px rgba(0,0,0,0.25);" />'
                f'<div style="color: #999; font-size: 11px; margin-top: 4px;">Путь к файлу: {obj.display_image}</div>'
                f'</div>'
            )
        return 'Образец еще не загружен'
