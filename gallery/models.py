from django.db import models

class ArtworkCategory(models.Model):
    name = models.CharField('Название направления', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория арт-работ'
        verbose_name_plural = 'Категории арт-работ'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

import re

def format_artwork_price(val):
    if not val:
        return 'По запросу'
    val = str(val).strip()
    if not val or 'запрос' in val.lower():
        return 'По запросу'
    digits = re.sub(r'\D', '', val)
    if digits:
        cleaned = re.sub(r'[\d\s₽.,руб\.rubRUB]', '', val, flags=re.IGNORECASE).strip()
        if not cleaned:
            num = int(digits)
            return f"{num:,}".replace(',', ' ') + ' ₽'
    return val

class Artwork(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступна к приобретению'),
        ('in_collection', 'В частной коллекции'),
        ('reserved', 'Зарезервировано'),
    ]

    title = models.CharField('Название произведения', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    category = models.ForeignKey(ArtworkCategory, on_delete=models.CASCADE, related_name='artworks', verbose_name='Направление')
    year = models.PositiveIntegerField('Год создания', default=2024)
    dimensions = models.CharField('Размеры', max_length=100, help_text='Например: 160 × 130 см или h: 42 см')
    medium = models.CharField('Техника и материалы', max_length=255, help_text='Например: Холст, минеральные пигменты, акрил, графит')
    status = models.CharField('Статус', max_length=30, choices=STATUS_CHOICES, default='available')
    price = models.CharField('Стоимость', max_length=100, default='По запросу', help_text='Например: 150000 или 350 000 ₽ (знак ₽ и пробелы подставляются автоматически)')
    
    curator_note = models.TextField('Кураторская экспликация / Описание концепции')
    image = models.ImageField('Фото произведения (загрузка с диска)', upload_to='artworks/', blank=True, null=True)
    image_url = models.CharField('Изображение (URL или статический путь)', max_length=255, default='/static/images/art_canvas.jpg')
    is_featured = models.BooleanField('Показывать в избранном', default=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Произведение искусства'
        verbose_name_plural = 'Арт-Галерея (Работы Саши)'
        ordering = ['order', '-year']

    def __str__(self):
        return f"«{self.title}» ({self.year}) — {self.get_status_display()}"

    @property
    def formatted_price(self):
        return format_artwork_price(self.price)

    def save(self, *args, **kwargs):
        self.price = format_artwork_price(self.price)
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

