from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import re

from projects.models import Project, ProjectCategory
from gallery.models import Artwork, ArtworkCategory
from articles.models import Article, Exhibition
from materials.models import DecorativeMaterial
from main.models import Partner, HomePageConfig
from leads.models import Lead
from leads.services import send_telegram_notification

def index(request):
    """Главная страница: B2B Fit-Out генподряд, Конфигуратор сметы, Кейсы, Мастерская и Арт-Галерея"""
    projects = Project.objects.filter(is_featured=True).select_related('category')
    categories = ProjectCategory.objects.all()
    artworks = Artwork.objects.filter(is_featured=True).select_related('category')[:4]
    articles = Article.objects.filter(is_published=True, is_featured=True)[:3]
    exhibitions = Exhibition.objects.all()[:4]
    materials = DecorativeMaterial.objects.filter(is_active=True, show_in_calculator=True).order_by('order', 'id')
    partners = Partner.objects.filter(is_active=True).order_by('order', 'id')
    home_config = HomePageConfig.get_solo()
    
    context = {
        'projects': projects,
        'categories': categories,
        'artworks': artworks,
        'articles': articles,
        'exhibitions': exhibitions,
        'materials': materials,
        'partners': partners,
        'home_config': home_config,
    }
    return render(request, 'index.html', context)

def gallery_view(request):
    """Выделенная страница Арт-Галереи Александра Попыкина: 3 направления (Живопись и графика, Керамика, Арт-объекты)"""
    category_slug = request.GET.get('category', '').strip()
    all_artworks = list(Artwork.objects.all().select_related('category').order_by('order', 'id'))
    
    cat_keys = [
        ('paintings-graphics', 'Живопись и графика', 'Крупноформатная станковая живопись на льняных холстах и камерная графика тушью.'),
        ('ceramics', 'Керамика', 'Скульптурные интерьерные вазы и сосуды из шамотной глины, высокотемпературный обжиг.'),
        ('art-objects', 'Арт-объекты', 'Монолитные арт-столики из микроцемента, рельефные стеновые панно и малые архитектурные формы.')
    ]
    
    flagship_categories = []
    for slug, title, desc in cat_keys:
        cat_items = [a for a in all_artworks if a.category.slug == slug]
        if cat_items:
            items_json = []
            for a in cat_items:
                items_json.append({
                    'id': a.id,
                    'title': a.title,
                    'slug': a.slug,
                    'image': a.get_image,
                    'year': f"{a.year} г.",
                    'medium': a.medium,
                    'dimensions': a.dimensions,
                    'curator_note': a.curator_note,
                    'price': a.formatted_price,
                    'category_name': a.category.name,
                })
            flagship_categories.append({
                'slug': slug,
                'name': title,
                'description': desc,
                'artworks': cat_items,
                'count': len(cat_items),
                'primary_artwork': cat_items[0],
                'items_json': json.dumps(items_json),
            })

    filtered_artworks = all_artworks
    if category_slug:
        filtered_artworks = [a for a in all_artworks if a.category.slug == category_slug]

    categories = ArtworkCategory.objects.all()
    home_config = HomePageConfig.get_solo()
    
    context = {
        'artworks': filtered_artworks,
        'all_artworks': all_artworks,
        'flagship_categories': flagship_categories,
        'categories': categories,
        'current_category': category_slug,
        'home_config': home_config,
    }
    return render(request, 'gallery.html', context)

def contacts_view(request):
    """Выделенная страница контактов студии Golden Brush Studio"""
    home_config = HomePageConfig.get_solo()
    context = {
        'home_config': home_config,
    }
    return render(request, 'contacts.html', context)

def journal_list(request):
    """Журнал Мастерской / Atelier Journal: авторские заметки, Work in Progress, фактуры и события"""
    category_filter = request.GET.get('category', '').strip()
    articles = Article.objects.filter(is_published=True)
    if category_filter:
        articles = articles.filter(category=category_filter)
        
    categories = Article.CATEGORY_CHOICES
    
    context = {
        'articles': articles,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'journal.html', context)

