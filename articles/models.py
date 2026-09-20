from django.db import models

class Article(models.Model):
    title = models.CharField('Заголовок статьи', max_length=250)
    slug = models.SlugField('Слаг URL', unique=True)
    tag = models.CharField('Тематический тег', max_length=100, default='Fit-Out Экспертиза')
    summary = models.TextField('Краткий анонс статьи')
    content = models.TextField('Текст статьи (поддерживает HTML разметку)')
    image_url = models.CharField('Превью статьи', max_length=255, default='/static/images/hero.jpg')
    read_time = models.CharField('Время чтения', max_length=50, default='4 мин')
    published_date = models.DateField('Дата публикации')
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Статья / Публикация'
        verbose_name_plural = 'Статьи и Блог'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Exhibition(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Предстоящая выставка'),
        ('current', 'Текущая экспозиция'),
        ('past', 'Архив / Прошедшая'),
    ]

    title = models.CharField('Название выставки / Проекта', max_length=200)
    venue = models.CharField('Арт-пространство / Галерея', max_length=150)
    city = models.CharField('Город', max_length=100, default='Москва')
    year = models.PositiveIntegerField('Год', default=2024)
    dates = models.CharField('Даты проведения', max_length=100, blank=True)
    exhibition_type = models.CharField('Формат', max_length=100, default='Персональная выставка')
    status = models.CharField('Статус', max_length=30, choices=STATUS_CHOICES, default='past')
    description = models.TextField('Описание проекта / Концепция', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Выставка'
        verbose_name_plural = 'Выставочная деятельность Саши'
        ordering = ['-year', 'order']

    def __str__(self):
        return f"{self.year}: «{self.title}» — {self.venue} ({self.city})"
