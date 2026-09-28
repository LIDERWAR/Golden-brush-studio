from django.contrib import admin
from .models import Partner, HomePageConfig

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'order', 'is_active')
    list_filter = ('partner_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'partner_type', 'description')
    ordering = ('order', 'name')


@admin.register(HomePageConfig)
class HomePageConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('1. Главный экран (Hero) и 3 Портала', {
            'fields': (
                'hero_eyebrow',
                'hero_title',
                'hero_bg_image_url',
                ('portal1_title', 'portal1_link', 'portal1_img_url'),
                ('portal2_title', 'portal2_link', 'portal2_img_url'),
                ('portal3_title', 'portal3_link', 'portal3_img_url'),
            ),
            'description': 'Первый экран сайта и 3 больших интерактивных окна (Наши проекты, Реставрация, Галерея).'
        }),
        ('2. Секция Мастерской (Видео Reel и ключевые показатели)', {
            'fields': (
                'process_badge',
                'process_eyebrow',
                'process_title',
                'process_video_url',
                ('metric1_val', 'metric1_lbl'),
                ('metric2_val', 'metric2_lbl'),
                ('metric3_val', 'metric3_lbl'),
            )
        }),
        ('3. Реставрация (Блок на главной странице)', {
            'fields': (
                'restoration_eyebrow',
                'restoration_title',
                'restoration_desc',
                'restoration_img_url',
            )
        }),
        ('4. Калькулятор материалов (раздел /materials/)', {
            'fields': (
                'calc_guarantee_text',
            ),
            'description': 'Список самих материалов и цены за м² настраиваются в разделе «Декоративные покрытия & Калькулятор».'
        }),
        ('5. Прямые контакты и соцсети', {
            'fields': (
                'contact_phone',
                'contact_email',
                'contact_address',
                'telegram_url',
                'whatsapp_url',
            )
        }),
    )

    def has_add_permission(self, request):
        return not HomePageConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
