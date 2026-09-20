import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from gallery.models import ArtworkCategory, Artwork
from articles.models import Article, Exhibition
from projects.models import ProjectCategory, Project

# Clean update of Artworks
Artwork.objects.all().delete()

cat_canvas = ArtworkCategory.objects.get(slug='paintings')
cat_ceramics = ArtworkCategory.objects.get(slug='ceramics')
cat_graphics = ArtworkCategory.objects.get(slug='graphics')

Artwork.objects.create(
    title='Композиция №14: Терра',
    slug='composition-14-terra',
    category=cat_canvas,
    year=2024,
    dimensions='165 × 140 см',
    medium='Холст, масло, фактурная паста, мастихин',
    status='available',
    price='380 000 ₽',
    curator_note='Крупноформатная станковая работа с плотной рельефной поверхностью. Многослойное нанесение охристых, песочных и графитовых оттенков создает глубокую осязаемую фактуру.',
    image_url='/static/images/art_canvas.jpg',
    is_featured=True,
    order=1
)

Artwork.objects.create(
    title='Ваза «Фактура земли»',
    slug='vase-earth-texture',
    category=cat_ceramics,
    year=2025,
    dimensions='h: 46 см, d: 34 см',
    medium='Шамотная глина, ручная лепка, кракле-глазурь, обжиг 1250°C',
    status='available',
    price='195 000 ₽',
    curator_note='Авторский скульптурный объект из крупнозернистого шамота. Естественные микротрещины и минеральный цвет глины подчеркивают первозданную красоту материала.',
    image_url='/static/images/art_ceramic.jpg',
    is_featured=True,
    order=2
)

Artwork.objects.create(
    title='Графический лист №08',
    slug='graphic-sheet-08',
    category=cat_graphics,
    year=2024,
    dimensions='70 × 50 см (дубовый багет, музейное стекло)',
    medium='Хлопковая бумага ручного отлива, тушь, графит',
    status='available',
    price='85 000 ₽',
    curator_note='Камерная графическая серия на фактурной бумаге с необрезным краем. Четкие линейные ритмы и тональные заливки тушью.',
    image_url='/static/images/art_graphics.jpg',
    is_featured=True,
    order=3
)

# Clean update of Exhibitions
Exhibition.objects.all().delete()
Exhibition.objects.create(
    title='Материал и форма',
    venue='Центр современного искусства «Винзавод»',
    city='Москва',
    year=2025,
    dates='Май — июнь 2025',
    exhibition_type='Персональная выставка',
    status='upcoming',
    description='Экспозиция станковой живописи, скульптурной керамики и авторских панно мастера.',
    order=1
)
Exhibition.objects.create(
    title='Современные фактуры',
    venue='Галерея «Триумф»',
    city='Москва',
    year=2024,
    dates='Октябрь 2024',
    exhibition_type='Групповая выставка',
    status='past',
    description='Работы современных художников, исследующих материальность и фактурные свойства поверхностей.',
    order=2
)
Exhibition.objects.create(
    title='Уличная волна: От эскиза к монументу',
    venue='Севкабель Порт',
    city='Санкт-Петербург',
    year=2023,
    dates='Июль 2023',
    exhibition_type='Кураторский проект',
    status='past',
    description='Ретроспектива художников с бэкграундом в граффити конца 90-х и их развития в современном искусстве.',
    order=3
)

# Clean update of Articles
Article.objects.all().delete()
Article.objects.create(
    title='Авторские покрытия в коммерческих объектах: эстетика и долговечность',
    slug='decorative-surfaces-commercial-spaces',
    tag='Fit-Out практика',
    summary='Практический опыт применения бесшовных известковых и минеральных составов в интерьерах с высокой проходимостью: отели, холлы и переговорные.',
    content='<p>При отделке общественных зон и представительских помещений ключевым фактором становится баланс выразительного внешнего вида и эксплуатационной надежности. Авторские минеральные покрытия на известковой и микроцементной основе не имеют стыковочных швов, ремонтопригодны и со временем приобретают благородный вид натурального камня...</p>',
    image_url='/static/images/case_hotel.jpg',
    read_time='4 мин',
    published_date=django.utils.timezone.now().date(),
    is_published=True
)
Article.objects.create(
    title='От уличного райтинга 1998 года к монументальным архитектурным объемам',
    slug='evolution-street-to-architecture',
    tag='Мастерская',
    summary='Александр Попыкин о 25-летнем пути в искусстве, понимании масштаба больших стен и переходе к авторским интерьерным объектам с 2011 года.',
    content='<p>Опыт уличного искусства конца девяностых дал главное — мгновенное ощущение пропорций и масштаба. Когда перед тобой стена высотой в несколько метров, ты учишься работать всем телом и видеть композицию целиком. Этот навык стал фундаментом для работы с крупными коммерческими объектами и архитектурными объемами...</p>',
    image_url='/static/images/hero.jpg',
    read_time='5 мин',
    published_date=django.utils.timezone.now().date(),
    is_published=True
)

print("Database cleaned and updated with authentic content!")
