from django.db import models
from django.urls import reverse

class MaterialCategory(models.Model):
    name = models.CharField('Название направления', max_length=150)
    slug = models.SlugField('Слаг URL', max_length=150, unique=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Категория материалов'
        verbose_name_plural = 'Категории материалов'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class DecorativeMaterial(models.Model):
    name = models.CharField('Название покрытия / материала', max_length=200)
    slug = models.SlugField('Слаг URL', max_length=200, unique=True)
    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materials',
        verbose_name='Категория'
    )
    badge = models.CharField(
        'Бейдж на карточке',
        max_length=100,
        blank=True,
        help_text='Например: Популярный выбор, Влагостойкий, Авторский арт, Скульптурный рельеф'
    )
    price_per_sqm = models.PositiveIntegerField(
        'Цена за м² под ключ (₽)',
        default=4500,
        help_text='Базовая расчетная стоимость (материал + нанесение мастерами)'
    )
    material_cost_ratio = models.FloatField(
        'Доля материалов в смете',
        default=0.35,
        help_text='0.35 = 35% на закупку и колеровку состава, 65% на работу декораторов'
    )
    speed_sqm_per_day = models.PositiveIntegerField(
        'Скорость нанесения (м² в день)',
        default=20,
        help_text='Используется для ориентировочного расчета рабочих дней'
    )
    short_desc = models.TextField(
        'Краткое описание (для калькулятора и карточки)',
        help_text='1-2 емких предложения о текстуре и эстетике'
    )
    full_desc = models.TextField(
        'Подробное описание и технология',
        blank=True,
        help_text='Детальная экспликация техники нанесения, компонентов и визуального восприятия'
    )
    composition = models.CharField(
        'Основа / Состав',
        max_length=255,
        blank=True,
        default='Минеральные компоненты, натуральные пигменты',
        help_text='Например: Гидравлическая известь, мраморная мука, гранитная крошка'
    )
    application_areas = models.CharField(
        'Зоны применения',
        max_length=255,
        blank=True,
        default='Гостиные, холлы, спальни, коммерческие пространства',
        help_text='Например: Санузлы, влажные зоны, фасады, акцентные стены в лобби'
    )
    fire_rating = models.CharField(
        'Класс пожарной безопасности',
        max_length=100,
        default='КМ-0 (негорючий минеральный состав)'
    )
    moisture_resistance = models.CharField(
        'Стойкость к влаге и уход',
        max_length=150,
        default='Влагостойкое, моющееся покрытие'
    )
    image = models.ImageField(
        'Главное фото выкраса / текстуры',
        upload_to='materials/',
        blank=True,
        null=True
    )
    image_url = models.CharField(
        'Резервный путь к изображению',
        max_length=255,
        default='/static/images/hero.jpg'
    )
    show_in_calculator = models.BooleanField(
        'Отображать в калькуляторе на главной',
        default=True,
        help_text='Если включено, покрытие выводится в сетке выбора калькулятора'
    )
    is_active = models.BooleanField('Активно (показывать на сайте)', default=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Декоративное покрытие'
        verbose_name_plural = 'Каталог материалов & Калькулятор'
        ordering = ['order', 'price_per_sqm']

    def __str__(self):
        return f"{self.name} ({self.formatted_price}/м²)"

    @property
    def formatted_price(self):
        return f"{self.price_per_sqm:,}".replace(',', ' ') + ' ₽'

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    def get_absolute_url(self):
        return reverse('materials:detail', kwargs={'slug': self.slug})


class MaterialSampleImage(models.Model):
    material = models.ForeignKey(
        DecorativeMaterial,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Материал'
    )
    image = models.ImageField('Фото образца / интерьера', upload_to='materials/samples/')
    title = models.CharField('Подпись / объект', max_length=150, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фотография образца'
        verbose_name_plural = 'Галерея выкрасов и объектов'
        ordering = ['order', 'id']

    def __str__(self):
        return f"Образец: {self.material.name} ({self.title or 'без подписи'})"