def projects_list(request):
    """Раздел «Наши проекты»: 3 флагманских направления (Бары и рестораны, Отели, Частные резиденции) + полный каталог"""
    category_slug = request.GET.get('category', '').strip()
    all_projects = list(Project.objects.all().select_related('category').order_by('order', 'id'))
    
    cat_keys = [
        ('bars-restaurants', 'Бары и рестораны', 'Культовые сетевые бары Coyote Ugly (4 заведения), ресторан «Горыныч» и концептуальные гастро-проекты.'),
        ('hotels', 'Отели', 'Реновация лобби и представительских сьютов бутик-отелей: The Oro, Метрополь Арт.'),
        ('residences', 'Частные резиденции', 'Комплексная отделка вилл и пентхаусов: Серебряный Бор, Патриаршие пруды, загородные усадьбы.')
    ]
    
    flagship_categories = []
    for slug, title, desc in cat_keys:
        cat_projects = [p for p in all_projects if p.category.slug == slug]
        if cat_projects:
            items_json = []
            for p in cat_projects:
                items_json.append({
                    'id': p.id,
                    'title': p.title,
                    'slug': p.slug,
                    'url': p.get_absolute_url(),
                    'image': p.get_image,
                    'location': p.location,
                    'area': f"{p.area_sqm} м²",
                    'duration': p.duration,
                    'short_desc': p.short_description,
                    'scope': p.get_scope_list()[:3],
                    'category_name': p.category.name,
                })
            flagship_categories.append({
                'slug': slug,
                'name': title,
                'description': desc,
                'projects': cat_projects,
                'count': len(cat_projects),
                'primary_project': cat_projects[0],
                'items_json': json.dumps(items_json),
            })
            
    filtered_projects = all_projects
    if category_slug:
        filtered_projects = [p for p in all_projects if p.category.slug == category_slug]

    categories = ProjectCategory.objects.all()

    context = {
        'projects': filtered_projects,
        'all_projects': all_projects,
        'flagship_categories': flagship_categories,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'projects_list.html', context)

def project_detail(request, slug):
    """Детальная страница кейса / объекта"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(id=project.id)[:3]
    return render(request, 'project_detail.html', {'project': project, 'related_projects': related_projects})

def article_detail(request, slug):
    """Страница записи Журнала Мастерской / публикации"""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    process_images = article.process_images.all()
    related_articles = Article.objects.filter(is_published=True).exclude(id=article.id)[:3]
    return render(request, 'article_detail.html', {
        'article': article,
        'process_images': process_images,
        'related_articles': related_articles
    })

def validate_and_clean_lead_data(data):
    """
    Валидация телефона и фильтрация спам-ботов через honeypot-ловушку.
    Возвращает: (is_valid, cleaned_phone, is_bot, error_msg)
    """
    # 1. Проверка поля-ловушки honeypot (скрыто для человека, но заполняется спам-ботами)
    honeypot = data.get('website_check', '') or data.get('website_url_check', '')
    if honeypot and str(honeypot).strip():
        return False, None, True, 'Spam detected'

    name = str(data.get('name', '')).strip()
    phone_raw = str(data.get('phone', '')).strip()

    if not name:
        return False, None, False, 'Пожалуйста, укажите контактное имя'
    if not phone_raw:
        return False, None, False, 'Пожалуйста, укажите контактный телефон'

    # 2. Очистка и валидация телефона
    digits = re.sub(r'\D', '', phone_raw)
    if len(digits) < 10 or len(digits) > 15:
        return False, None, False, 'Пожалуйста, введите корректный номер телефона (не менее 10 цифр)'

    # Исключение явных фиктивных номеров вида 0000000000, 1111111111
    if len(set(digits)) <= 2:
        return False, None, False, 'Пожалуйста, укажите действительный номер телефона'

    # Нормализация формата: +7 (XXX) XXX-XX-XX
    if len(digits) == 11 and digits[0] in ('7', '8'):
        cleaned_phone = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 10:
        cleaned_phone = f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    else:
        cleaned_phone = f"+{digits}"

    return True, cleaned_phone, False, None


@require_POST
def submit_quiz_lead(request):
    """Прием заявки из интерактивного конфигуратора предварительного расчета сметы объекта"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Заявка принята!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        company = data.get('company', '').strip()
        email = data.get('email', '').strip()
        object_type = data.get('object_type', '').strip()
        area_range = data.get('area_range', '').strip()
        service_needed = data.get('service_needed', '').strip()
        timeline = data.get('timeline', '').strip()
        message = data.get('message', '').strip()
        estimated_cost = data.get('estimated_cost', '').strip()
        source = data.get('source', 'quiz')

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            company=company,
            email=email,
            object_type=object_type,
            area_range=area_range,
            service_needed=service_needed,
            timeline=timeline,
            estimated_cost=estimated_cost,
            message=message,
            source=source,
            status='new',
            manager_notes='Заявка из конфигуратора сметы Fit-Out объекта. Требуется обратный звонок руководителя проекта.'
        )

        # Мгновенная отправка пуша Наталье в Telegram
        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Заявка успешно принята! Руководитель коммерческого направления Наталья свяжется с вами в ближайшее время.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def submit_sample_box(request):
    """Заказ физического Sample Box фактурных покрытий для архитекторов и девелоперов"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Заказ принят!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        company = data.get('company', '').strip()
        address = data.get('address', '').strip()

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            company=company,
            message=f"Заказ Architect Sample Box. Адрес доставки кейса: {address}",
            source='sample_box',
            status='new',
            manager_notes='Наталья: Заказ образцов фактур для архитектора/дизайнера. Подготовить бокс и отправить курьером/СДЭК.'
        )

        # Мгновенная отправка пуша в Telegram
        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Заказ кейса образцов принят! Мы свяжемся с вами для подтверждения курьерской доставки.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def submit_art_inquiry(request):
    """Запрос на резервирование произведения искусства или авторский проект монументального панно"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Запрос принят!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        artwork_title = data.get('artwork_title', '').strip()
        artwork_id = data.get('artwork_id', '').strip()
        message = data.get('message', '').strip()

        lead_message = f"Резерв произведения: «{artwork_title}» (ID #{artwork_id})."
        if message:
            lead_message += f"\nПожелания заказчика: {message}"

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            message=lead_message,
            source='art_inquiry',
            status='new',
            manager_notes=f'Запрос на резерв произведения Саши Попыкина: «{artwork_title}». Согласовать условия показа в мастерской.'
        )

        # Мгновенная отправка пуша в Telegram
        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': f'Запрос на резервирование «{artwork_title}» принят! Мы свяжемся с вами для согласования деталей.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def submit_art_fitting(request):
    """Заявка на бесплатную примерку картин в интерьере заказчика"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Заявка принята!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        address = data.get('address', '').strip()
        artworks_selected = data.get('artworks_selected', '').strip()
        message = data.get('message', '').strip()

        lead_msg = f"Заявка на БЕСПЛАТНУЮ ПРИМЕРКУ КАРТИН В ИНТЕРЬЕРЕ.\nАдрес доставки: {address or 'Не указан'}\nПолотна для примерки: {artworks_selected or 'Подборка куратора'}"
        if message:
            lead_msg += f"\nПожелания / интерьер: {message}"

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            message=lead_msg,
            source='art_fitting',
            status='new',
            manager_notes='Бесплатная примерка картин на объекте. Согласовать удобное время визита и отобрать полотна в мастерской.'
        )

        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Заявка на примерку полотен принята! Мы свяжемся с вами в течение 15 минут для согласования времени доставки.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def submit_calculator_lead(request):
    """Заявка из калькулятора расчета стоимости покрытий по площади стен"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Расчет принят!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        material = data.get('material', '').strip()
        area_sqm = data.get('area_sqm', '').strip()
        estimated_cost = data.get('estimated_cost', '').strip()
        message = data.get('message', '').strip()

        lead_msg = f"Расчет из калькулятора материалов:\nПокрытие: {material}\nПлощадь стен: {area_sqm} м²\nОриентировочная сумма: {estimated_cost}"
        if message:
            lead_msg += f"\nКомментарий: {message}"

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            service_needed=material,
            area_range=f"{area_sqm} м²",
            estimated_cost=estimated_cost,
            message=lead_msg,
            source='calculator',
            status='new',
            manager_notes='Расчет по калькулятору поверхностей. Согласовать выезд технолога с планшетами выкрасов.'
        )

        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Расчет зафиксирован! Мы свяжемся с вами для подтверждения параметров и бесплатного предоставления образцов.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def fonts_presentation(request):
    """Интерактивная презентация шрифтовой айдентики для согласования с заказчиком"""
    return render(request, 'fonts_presentation.html')


