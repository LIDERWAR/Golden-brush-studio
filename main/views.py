from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from projects.models import Project, ProjectCategory
from gallery.models import Artwork, ArtworkCategory
from articles.models import Article, Exhibition
from leads.models import Lead
from leads.services import send_telegram_notification

def index(request):
    """Главная страница: B2B Fit-Out генподряд, Конфигуратор сметы, Кейсы, Мастерская и Арт-Галерея"""
    projects = Project.objects.filter(is_featured=True).select_related('category')
    categories = ProjectCategory.objects.all()
    artworks = Artwork.objects.filter(is_featured=True).select_related('category')[:4]
    articles = Article.objects.filter(is_published=True, is_featured=True)[:3]
    exhibitions = Exhibition.objects.all()[:4]
    
    context = {
        'projects': projects,
        'categories': categories,
        'artworks': artworks,
        'articles': articles,
        'exhibitions': exhibitions,
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

