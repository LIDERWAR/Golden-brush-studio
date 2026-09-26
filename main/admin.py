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
                'hero_title_main',
                'hero_title_sub',
                'hero_desc',
                'hero_bg_image_url',
                ('portal1_num', 'portal1_title', 'portal1_link'),
                'portal1_desc',
                'portal1_img_url',
                ('portal2_num', 'portal2_title', 'portal2_link'),
                'portal2_desc',
                'portal2_img_url',
                ('portal3_num', 'portal3_title', 'portal3_link'),
                'portal3_desc',
                'portal3_img_url',
            ),
            'description': 'Первый экран сайта и 3 больших интерактивных окна (Художественные работы, Реставрация, Картинная галерея).'
        }),
        ('2. Секция Мастерской (Живой процесс и метрики)', {
            'fields': (
                'process_eyebrow',
                'process_title',
                'process_desc',
                'process_badge',
                'process_video_url',
                ('metric1_val', 'metric1_lbl'),
                ('metric2_val', 'metric2_lbl'),
                ('metric3_val', 'metric3_lbl'),
            )
        }),
        ('3. Интерактивный калькулятор сметы', {
            'fields': (
                'calc_eyebrow',
                'calc_title',
                'calc_desc',
                'calc_guarantee_text',
            ),
            'description': 'Список самих материалов и цены за м² редактируются в разделе «Каталог материалов & Калькулятор».'
        }),
        ('4. Реставрация и архитектурная реконструкция', {
            'fields': (
                'restoration_eyebrow',
                'restoration_title',
                'restoration_desc',
                ('restoration_badge_num', 'restoration_badge_lbl'),
                'restoration_img_url',
                ('restoration_item1_title', 'restoration_item1_desc'),
                ('restoration_item2_title', 'restoration_item2_desc'),
                ('restoration_item3_title', 'restoration_item3_desc'),
                ('restoration_item4_title', 'restoration_item4_desc'),
            )
        }),
        ('5. Бесплатная примерка картин в интерьере', {
            'fields': (
                'fitting_eyebrow',
                'fitting_title',
                'fitting_desc',
                ('fitting_step1_title', 'fitting_step1_desc'),
                ('fitting_step2_title', 'fitting_step2_desc'),
                ('fitting_step3_title', 'fitting_step3_desc'),
                ('fitting_step4_title', 'fitting_step4_desc'),
            )
        }),
        ('6. Кастомная арт-мебель и объекты', {
            'fields': (
                'furniture_eyebrow',
                'furniture_title',
                'furniture_desc',
                'furniture_img_url',
                ('furniture_item1_title', 'furniture_item1_desc'),
                ('furniture_item2_title', 'furniture_item2_desc'),
                ('furniture_item3_title', 'furniture_item3_desc'),
            )
        }),
        ('7. Блок Мастера (Александр Попыкин)', {
            'fields': (
                'master_eyebrow',
                'master_title',
                'master_quote',
                'master_desc',
                'master_img_url',
                ('timeline1_year', 'timeline1_text'),
                ('timeline2_year', 'timeline2_text'),
                ('timeline3_year', 'timeline3_text'),
                ('timeline4_year', 'timeline4_text'),
            )
        }),
        ('8. Прямые контакты и ссылки', {
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
        # Ограничиваем создание более 1 экземпляра настроек
        return not HomePageConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
