from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import re
from .models import ClientAccount, ProjectContract, ProjectStage, StageUpdatePhoto, ProjectDocument

def get_demo_context():
    """Fallback demo data for showcase and preview if no client is in database yet."""
    return {
        'client': {
            'full_name': 'Евгений Михайлович Воронов',
            'phone': '+7 (985) 211-40-55',
            'company': 'Частный заказчик / Пентхаус',
            'email': 'voronov.art@gmail.com',
        },
        'project': {
            'title': 'Пентхаус на Патриарших прудах, 240 м²',
            'contract_number': 'GB-2026/09-14',
            'address': 'Москва, Малый Козихинский пер., 12',
            'total_area': '240 м²',
            'total_amount': 850000,
            'paid_amount': 425000,
            'remaining_amount': 425000,
            'progress_percent': 65,
            'status_display': 'В активной работе',
            'lead_artisan': 'Александр Попыкин (Арт-директор)',
            'artisan_phone': '+7 (495) 890-44-22',
            'start_date': '15.09.2026',
            'estimated_completion': '25.10.2026',
        },
        'stages': [
            {
                'step_number': 1,
                'title': 'Выездной аудит и лазерный замер геометрии стен',
                'description': 'Инженерное обследование плоскостей, оценка влажности и несущей способности основания. Протокол замера утвержден.',
                'status': 'completed',
                'status_display': 'Завершен',
                'date_label': '18 сентября 2026',
            },
            {
                'step_number': 2,
                'title': 'Колеровка и согласование авторских образцов (Sample Box)',
                'description': 'Изготовление 4 планшетов с микроцементом и минеральным рельефом. Выбран оттенок «Теплый парижский травертин».',
                'status': 'completed',
                'status_display': 'Завершен',
                'date_label': '22 сентября 2026',
            },
            {
                'step_number': 3,
                'title': 'Адгезионная подготовка основания и армирование',
                'description': 'Нанесение эпоксидного праймера с кварцевым песком, армирование стеклосеткой примыканий в мокрых зонах.',
                'status': 'completed',
                'status_display': 'Завершен',
                'date_label': '26 сентября 2026',
            },
            {
                'step_number': 4,
                'title': 'Художественное нанесение 2 слоев микроцемента',
                'description': 'Ручная формовка минеральной фактуры шпателем, создание бесшовных переходов в мастер-спальне и гостиной.',
                'status': 'in_progress',
                'status_display': 'В работе сейчас',
                'date_label': 'В процессе (сдача слоя 03 октября)',
            },
            {
                'step_number': 5,
                'title': 'Финишная гидрофобизация, полиуретановый лак и сдача',
                'description': 'Нанесение двухкомпонентного матового защитного лака (Италия), проверка светотеневых углов и подписание КС-2.',
                'status': 'pending',
                'status_display': 'Ожидает начала',
                'date_label': '12–15 октября 2026',
            },
        ],
        'photos': [
            {
                'caption': 'Нанесение первого базового слоя микроцемента в гостиной зоне',
                'display_url': '/static/images/hero.jpg',
                'date': '28.09.2026',
            },
            {
                'caption': 'Подготовка образцов фактуры травертина в мастерской',
                'display_url': '/static/images/fresco_texture.jpg',
                'date': '24.09.2026',
            },
            {
                'caption': 'Декоративная расшивка стыков перед нанесением финиша',
                'display_url': '/static/images/restoration_craft.jpg',
                'date': '27.09.2026',
            },
        ],
        'documents': [
            {
                'title': 'Договор подряда №GB-2026/09-14 на выполнение декоративных работ',
                'doc_type_display': 'Договор подряда',
                'size_label': 'PDF, 1.8 МБ',
                'url': '#download-contract',
            },
            {
                'title': 'Согласованная смета и технологическая спецификация материалов',
                'doc_type_display': 'Смета и спецификация',
                'size_label': 'PDF, 850 КБ',
                'url': '#download-estimate',
            },
            {
                'title': 'Акт освидетельствования скрытых работ (грунтовка и армирование)',
                'doc_type_display': 'Акт скрытых работ',
                'size_label': 'PDF, 620 КБ',
                'url': '#download-act',
            },
            {
                'title': 'Официальный сертификат 5-летней гарантии Golden Brush Studio',
                'doc_type_display': 'Гарантийный сертификат',
                'size_label': 'PDF, 410 КБ',
                'url': '#download-warranty',
            },
        ],
        'tier': {
            'code': 'resident',
            'name': '02. Постоянный партнер (Resident)',
            'client_type_display': 'Архитектурное бюро / Дизайн-студия',
            'discount_materials': 10,
            'discount_works': 5,
            'completed_projects': 1,
            'current_project_number': 2,
            'next_tier_label': 'До статуса «Корпоративный клуб» (материалы 15% / работы 10%)',
            'projects_needed': 1,
            'progress_pct': 66,
            'max_tier': False,
        },
        'has_active_project': True,
        'just_registered': False,
    }

def portal_login(request):
    error = None
    active_tab = request.GET.get('tab', 'login')
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        pin = request.POST.get('pin', '').strip()
        demo = request.POST.get('demo', '')

        # 1. Явный демо-доступ для демонстрации интерфейса
        if demo or phone.lower() == 'demo':
            request.session['client_phone'] = 'demo'
            return redirect('portal:dashboard')

        # 2. Поиск реального договора по номеру телефона
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            client = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()
        else:
            client = None

        if client:
            # Если у клиента установлен персональный PIN, требуем точного соответствия
            if client.access_pin and client.access_pin != pin:
                return render(request, 'portal/login.html', {
                    'error': 'Неверный PIN-код быстрого доступа. Проверьте 4 цифры из SMS или договора.',
                    'active_tab': 'login',
                    'login_phone': phone,
                })
            request.session['client_phone'] = client.phone
            return redirect('portal:dashboard')
        else:
            return render(request, 'portal/login.html', {
                'error': 'Объект с данным номером пока не зарегистрирован. Перейдите во вкладку «Регистрация», чтобы зафиксировать накопительную скидку на материалы и работы.',
                'active_tab': 'login',
                'login_phone': phone,
            })

    return render(request, 'portal/login.html', {'active_tab': active_tab})

def portal_register(request):
    """Регистрация нового заказчика / архитектурного партнера с фиксацией скидки."""
    if request.method == 'POST':
        # Защита от спам-ботов
        if request.POST.get('website_check'):
            return redirect('portal:login')

        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip()
        email = request.POST.get('email', '').strip()
        client_type = request.POST.get('client_type', 'architect').strip()
        pin = request.POST.get('pin', '').strip() or '1234'

        if not full_name or not phone:
            return render(request, 'portal/login.html', {
                'reg_error': 'Пожалуйста, укажите имя контактного лица и номер телефона.',
                'active_tab': 'register',
                'reg_data': request.POST,
            })

        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10:
            return render(request, 'portal/login.html', {
                'reg_error': 'Номер телефона должен содержать минимум 10 цифр.',
                'active_tab': 'register',
                'reg_data': request.POST,
            })

        # Проверяем, существует ли уже клиент с таким номером
        existing_client = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()
        if existing_client:
            request.session['client_phone'] = existing_client.phone
            return redirect('portal:dashboard')

        # Создаем профиль заказчика
        client = ClientAccount.objects.create(
            full_name=full_name,
            phone=phone,
            company=company,
            email=email if email else None,
            client_type=client_type,
            access_pin=pin,
        )

        # Создаем лид для Натальи и Александра в CRM
        try:
            from leads.models import Lead
            Lead.objects.create(
                name=full_name,
                company=company,
                phone=phone,
                email=email,
                source='portal_reg',
                object_type=f"Партнерский кабинет ({client.get_client_type_display()})",
                service_needed="Накопительная скидка: 5% на материалы со старта",
                message=f"Клиент зарегистрировался на сайте. Статус: {client.tier_name}. ПИН: {pin}. Контакт: {phone}",
            )
        except Exception:
            pass

        request.session['client_phone'] = client.phone
        request.session['just_registered'] = True
        return redirect('portal:dashboard')

    return render(request, 'portal/login.html', {'active_tab': 'register'})

def portal_dashboard(request):
    phone = request.session.get('client_phone')
    just_registered = request.session.pop('just_registered', False)
    
    if not phone or phone == 'demo':
        demo_ctx = get_demo_context()
        demo_ctx['just_registered'] = just_registered
        return render(request, 'portal/dashboard.html', {'data': demo_ctx, 'is_demo': True})

    client = ClientAccount.objects.filter(phone=phone).first()
    if not client:
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            client = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()

    if not client:
        demo_ctx = get_demo_context()
        demo_ctx['just_registered'] = just_registered
        return render(request, 'portal/dashboard.html', {'data': demo_ctx, 'is_demo': True})

    tier_info = client.next_tier_info
    tier_data = {
        'code': client.tier_code,
        'name': client.tier_name,
        'client_type_display': client.get_client_type_display(),
        'discount_materials': client.discount_materials,
        'discount_works': client.discount_works,
        'completed_projects': client.total_projects_count,
        'current_project_number': client.total_projects_count + 1,
        'next_tier_label': tier_info['label'],
        'projects_needed': tier_info['projects_needed'],
        'progress_pct': tier_info['progress_pct'],
        'max_tier': tier_info['max_tier'],
    }

    project = client.projects.first()
    if not project:
        context = {
            'client': client,
            'tier': tier_data,
            'project': None,
            'stages': [],
            'photos': [],
            'documents': [],
            'is_demo': False,
            'has_active_project': False,
            'just_registered': just_registered,
        }
        return render(request, 'portal/dashboard.html', {'data': context, 'is_demo': False})

    stages = project.stages.all().order_by('step_number')
    photos = project.photos.all()
    documents = project.documents.all()

    context = {
        'client': client,
        'tier': tier_data,
        'project': project,
        'stages': stages,
        'photos': photos,
        'documents': documents,
        'is_demo': False,
        'has_active_project': True,
        'just_registered': just_registered,
    }
    return render(request, 'portal/dashboard.html', {'data': context, 'is_demo': False})

def portal_logout(request):
    request.session.flush()
    return redirect('portal:login')
