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
    list_display = ('full_name', 'phone', 'email', 'company', 'access_pin', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'company')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')

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
