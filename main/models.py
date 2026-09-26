from django.db import models

class Partner(models.Model):
    name = models.CharField('Название бюро / партнера', max_length=150)
    partner_type = models.CharField('Тип партнера', max_length=150, help_text='Например: Архитектурное бюро, Девелопер клубных домов')
    description = models.TextField('Описание совместных проектов')
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
    Единая панель управления текстовым и визуальным контентом главной страницы.
    Singleton-модель: в базе хранится 1 запись.
    """
    # 1. Hero-блок
    hero_eyebrow = models.CharField(
        'Hero: Надстрочник',
        max_length=200,
        default='Искусство как преображение пространства'
    )
    hero_title_main = models.CharField(
        'Hero: Главный заголовок (строка 1)',
        max_length=200,
        default='Художественно-декоративные работы'
    )
    hero_title_sub = models.CharField(
        'Hero: Акцентный подзаголовок (строка 2)',
        max_length=200,
        default='и проекты под ключ'
    )
    hero_desc = models.TextField(
        'Hero: Описание студии',
        default='Ателье авторских минеральных поверхностей, монументальной росписи, реставрации и станковой живописи под руководством художника Александра Попыкина с 2011 года.'
    )
    hero_bg_image_url = models.CharField(
        'Hero: Фоновое изображение',
        max_length=255,
        default='/static/images/fresco_texture.jpg'
    )

    # 3 Главных Портала (Окна)
    portal1_num = models.CharField('Портал 1: Номер/рубрика', max_length=100, default='01 / Фактуры & Материя')
    portal1_title = models.CharField('Портал 1: Заголовок', max_length=150, default='Художественно-декоративные работы')
    portal1_desc = models.TextField('Портал 1: Описание', default='Авторские рельефные штукатурки, бесшовный микроцемент, монументальные фрески, барельефы, золочение и окислы металлов.')
    portal1_link = models.CharField('Портал 1: Ссылка', max_length=200, default='/materials/')
    portal1_link_text = models.CharField('Портал 1: Текст ссылки', max_length=100, default='Каталог фактур и калькулятор')
    portal1_img_url = models.CharField('Портал 1: Фото', max_length=255, default='/static/images/hero.jpg')

    portal2_num = models.CharField('Портал 2: Номер/рубрика', max_length=100, default='02 / Наследие & Мастерство')
    portal2_title = models.CharField('Портал 2: Заголовок', max_length=150, default='Реставрация и оформление')
    portal2_desc = models.TextField('Портал 2: Описание', default='Бережная реставрация архитектурной лепнины, мозаичных панно, антикварных деталей, фасадов, каминных порталов и сусального золота.')
    portal2_link = models.CharField('Портал 2: Ссылка', max_length=200, default='#restoration')
    portal2_link_text = models.CharField('Портал 2: Текст ссылки', max_length=100, default='Реставрационные кейсы')
    portal2_img_url = models.CharField('Портал 2: Фото', max_length=255, default='/static/images/restoration_craft.jpg')

    portal3_num = models.CharField('Портал 3: Номер/рубрика', max_length=100, default='03 / Живопись & Витрина')
    portal3_title = models.CharField('Портал 3: Заголовок', max_length=150, default='Картинная галерея с примеркой')
    portal3_desc = models.TextField('Портал 3: Описание', default='Оригинальные интерьерные полотна Александра Попыкина с указанием размеров и цен. Бесплатная примерка полотен в вашем интерьере.')
    portal3_link = models.CharField('Портал 3: Ссылка', max_length=200, default='/gallery/')
    portal3_link_text = models.CharField('Портал 3: Текст ссылки', max_length=100, default='Витрина полотен и заказ')
    portal3_img_url = models.CharField('Портал 3: Фото', max_length=255, default='/static/images/art_canvas.jpg')

    # 2. Процесс мастерской (Reel)
    process_eyebrow = models.CharField('Процесс: Надстрочник', max_length=200, default='Живой процесс мастерской')
    process_title = models.CharField('Процесс: Заголовок', max_length=200, default='Как рождается материя в руках художника')
    process_desc = models.TextField('Процесс: Описание', default='Каждая фактура стены, рельефное панно и картина — результат тонкого диалога мастера с материалом. Мы сами смешиваем минеральные пигменты, наносим многослойные воски, полируем микроцемент и вручную создаем сложнейшие переходы светотени, которые невозможно воспроизвести заводским способом.')
    process_badge = models.CharField('Процесс: Подпись на видео', max_length=150, default='Мастерская Александра Попыкина • Москва')
    process_video_url = models.CharField('Процесс: Видео (URL файла или ролика)', max_length=255, blank=True, default='')
    
    metric1_val = models.CharField('Метрика 1: Число', max_length=50, default='15+')
    metric1_lbl = models.CharField('Метрика 1: Подпись', max_length=100, default='лет практики в декоре и росписи')
    metric2_val = models.CharField('Метрика 2: Число', max_length=50, default='200+')
    metric2_lbl = models.CharField('Метрика 2: Подпись', max_length=100, default='авторских рецептур штукатурки')
    metric3_val = models.CharField('Метрика 3: Число', max_length=50, default='100%')
    metric3_lbl = models.CharField('Метрика 3: Подпись', max_length=100, default='ручное нанесение мастерами')

    # 3. Калькулятор покрытий
    calc_eyebrow = models.CharField('Калькулятор: Надстрочник', max_length=200, default='Каталог материалов & Расчет сметы')
    calc_title = models.CharField('Калькулятор: Заголовок', max_length=200, default='Каталог декоративных покрытий и расчет по площади')
    calc_desc = models.TextField('Калькулятор: Описание', default='Выберите тип покрытия и укажите метраж стен для моментального расчета стоимости материалов и работы мастеров с выездом технолога.')
    calc_guarantee_text = models.CharField('Калькулятор: Текст гарантии под кнопкой', max_length=255, default='Бесплатный выезд технолога с образцами по Москве и МО • Замер и точная смета')

    # 4. Реставрация
    restoration_eyebrow = models.CharField('Реставрация: Надстрочник', max_length=200, default='Реконструкция & Наследие')
    restoration_title = models.CharField('Реставрация: Заголовок', max_length=200, default='Реставрация лепнины, мозаики и оформление')
    restoration_desc = models.TextField('Реставрация: Описание', default='Мы бережно восстанавливаем утраченные фрагменты сложной архитектурной лепнины, мозаичные панно из смальты и натурального камня, сусальное золочение, историческую роспись и антикварные поверхности. Работаем как с памятниками архитектуры, так и с частными коллекционными пространствами.')
    restoration_badge_num = models.CharField('Реставрация: Бейдж (число)', max_length=50, default='100%')
    restoration_badge_lbl = models.CharField('Реставрация: Бейдж (текст)', max_length=150, default='сохранение исторической аутентичности')
    restoration_img_url = models.CharField('Реставрация: Фото', max_length=255, default='/static/images/restoration_craft.jpg')
    restoration_item1_title = models.CharField('Услуга 1: Заголовок', max_length=150, default='Воссоздание гипсовой и каменной лепнины')
    restoration_item1_desc = models.TextField('Услуга 1: Описание', default='Снятие форм, долепка утрат, укрепление основы и финишная тонировка.')
    restoration_item2_title = models.CharField('Услуга 2: Заголовок', max_length=150, default='Золочение сусальным золотом и поталью')
    restoration_item2_desc = models.TextField('Услуга 2: Описание', default='Классическое клеевое и масляное золочение карнизов, пилястр, сводов и арт-объектов.')
    restoration_item3_title = models.CharField('Услуга 3: Заголовок', max_length=150, default='Мозаичные панно и римская мозаика')
    restoration_item3_desc = models.TextField('Услуга 3: Описание', default='Реставрация и создание мозаичных ковров, фартуков, бассейнов и каминных зон.')
    restoration_item4_title = models.CharField('Услуга 4: Заголовок', max_length=150, default='Патинирование и художественное состаривание')
    restoration_item4_desc = models.TextField('Услуга 4: Описание', default='Благородная патина времени для каминов, порталов, дверей и деревянных панелей.')

    # 5. Примерка картин в интерьере
    fitting_eyebrow = models.CharField('Примерка: Надстрочник', max_length=200, default='Флагманский сервис студии')
    fitting_title = models.CharField('Примерка: Заголовок', max_length=200, default='Бесплатная примерка картин в вашем интерьере')
    fitting_desc = models.TextField('Примерка: Описание', default='Картина должна звучать в реальном свете вашего дома. Мы бесплатно привезем оригиналы выбранных полотен Александра Попыкина к вам на объект в Москве и Подмосковье, навесим и примерим на ваших стенах. Вы покупаете только то, что идеально подошло вашему пространству.')
    fitting_step1_title = models.CharField('Шаг 1: Заголовок', max_length=100, default='Выбор работ')
    fitting_step1_desc = models.CharField('Шаг 1: Описание', max_length=255, default='Выберите до 5 полотен на сайте или отправьте фото интерьера нашему куратору.')
    fitting_step2_title = models.CharField('Шаг 2: Заголовок', max_length=100, default='Доставка на объект')
    fitting_step2_desc = models.CharField('Шаг 2: Описание', max_length=255, default='Бесплатно привозим картины на специально оборудованном транспорте студии.')
    fitting_step3_title = models.CharField('Шаг 3: Заголовок', max_length=100, default='Примерка на стене')
    fitting_step3_desc = models.CharField('Шаг 3: Описание', max_length=255, default='Оцениваем масштаб, колорит и освещение в дневных и вечерних сценариях.')
    fitting_step4_title = models.CharField('Шаг 4: Заголовок', max_length=100, default='Решение без спешки')
    fitting_step4_desc = models.CharField('Шаг 4: Описание', max_length=255, default='Подошедшие картины остаются у вас. Остальные мы увозим без каких-либо оплат.')

    # 6. Арт-мебель
    furniture_eyebrow = models.CharField('Арт-мебель: Надстрочник', max_length=200, default='Сложные интерьерные формы')
    furniture_title = models.CharField('Арт-мебель: Заголовок', max_length=200, default='Кастомные арт-объекты и дизайнерская мебель')
    furniture_desc = models.TextField('Арт-мебель: Описание', default='Помимо стен, мы создаем уникальные штучные предметы интерьера: массивные обеденные столы из монолитного микроцемента, стулья и кресла скульптурных форм, каминные порталы с патиной и латунью, декоративные колонны и арт-перегородки под ключ.')
    furniture_img_url = models.CharField('Арт-мебель: Фото', max_length=255, default='/static/images/art_furniture.jpg')
    furniture_item1_title = models.CharField('Мебель 1: Заголовок', max_length=150, default='Монолитные столы из микроцемента и слэбов')
    furniture_item1_desc = models.CharField('Мебель 1: Описание', max_length=255, default='Устойчивые к царапинам, влаге и горячей посуде. Любая геометрия под заказ.')
    furniture_item2_title = models.CharField('Мебель 2: Заголовок', max_length=150, default='Скульптурные стулья и арт-кресла')
    furniture_item2_desc = models.CharField('Мебель 2: Описание', max_length=255, default='Интерьерная пластика с минеральными и бронзовыми эффектами поверхности.')
    furniture_item3_title = models.CharField('Мебель 3: Заголовок', max_length=150, default='Каминные порталы и архитектурные объемы')
    furniture_item3_desc = models.CharField('Мебель 3: Описание', max_length=255, default='Индивидуальное проектирование, патинирование, интеграция подсветки и металла.')

    # 7. Мастер (Саша Попыкин)
    master_eyebrow = models.CharField('Мастер: Надстрочник', max_length=200, default='Мастер и создатель студии')
    master_title = models.CharField('Мастер: Заголовок', max_length=200, default='Александр Попыкин: Искусство монументальной материи')
    master_quote = models.TextField('Мастер: Цитата', default='«Стена в несколько сотен или тысяч метров — это такое же художественное полотно, где плотность зерна, температура света и тактильный рельеф определяют статус всего пространства».')
    master_desc = models.TextField('Мастер: Описание пути', default='Начав творческий путь в 1998 году с граффити-райтинга, Александр выработал безупречное чувство масштаба, ритма и пластики. Станковая живопись, эксперименты со скульптурной керамикой и монументальными декоративными покрытиями (с 2011 г.) сформировали неповторимый авторский почерк студии.')
    master_img_url = models.CharField('Мастер: Фото', max_length=255, default='/static/images/art_canvas.jpg')
    timeline1_year = models.CharField('Хроника 1: Год', max_length=50, default='1998')
    timeline1_text = models.CharField('Хроника 1: Текст', max_length=200, default='Уличные корни, масштаб и пластика')
    timeline2_year = models.CharField('Хроника 2: Год', max_length=50, default='2005')
    timeline2_text = models.CharField('Хроника 2: Текст', max_length=200, default='Станковая живопись и выставки')
    timeline3_year = models.CharField('Хроника 3: Год', max_length=50, default='2011')
    timeline3_text = models.CharField('Хроника 3: Текст', max_length=200, default='Интерьерный декор и архитектурные поверхности')
    timeline4_year = models.CharField('Хроника 4: Год', max_length=50, default='2026')
    timeline4_text = models.CharField('Хроника 4: Текст', max_length=200, default='Собственная лаборатория фактур и ателье')

    # 8. Контакты и каналы
    contact_phone = models.CharField('Телефон для связи', max_length=50, default='+7 (495) 890-44-22')
    contact_email = models.EmailField('Email', default='welcome@gbstudio.ru')
    contact_address = models.CharField('Адрес студии / мастерской', max_length=255, default='Москва, Центр дизайна ARTPLAY / Мастерская на Яузе')
    telegram_url = models.CharField('Ссылка Telegram', max_length=200, default='https://t.me/gbstudio')
    whatsapp_url = models.CharField('Ссылка / номер WhatsApp', max_length=200, default='https://wa.me/74958904422')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Контент главной страницы'
        verbose_name_plural = 'Главная страница (Все тексты и блоки)'

    def __str__(self):
        return f"Тексты и блоки главной страницы (обновлено {self.updated_at.strftime('%d.%m.%Y')})"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj
