from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

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
    """Выделенная страница Арт-Галереи Александра Попыкина"""
    artworks = Artwork.objects.all().select_related('category')
    categories = ArtworkCategory.objects.all()
    exhibitions = Exhibition.objects.all()
    
    context = {
        'artworks': artworks,
        'categories': categories,
        'exhibitions': exhibitions,
    }
    return render(request, 'gallery.html', context)

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

def project_detail(request, slug):
    """Детальная страница B2B кейса"""
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

@require_POST
def submit_quiz_lead(request):
    """Прием заявки из интерактивного конфигуратора предварительного расчета сметы объекта"""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        company = data.get('company', '').strip()
        email = data.get('email', '').strip()
        object_type = data.get('object_type', '').strip()
        area_range = data.get('area_range', '').strip()
        service_needed = data.get('service_needed', '').strip()
        timeline = data.get('timeline', '').strip()
        message = data.get('message', '').strip()
        estimated_cost = data.get('estimated_cost', '').strip()
        source = data.get('source', 'quiz')

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, укажите контактное лицо и номер телефона'}, status=400)

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

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        company = data.get('company', '').strip()
        address = data.get('address', '').strip()

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Укажите ваше имя и телефон'}, status=400)

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

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        artwork_title = data.get('artwork_title', '').strip()
        artwork_id = data.get('artwork_id', '').strip()
        message = data.get('message', '').strip()

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, укажите имя и телефон для связи'}, status=400)

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

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        artworks_selected = data.get('artworks_selected', '').strip()
        message = data.get('message', '').strip()

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Укажите ваше имя и телефон'}, status=400)

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

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        material = data.get('material', '').strip()
        area_sqm = data.get('area_sqm', '').strip()
        estimated_cost = data.get('estimated_cost', '').strip()
        message = data.get('message', '').strip()

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Укажите ваше имя и телефон'}, status=400)

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


