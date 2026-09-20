from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'phone', 'object_type', 'area_range', 'source', 'status', 'created_at')
    list_filter = ('status', 'source', 'object_type', 'created_at')
    search_fields = ('name', 'company', 'phone', 'email', 'message', 'manager_notes')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Контактная информация', {
            'fields': ('name', 'company', 'phone', 'email')
        }),
        ('Параметры объекта (B2B расчет)', {
            'fields': ('object_type', 'area_range', 'service_needed', 'timeline', 'estimated_cost', 'message')
        }),
        ('Статус и ведение лида (CRM)', {
            'fields': ('source', 'status', 'manager_notes', 'created_at', 'updated_at')
        }),
    )
