from django.db import models

class ProjectCategory(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Категория объектов'
        verbose_name_plural = 'Категории объектов'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField('Название проекта', max_length=200)
    slug = models.SlugField('Слаг URL', unique=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects', verbose_name='Категория')
    client_name = models.CharField('Заказчик / Бренд', max_length=150, blank=True)
    location = models.CharField('Локация / Город', max_length=150, default='Москва')
    area_sqm = models.PositiveIntegerField('Площадь, м²', help_text='Например: 1850')
    year = models.PositiveIntegerField('Год реализации', default=2024)
    duration = models.CharField('Срок выполнения', max_length=100, default='3 месяца')
    
    short_description = models.TextField('Краткое описание проекта')
    scope_of_work = models.TextField('Выполненные работы (через точку с запятой)', help_text='Например: Комплексный fit-out под ключ; Монтаж вентиляции и СКС; Авторские рельефные покрытия стен; Изготовление стола из массива дуба и латуни')
    
    image = models.ImageField('Фото объекта (загрузка с диска)', upload_to='projects/', blank=True, null=True)
    image_url = models.CharField('URL или путь к изображению', max_length=255, default='/static/images/case_hotel.jpg')
    is_featured = models.BooleanField('Отображать на главной', default=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объект Fit-Out (Кейс)'
        verbose_name_plural = 'Объекты Fit-Out (Портфолио)'
        ordering = ['order', '-year']

    def __str__(self):
        return f"{self.title} ({self.area_sqm} м²) — {self.category.name}"

    def get_scope_list(self):
        return [item.strip() for item in self.scope_of_work.split(';') if item.strip()]

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

