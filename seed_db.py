import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from projects.models import ProjectCategory, Project
from gallery.models import ArtworkCategory, Artwork
from articles.models import Article, Exhibition
from leads.models import Lead
from datetime import date

User = get_user_model()

# 1. Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gbstudio.ru', 'admin2026')
    print("Superuser created: admin / admin2026")
else:
    print("Superuser already exists")

# 2. Project Categories
cat_horeca, _ = ProjectCategory.objects.get_or_create(name='Гостиничный сектор (HoReCa)', slug='horeca', order=1)
cat_corp, _ = ProjectCategory.objects.get_or_create(name='Штаб-квартиры и корпоративные офисы', slug='corporate', order=2)
cat_industrial, _ = ProjectCategory.objects.get_or_create(name='Производственные предприятия и холдинги', slug='industrial', order=3)
cat_residence, _ = ProjectCategory.objects.get_or_create(name='Элитная недвижимость и пентхаусы', slug='residential', order=4)

# 3. Projects
if not Project.objects.exists():
    Project.objects.create(
        title='Реновация лобби и представительских зон пятизвездочного отеля The Oro',
        slug='hotel-the-oro-lobby',
        category=cat_horeca,
        client_name='The Oro Hospitality Group',
        location='Москва, Центр',
        area_sqm=1850,
        year=2025,
        duration='3.5 месяца',
        short_description='Комплексный fit-out входной группы, лобби-бара и лаунж-зон. Создание монументальной скульптурной волны из авторской известковой штукатурки с криволинейной подсветкой.',
        scope_of_work='Инженерный демонтаж и усиление конструкций; Скульптурные рельефные стены ручной работы; Бесшовные полы терраццо с латунной расшивкой; Изготовление стойки ресепшн из цельного мрамора Calacatta; Комплексный светодизайн',
        image_url='/static/images/case_hotel.jpg',
        is_featured=True,
        order=1
    )

    Project.objects.create(
        title='Штаб-квартира и совет директоров инвестиционной корпорации Apex Global',
        slug='apex-global-headquarters',
        category=cat_corp,
        client_name='Apex Capital Partners',
        location='Москва-Сити',
        area_sqm=920,
        year=2024,
        duration='2.5 месяца',
        short_description='Премиальная отделка VIP-этажа: переговорная зала на 16 персон с акцентной фактурной стеной "Антрацитовый срез", стеклянными акустическими перегородками и авторским столом из массива дуба.',
        scope_of_work='Комплексный fit-out под ключ; Акустическая подготовка и звукоизоляция 52 дБ; Авторская декоративная стена с графитовым пигментом; Изготовление переговорного стола 5.4 м из массива дуба и латуни; Монтаж скрытого мультимедиа-оборудования',
        image_url='/static/images/case_office.jpg',
        is_featured=True,
        order=2
    )

    Project.objects.create(
        title='Атриум и представительский блок машиностроительного кластера',
        slug='industrial-holding-atrium',
        category=cat_industrial,
        client_name='ПАО "ТехноМаш"',
        location='Калужская область',
        area_sqm=3400,
        year=2024,
        duration='5 месяцев',
        short_description='Капитальная реновация административно-бытового корпуса промышленного предприятия. Индустриальная эстетика, высокопрочные износостойкие покрытия и монументальные акценты.',
        scope_of_work='Замена всех инженерных сетей (ОВ, ВК, ЭОМ); Антивандальные авторские покрытия стен с устойчивостью к истиранию 50 000 циклов; Промышленные полимер-бетонные полы; Зонирование холлов и переговорных',
        image_url='/static/images/hero.jpg',
        is_featured=True,
        order=3
    )
    print("B2B Projects seeded")

# 4. Artwork Categories
cat_canvas, _ = ArtworkCategory.objects.get_or_create(name='Живопись на холсте', slug='paintings', order=1)
cat_ceramics, _ = ArtworkCategory.objects.get_or_create(name='Скульптурная керамика', slug='ceramics', order=2)
cat_graphics, _ = ArtworkCategory.objects.get_or_create(name='Авторская графика', slug='graphics', order=3)

# 5. Artworks (Architectural Luxury & Modern Art Authority, Anti-Neuroslop)
artworks_data = [
    {
        'title': 'Композиция №14: Терра',
        'slug': 'composition-14-terra',
        'category': cat_canvas,
        'year': 2024,
        'dimensions': '165 × 140 см',
        'medium': 'Холст, масло, фактурная паста, мастихин',
        'status': 'available',
        'price': '380 000 ₽',
        'curator_note': 'Крупноформатная станковая работа с плотной рельефной поверхностью. Многослойное нанесение охристых, песочных и графитовых оттенков создает глубокую осязаемую фактуру.',
        'image_url': '/static/images/art_canvas.jpg',
        'is_featured': True,
        'order': 1
    },
    {
        'title': 'Ваза «Фактура земли»',
        'slug': 'vase-texture-of-earth',
        'category': cat_ceramics,
        'year': 2025,
        'dimensions': 'h: 46 см, d: 34 см',
        'medium': 'Шамотная глина, ручная лепка, кракле-глазурь, обжиг 1250°C',
        'status': 'available',
        'price': '195 000 ₽',
        'curator_note': 'Авторский скульптурный объект из крупнозернистого шамота. Естественные микротрещины и минеральный цвет глины подчеркивают первозданную красоту материала.',
        'image_url': '/static/images/art_ceramic.jpg',
        'is_featured': True,
        'order': 2
    },
    {
        'title': 'Графический лист №08',
        'slug': 'graphic-sheet-08',
        'category': cat_graphics,
        'year': 2024,
        'dimensions': '70 × 50 см (дубовый багет, музейное стекло)',
        'medium': 'Хлопковая бумага ручного отлива, тушь, графит',
        'status': 'available',
        'price': '85 000 ₽',
        'curator_note': 'Камерная графическая серия на фактурной бумаге с необрезным краем. Четкие линейные ритмы и тональные заливки тушью.',
        'image_url': '/static/images/art_graphics.jpg',
        'is_featured': True,
        'order': 3
    }
]

