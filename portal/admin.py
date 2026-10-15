from django.contrib import admin
from .models import ClientAccount, ProjectContract, ProjectStage, StageUpdatePhoto, ProjectDocument

class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 1
    fields = ('step_number', 'title', 'status', 'date_label', 'description')

class StageUpdatePhotoInline(admin.TabularInline):
    model = StageUpdatePhoto
    extra = 2
    fields = ('caption', 'image', 'image_url', 'stage')

class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 1
    fields = ('title', 'doc_type', 'file', 'external_url', 'size_label')

@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'company', 'client_type', 'get_tier_display', 'get_materials_discount', 'get_works_discount', 'access_pin', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'company')
    list_filter = ('client_type', 'custom_tier', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'get_tier_display', 'get_materials_discount', 'get_works_discount', 'total_projects_count')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'full_name', 'phone', 'email', 'company', 'client_type', 'access_pin')
        }),
        ('Пожелания заказчика и логистика', {
            'fields': ('delivery_address', 'preferred_messenger', 'preferred_materials', 'preferred_spaces', 'service_options', 'client_wishes')
        }),
        ('Программа долгосрочного партнерства и скидок', {
            'fields': ('custom_tier', 'get_tier_display', 'get_materials_discount', 'get_works_discount', 'total_projects_count')
        }),
        ('Служебные заметки и системная информация', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )

    def get_tier_display(self, obj):
        return obj.tier_name
    get_tier_display.short_description = 'Уровень привилегий'

    def get_materials_discount(self, obj):
        return f"{obj.discount_materials}%"
    get_materials_discount.short_description = 'Скидка на материалы'

    def get_works_discount(self, obj):
        return f"{obj.discount_works}%"
    get_works_discount.short_description = 'Скидка на работы'

@admin.register(ProjectContract)
class ProjectContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'contract_number', 'status', 'progress_percent', 'total_amount', 'paid_amount', 'start_date')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'contract_number', 'client__full_name', 'client__phone')
    inlines = [ProjectStageInline, StageUpdatePhotoInline, ProjectDocumentInline]
    fieldsets = (
        ('Основная информация об объекте', {
            'fields': ('client', 'title', 'contract_number', 'address', 'total_area', 'status', 'progress_percent')
        }),
        ('Финансовые параметры сметы', {
            'fields': ('total_amount', 'paid_amount')
        }),
        ('Сроки и кураторы объекта', {
            'fields': ('start_date', 'estimated_completion', 'lead_artisan', 'artisan_phone')
        }),
    )

@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('project', 'step_number', 'title', 'status', 'date_label')
    list_filter = ('status',)
    search_fields = ('title', 'project__title')

@admin.register(StageUpdatePhoto)
class StageUpdatePhotoAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'stage', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('caption', 'project__title')

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'doc_type', 'size_label', 'created_at')
    list_filter = ('doc_type', 'created_at')
    search_fields = ('title', 'project__title')
