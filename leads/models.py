from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('in_progress', 'В обработке (контакт установлен)'),
        ('audit_booked', 'Назначен выезд инженера на объект'),
        ('kp_sent', 'ТКП / Смета направлена'),
        ('contract', 'Заключение договора / Сделка'),
        ('archived', 'Архив / Нецелевой'),
    ]

    SOURCE_CHOICES = [
        ('quiz', 'Интерактивный B2B-квиз'),
        ('sample_box', 'Заказ Sample Box для архитекторов'),
        ('audit_form', 'Заявка на аудит объекта'),
        ('art_inquiry', 'Запрос на арт-работу (Галерея)'),
        ('quick_call', 'Быстрый звонок / Консультация'),
    ]

    name = models.CharField('Контактное лицо', max_length=150)
    company = models.CharField('Компания / Предприятие / Бюро', max_length=200, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50)
    email = models.EmailField('Email', blank=True, null=True)
    
    object_type = models.CharField('Тип объекта', max_length=100, blank=True, null=True)
    area_range = models.CharField('Площадь объекта', max_length=100, blank=True, null=True)
    service_needed = models.CharField('Требуемые услуги', max_length=255, blank=True, null=True)
    timeline = models.CharField('Планируемые сроки', max_length=100, blank=True, null=True)
    estimated_cost = models.CharField('Предварительная оценка сметы', max_length=100, blank=True, null=True)
    
    message = models.TextField('Комментарий заказчика / ТЗ', blank=True, null=True)
    source = models.CharField('Источник лида', max_length=50, choices=SOURCE_CHOICES, default='quiz')
    status = models.CharField('Статус обработки', max_length=30, choices=STATUS_CHOICES, default='new')
    manager_notes = models.TextField('Заметки Натальи / Менеджера', blank=True, null=True)
    
    created_at = models.DateTimeField('Дата и время поступления', auto_now_add=True)
    updated_at = models.DateTimeField('Последнее обновление', auto_now=True)

    class Meta:
        verbose_name = 'Входящий Лид (Заявка)'
        verbose_name_plural = 'Входящие Лиды (CRM)'
        ordering = ['-created_at']

    def __str__(self):
        comp = f" ({self.company})" if self.company else ""
        return f"{self.name}{comp} — {self.phone} [{self.get_status_display()}]"