# Clean up legacy neuroslop records
Artwork.objects.filter(slug__in=['palimpsest-street-layer-7', 'tectonic-rupture-ceramic', 'architectural-matrix-4']).delete()

for art in artworks_data:
    Artwork.objects.update_or_create(
        slug=art['slug'],
        defaults=art
    )
print("Artworks seeded cleanly")

# 6. Exhibitions
exhibitions_data = [
    {
        'title': 'Материал и форма',
        'venue': 'Центр современного искусства «Винзавод»',
        'city': 'Москва',
        'year': 2025,
        'dates': 'Май — июнь 2025',
        'exhibition_type': 'Персональная выставка',
        'status': 'upcoming',
        'description': 'Масштабный проект, объединяющий станковую живопись, монументальные фрагменты интерьерных фактур и скульптурную керамику мастера.',
        'order': 1
    },
    {
        'title': 'Современные фактуры',
        'venue': 'Галерея «Триумф»',
        'city': 'Москва',
        'year': 2024,
        'dates': 'Октябрь 2024',
        'exhibition_type': 'Групповая выставка',
        'status': 'past',
        'description': 'Экспозиция работ, исследующих тактильность и трансформацию урбанистических материалов в выставочном контексте.',
        'order': 2
    },
    {
        'title': 'Уличная волна: От эскиза к монументу',
        'venue': 'Севкабель Порт',
        'city': 'Санкт-Петербург',
        'year': 2023,
        'dates': 'Июль 2023',
        'exhibition_type': 'Кураторский проект',
        'status': 'past',
        'description': 'Исторический срез пионеров российского уличного искусства и их эволюции в станковое и монументальное искусство.',
        'order': 3
    }
]

# Clean up legacy neuroslop exhibitions
Exhibition.objects.filter(title__icontains='Археология').delete()
Exhibition.objects.filter(title__icontains='Теория Стен').delete()

for exh in exhibitions_data:
    Exhibition.objects.update_or_create(
        title=exh['title'],
        defaults=exh
    )
print("Exhibitions seeded cleanly")

# 7. Articles
if not Article.objects.exists():
    Article.objects.create(
        title='Почему отели 5* и флагманские офисы выбирают авторские фактуры вместо стандартных панелей',
        slug='author-surfaces-for-luxury-hotels',
        tag='Fit-Out Экспертиза',
        summary='Разбираем экономику и эстетику монументальных покрытий: как бесшовные авторские стены сокращают затраты на эксплуатацию и повышают капитализацию коммерческого объекта.',
        content='<p>В сегменте коммерческой недвижимости представительского класса типовые отделочные материалы быстро устаревают морально и физически. Авторские минеральные покрытия на основе микроцемента, извести и кварца обладают антивандальной стойкостью до 15 лет и не требуют стыковочных швов...</p>',
        image_url='/static/images/case_hotel.jpg',
        read_time='5 мин',
        published_date=date(2025, 1, 15),
        is_published=True
    )
    Article.objects.create(
        title='Генезис формы: 25 лет от баллона с краской до монументальных интерьерных объемов',
        slug='genesis-from-spraycan-to-architectural-volumes',
        tag='Манифест мастера',
        summary='Александр Попыкин рассказывает об уроках уличной волны 1998 года, работе с пропорциями архитектурных объемов и создании уникальных фактурных формул.',
        content='<p>Уличное искусство учит мгновенно чувствовать масштаб. Стена высотой в 6 метров не прощает ошибок в композиции. Этот опыт мы перенесли в 2011 году в интерьеры крупных объектов...</p>',
        image_url='/static/images/hero.jpg',
        read_time='6 мин',
        published_date=date(2024, 11, 20),
        is_published=True
    )
    print("Articles seeded")

# 8. Sample Leads in CRM
if not Lead.objects.exists():
    Lead.objects.create(
        name='Константин Романов',
        company='Девелопмент Групп «Северный Квартал»',
        phone='+7 (916) 450-22-11',
        email='romanov@nordquarter.ru',
        object_type='Девелопмент / Лобби и МОП ЖК',
        area_range='1500–5000 м²',
        service_needed='Комплексный fit-out под ключ + авторские фактурные стены входных групп',
        timeline='В течение 1-3 месяцев',
        estimated_cost='от 25 000 000 ₽',
        message='Необходима комплексная отделка 3 входных лобби в жилом комплексе премиум-класса. Ищем подрядчика со своим производством и художественным надзором.',
        source='quiz',
        status='audit_booked',
        manager_notes='Наталья: Выезд главного инженера на объект согласован на вторник 11:00. Взять планшетный бокс с образцами фактур для архитектора проекта.'
    )
    Lead.objects.create(
        name='Елена Савельева',
        company='Архитектурное бюро «Форма и Пространство»',
        phone='+7 (925) 880-99-33',
        email='elena@form-arch.com',
        object_type='Бутик-отель / Ресторан',
        area_range='500–1500 м²',
        service_needed='Заказ Sample Box с выкрасами фактур под проект отеля в Сочи',
        timeline='Стадия проектирования / Тендер',
        estimated_cost='12 000 000 ₽',
        source='sample_box',
        status='kp_sent',
        manager_notes='Наталья: Sample Box отправлен СДЭКом. Каталог и прайс-лист высланы на почту.'
    )
    print("Leads seeded")

print("All seed data created successfully!")
