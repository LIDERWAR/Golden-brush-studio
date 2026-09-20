from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from projects.models import Project, ProjectCategory
from gallery.models import Artwork, ArtworkCategory
from articles.models import Article, Exhibition
from leads.models import Lead

def index(request):
    """Главная страница: B2B Fit-Out, Квиз-воронка, Кейсы, Презентация Ателье и Галереи"""
    projects = Project.objects.filter(is_featured=True).select_related('category')
    categories = ProjectCategory.objects.all()
    artworks = Artwork.objects.filter(is_featured=True).select_related('category')[:4]
    articles = Article.objects.filter(is_published=True)[:3]
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

def project_detail(request, slug):
    """Детальная страница B2B кейса"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(id=project.id)[:3]
    return render(request, 'project_detail.html', {'project': project, 'related_projects': related_projects})

def article_detail(request, slug):
    """Страница статьи / пресс-релиза"""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'article_detail.html', {'article': article})

@require_POST
def submit_quiz_lead(request):
    """Прием лида из интерактивного B2B квиза расчета объекта"""
    try:
        # Проверяем JSON или стандартный POST
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
            manager_notes='Лид поступил с сайта через квиз расчета объекта. Требуется обратный звонок в течение 15 минут.'
        )

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Заявка успешно принята! Руководитель B2B-направления Наталья свяжется с вами для уточнения деталей.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def submit_sample_box(request):
    """Заказ физического Sample Box фактурных покрытий для архитекторов и дизайнеров"""
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
            message=f"Заказ Architect Sample Box. Адрес доставки образцов: {address}",
            source='sample_box',
            status='new',
            manager_notes='Наталья: Заказ образцов для архитектора/дизайнера. Подготовить бокс и отправить курьером/СДЭК.'
        )

        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Заказ кейса образцов принят! Мы свяжемся с вами для подтверждения адреса доставки.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