def partners_view(request):
    """Выделенная страница Партнёрской программы: архитекторам, дизайнерам, девелоперам и заказ красок со скидкой"""
    partners = Partner.objects.filter(is_active=True).order_by('order', 'id')
    home_config = HomePageConfig.get_solo()
    context = {
        'partners': partners,
        'home_config': home_config,
    }
    return render(request, 'partners.html', context)


@require_POST
def submit_partner_inquiry(request):
    """Заявка на партнерство от архитектора / дизайнера / девелопера"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Партнёрская заявка принята!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        company = data.get('company', '').strip()
        role = data.get('role', 'Архитектор / Дизайнер').strip()
        message = data.get('message', '').strip()

        lead_msg = f"Партнёрская заявка:\nРоль: {role}\nБюро/Компания: {company}"
        if message:
            lead_msg += f"\nПожелания / проекты: {message}"

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            company=company,
            service_needed=f"Партнёрство: {role}",
            message=lead_msg,
            source='sample_box',
            status='new',
            manager_notes='Запрос на партнёрскую программу. Направить Sample Box и условия агентского вознаграждения.'
        )

        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Партнёрская заявка принята! Мы свяжемся с вами для передачи каталогов и согласования доставки Sample Box.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def submit_paint_order(request):
    """Заказ интерьерных красок официального партнера с персональной клубной скидкой Golden Brush (12%)"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        is_valid, cleaned_phone, is_bot, error_msg = validate_and_clean_lead_data(data)
        if is_bot:
            return JsonResponse({'success': True, 'lead_id': 0, 'message': 'Заказ на краску зафиксирован!'})
        if not is_valid:
            return JsonResponse({'success': False, 'error': error_msg}, status=400)

        name = data.get('name', '').strip()
        phone = cleaned_phone
        paint_brand = data.get('paint_brand', 'Премиальная матовая интерьерная краска (Италия)').strip()
        liters = data.get('liters', '10').strip()
        area = data.get('area', '60').strip()
        color_code = data.get('color_code', 'Подбор по RAL / NCS').strip()
        discount_price = data.get('discount_price', '').strip()
        address = data.get('address', '').strip()

        order_msg = (
            f"Заказ красок партнера со скидкой Golden Brush (12%):\n"
            f"Литраж: {liters} л (на площадь ~{area} м²)\n"
            f"Цвет / Колеровка: {color_code}\n"
            f"Ориентировочная сумма со скидкой: {discount_price}\n"
            f"Адрес доставки / Шоурум: {address}"
        )

        lead = Lead.objects.create(
            name=name,
            phone=phone,
            service_needed=f"Заказ красок партнера: {liters} л",
            area_range=f"{area} м²",
            estimated_cost=discount_price,
            message=order_msg,
            source='quick_call',
            status='new',
            manager_notes='Заказ краски партнера по клубной скидке Golden Brush. Передать заявку в салон красок для комплектации.'
        )

        send_telegram_notification(lead)

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Заказ на краску со скидкой 12% зафиксирован! Менеджер партнерского салона свяжется для подтверждения колеровки и доставки.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)




