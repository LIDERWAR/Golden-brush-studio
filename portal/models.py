from django.db import models
from django.contrib.auth.models import User

class ClientAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_account', null=True, blank=True)
    phone = models.CharField('Номер телефона', max_length=30, unique=True, db_index=True)
    full_name = models.CharField('ФИО Заказчика', max_length=150)
    email = models.EmailField('Email', blank=True, null=True)
    company = models.CharField('Организация / Бюро / Объект', max_length=200, blank=True, null=True)
    access_pin = models.CharField('Код быстрого доступа / ПИН', max_length=10, default='1234')
    notes = models.TextField('Служебные заметки Натальи / CRM', blank=True, null=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Последняя активность', auto_now=True)

    class Meta:
        verbose_name = 'Клиентский профиль'
        verbose_name_plural = 'Клиентская база (Личные кабинеты)'
        ordering = ['-created_at']

    def __str__(self):
        comp = f" ({self.company})" if self.company else ""
        return f"{self.full_name}{comp} — {self.phone}"


class ProjectContract(models.Model):
    STATUS_CHOICES = [
        ('active', 'В активной работе'),
        ('review', 'Приемка и технический контроль'),
        ('completed', 'Объект сдан (на 5-летней гарантии)'),
    ]

    client = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, related_name='projects', verbose_name='Заказчик')
    title = models.CharField('Название объекта', max_length=200, default='Премиальный жилой интерьер')
    contract_number = models.CharField('Номер договора', max_length=50, blank=True, default='GB-2026/09-14')
    address = models.CharField('Адрес объекта', max_length=255, blank=True, default='Москва, Центр')
    total_area = models.CharField('Площадь помещений', max_length=50, default='240 м²')
    total_amount = models.DecimalField('Сумма по смете (₽)', max_digits=12, decimal_places=2, default=850000)
    paid_amount = models.DecimalField('Оплачено заказчиком (₽)', max_digits=12, decimal_places=2, default=425000)
    
    start_date = models.DateField('Дата начала работ', null=True, blank=True)
    estimated_completion = models.DateField('Планируемая сдача', null=True, blank=True)
    lead_artisan = models.CharField('Ведущий мастер / Технолог', max_length=150, default='Александр Попыкин')
    artisan_phone = models.CharField('Телефон технолога объекта', max_length=50, default='+7 (495) 890-44-22')
    
    status = models.CharField('Статус объекта', max_length=30, choices=STATUS_CHOICES, default='active')
    progress_percent = models.PositiveIntegerField('Общий прогресс (%)', default=65)
    
    created_at = models.DateTimeField('Дата создания карточки', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Объект заказчика'
        verbose_name_plural = 'Объекты в работе (Трекер)'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.client.full_name}] — {self.get_status_display()}"

    @property
    def remaining_amount(self):
        return max(self.total_amount - self.paid_amount, 0)


class ProjectStage(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Завершен'),
        ('in_progress', 'В работе сейчас'),
        ('pending', 'Ожидает начала'),
    ]

    project = models.ForeignKey(ProjectContract, on_delete=models.CASCADE, related_name='stages', verbose_name='Объект')
    step_number = models.PositiveIntegerField('Порядок этапа', default=1)
    title = models.CharField('Название этапа', max_length=200)
    description = models.TextField('Техническое описание и примечания', blank=True, null=True)
    status = models.CharField('Статус этапа', max_length=30, choices=STATUS_CHOICES, default='pending')
    date_label = models.CharField('Сроки / Дата завершения', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Этап реализации'
        verbose_name_plural = 'Этапы реализации объекта'
        ordering = ['step_number']

    def __str__(self):
        return f"Этап {self.step_number}: {self.title} ({self.get_status_display()})"


class StageUpdatePhoto(models.Model):
    project = models.ForeignKey(ProjectContract, on_delete=models.CASCADE, related_name='photos', verbose_name='Объект')
    stage = models.ForeignKey(ProjectStage, on_delete=models.SET_NULL, null=True, blank=True, related_name='stage_photos', verbose_name='Привязка к этапу')
    image = models.ImageField('Фотография со стройки/мастерской', upload_to='portal/updates/%Y/%m/', null=True, blank=True)
    image_url = models.CharField('Или URL изображения', max_length=500, blank=True, null=True)
    caption = models.CharField('Подпись к фото', max_length=255)
    created_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Фотоотчет со стройки'
        verbose_name_plural = 'Фотоотчеты со стройки (Бэкстейдж)'
        ordering = ['-created_at']

    def get_display_url(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/images/hero.jpg'


class ProjectDocument(models.Model):
    DOC_TYPES = [
        ('contract', 'Договор подряда'),
        ('estimate', 'Смета и спецификация материалов'),
        ('act', 'Акт скрытых работ / КС-2'),
        ('warranty', 'Официальный сертификат 5 лет гарантии'),
        ('tech', 'Технологическая карта нанесения'),
        ('other', 'Прочие документы'),
    ]

    project = models.ForeignKey(ProjectContract, on_delete=models.CASCADE, related_name='documents', verbose_name='Объект')
    title = models.CharField('Название документа', max_length=200)
    doc_type = models.CharField('Тип документа', max_length=50, choices=DOC_TYPES, default='contract')
    file = models.FileField('Файл (PDF/DOCX)', upload_to='portal/docs/%Y/%m/', blank=True, null=True)
    external_url = models.URLField('Внешняя ссылка на скачивание', blank=True, null=True)
    size_label = models.CharField('Размер / Формат', max_length=50, default='PDF, 2.4 МБ')
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Проектный документ'
        verbose_name_plural = 'Проектные документы и сметы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_doc_type_display()})"
