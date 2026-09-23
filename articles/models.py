from django.db import models

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('wip', 'Мастерская: Work in Progress (Процесс создания)'),
        ('surfaces', 'Архитектура & Фактуры (Fit-Out философия)'),
        ('ceramics', 'Интерьерная керамика & Форма'),
        ('exhibitions', 'Хроника признания & События'),
        ('expert', 'Экспертиза генподряда'),
    ]

    title = models.CharField('Заголовок статьи / Эссе', max_length=250)
    slug = models.SlugField('Слаг URL', unique=True)
    category = models.CharField('Рубрика журнала', max_length=50, choices=CATEGORY_CHOICES, default='wip')
    tag = models.CharField('Тематический тег', max_length=100, default='Мастерская Саши Попыкина')
    summary = models.TextField('Краткий анонс / Кураторская экспликация')
    author_quote = models.TextField('Мысль автора / Цитата Саши', blank=True, null=True, help_text='Ключевая авторская мысль для акцентного блока')
    content = models.TextField('Текст статьи (поддерживает HTML разметку)')
    
    image = models.ImageField('Основное фото (загрузка с диска)', upload_to='journal/', blank=True, null=True)
    image_url = models.CharField('Превью (URL или статический путь)', max_length=255, default='/static/images/hero.jpg')
    
    read_time = models.CharField('Время чтения', max_length=50, default='4 мин')
    published_date = models.DateField('Дата публикации')
    is_published = models.BooleanField('Опубликовано', default=True)
    is_featured = models.BooleanField('Выводить на главной в Мастерской', default=True)

    class Meta:
        verbose_name = 'Запись Журнала / Статья'
        verbose_name_plural = 'Журнал Мастерской (Atelier Notes)'
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.get_category_display().split(':')[0]}] {self.title}"

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='process_images', verbose_name='Запись журнала')
    image = models.ImageField('Фото этапа создания', upload_to='journal/process/', blank=True, null=True)
    image_url = models.CharField('URL фото этапа', max_length=255, blank=True, default='/static/images/art_canvas.jpg')
    caption = models.CharField('Подпись к фотографии (стадия работы / материал)', max_length=250, blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Фотография процесса (WIP)'
        verbose_name_plural = 'Галерея процесса создания'
        ordering = ['order', 'id']

    def __str__(self):
        return f"Этап для: {self.article.title} ({self.caption or 'Без подписи'})"

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

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
