from django.db import models
from django.core.validators import RegexValidator

metrika_validator = RegexValidator(
    regex=r'^\d{5,15}$',
    message='Номер счетчика Яндекс.Метрики должен содержать только цифры (от 5 до 15 знаков).'
)

class Partner(models.Model):
    name = models.CharField('Название бюро / партнера', max_length=150)
    partner_type = models.CharField('Тип партнера', max_length=150, blank=True, help_text='Например: Архитектурное бюро, Девелопер клубных домов')
    description = models.TextField('Описание совместных проектов', blank=True)
    website_url = models.URLField('Ссылка на сайт / соцсети', blank=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры студии'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.partner_type})"


class HomePageConfig(models.Model):
    """
    Единая панель управления текстовым и визуальным контентом главной страницы
    и общими настройками студии Golden Brush Studio.
    Singleton-модель: в базе хранится 1 запись.
    """
    # 1. Hero-блок и 3 Портала
    hero_eyebrow = models.CharField(
        'Hero: Надстрочник',
        max_length=200,
        default='',
        blank=True
    )
    hero_title = models.CharField(
        'Hero: Главный заголовок',
        max_length=200,
        default='Художественно-декоративные работы под ключ',
        blank=True
    )
    hero_bg_image = models.ImageField(
        'Hero: Загрузить фоновое фото',
        upload_to='home/',
        blank=True,
        null=True,
        help_text='Загрузите фото с компьютера через кнопку «Выберите файл»'
    )
    hero_bg_image_url = models.CharField(
        'Hero: Резервный URL / путь',
        max_length=255,
        default='/static/images/hero_plaster_texture.jpg',
        blank=True
    )

    portal1_title = models.CharField('Портал 1: Заголовок', max_length=150, default='Наши проекты', blank=True)
    portal1_link = models.CharField('Портал 1: Ссылка', max_length=200, default='/projects/', blank=True)
    portal1_image = models.ImageField(
        'Портал 1: Загрузить фото',
        upload_to='home/',
        blank=True,
        null=True,
        help_text='Загрузите фото с компьютера через кнопку «Выберите файл»'
    )
    portal1_img_url = models.CharField('Портал 1: Резервный URL / путь', max_length=255, default='/static/images/case_bar_coyote.jpg', blank=True)

    portal2_title = models.CharField('Портал 2: Заголовок', max_length=150, default='Декоративные покрытия', blank=True)
    portal2_link = models.CharField('Портал 2: Ссылка', max_length=200, default='/materials/', blank=True)
    portal2_image = models.ImageField(
        'Портал 2: Загрузить фото',
        upload_to='home/',
        blank=True,
        null=True,
        help_text='Загрузите фото с компьютера через кнопку «Выберите файл»'
    )
    portal2_img_url = models.CharField('Портал 2: Резервный URL / путь', max_length=255, default='/static/images/mat_mural.jpg', blank=True)

    portal3_title = models.CharField('Портал 3: Заголовок', max_length=150, default='Арт-галерея', blank=True)
    portal3_link = models.CharField('Портал 3: Ссылка', max_length=200, default='/gallery/', blank=True)
    portal3_image = models.ImageField(
        'Портал 3: Загрузить фото',
        upload_to='home/',
        blank=True,
        null=True,
        help_text='Загрузите фото с компьютера через кнопку «Выберите файл»'
    )
    portal3_img_url = models.CharField('Портал 3: Резервный URL / путь', max_length=255, default='/static/images/art_canvas.jpg', blank=True)

    # 2. Процесс мастерской (Reel & Метрики)
    process_badge = models.CharField('Процесс: Подпись на бейдже', max_length=150, default='Мастерская Golden Brush Studio', blank=True)
    process_eyebrow = models.CharField('Процесс: Надстрочник', max_length=200, default='Процесс создания', blank=True)
    process_title = models.CharField('Процесс: Заголовок', max_length=200, default='Магия ручной работы и минеральных текстур', blank=True)
    process_video_url = models.CharField('Процесс: Видео (URL ролика или mp4)', max_length=255, blank=True, default='')

    metric1_val = models.CharField('Метрика 1: Число', max_length=50, default='15+', blank=True)
    metric1_lbl = models.CharField('Метрика 1: Подпись', max_length=100, default='лет практики в декоре и росписи', blank=True)
    metric2_val = models.CharField('Метрика 2: Число', max_length=50, default='200+', blank=True)
    metric2_lbl = models.CharField('Метрика 2: Подпись', max_length=100, default='авторских рецептур штукатурки', blank=True)
    metric3_val = models.CharField('Метрика 3: Число', max_length=50, default='100%', blank=True)
    metric3_lbl = models.CharField('Метрика 3: Подпись', max_length=100, default='ручное нанесение мастерами', blank=True)

    # 3. Реставрационный блок (Превью на главной)
    restoration_eyebrow = models.CharField('Реставрация: Надстрочник', max_length=200, default='Мастерство & Наследие', blank=True)
    restoration_title = models.CharField('Реставрация: Заголовок', max_length=200, default='Реставрация и оформление', blank=True)
    restoration_desc = models.TextField('Реставрация: Описание', default='Бережное восстановление исторической архитектурной лепнины, мозаичных панно, сусального золота и антикварных интерьерных поверхностей.', blank=True)
    restoration_image = models.ImageField(
        'Реставрация: Загрузить фото',
        upload_to='home/',
        blank=True,
        null=True,
        help_text='Загрузите фото с компьютера через кнопку «Выберите файл»'
    )
    restoration_img_url = models.CharField('Реставрация: Резервный URL / путь', max_length=255, default='/static/images/restoration_craft.jpg', blank=True)

    # 4. Внутренние разделы: Калькулятор покрытий (/materials/)
    calc_guarantee_text = models.CharField('Калькулятор: Текст гарантии под кнопкой', max_length=255, default='Бесплатный выезд технолога с образцами по Москве и МО • Замер и точная смета', blank=True)

    # 5. Прямые контакты и соцсети студии
    contact_phone = models.CharField('Телефон для связи', max_length=50, default='+7 (495) 890-44-22', blank=True)
    contact_email = models.EmailField('Email', default='welcome@gbstudio.ru', blank=True)
    contact_address = models.CharField('Адрес студии / мастерской', max_length=255, default='Москва, Центр дизайна ARTPLAY / Мастерская на Яузе', blank=True)
    telegram_url = models.CharField('Ссылка Telegram', max_length=200, default='https://t.me/gbstudio', blank=True)
    whatsapp_url = models.CharField('Ссылка / номер WhatsApp', max_length=200, default='https://wa.me/74958904422', blank=True)
    yandex_metrika_id = models.CharField(
        'Номер счетчика Яндекс.Метрики',
        max_length=50,
        blank=True,
        default='',
        validators=[metrika_validator],
        help_text='Например: 99123456. При указании счетчик и цели аналитики подключаются автоматически.'
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Контент главной страницы & Настройки'
        verbose_name_plural = 'Главная страница & Настройки'

    def __str__(self):
        return f"Golden Brush Studio — Тексты и настройки (обновлено {self.updated_at.strftime('%d.%m.%Y')})"

    @property
    def get_hero_bg_image(self):
        if self.hero_bg_image:
            return self.hero_bg_image.url
        return self.hero_bg_image_url or '/static/images/hero_plaster_texture.jpg'

    @property
    def get_portal1_img(self):
        if self.portal1_image:
            return self.portal1_image.url
        return self.portal1_img_url or '/static/images/case_bar_coyote.jpg'

    @property
    def get_portal2_img(self):
        if self.portal2_image:
            return self.portal2_image.url
        return self.portal2_img_url or '/static/images/mat_mural.jpg'

    @property
    def get_portal3_img(self):
        if self.portal3_image:
            return self.portal3_image.url
        return self.portal3_img_url or '/static/images/art_canvas.jpg'

    @property
    def get_restoration_img(self):
        if self.restoration_image:
            return self.restoration_image.url
        return self.restoration_img_url or '/static/images/restoration_craft.jpg'

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj
