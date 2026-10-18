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

from django.contrib.auth import authenticate, login as django_login, logout as django_logout

def check_is_master(request):
    """Проверка прав мастера / администратора мастерской (Александр Попыкин, Наталья, staff/superuser)."""
    if hasattr(request, 'user') and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return True
    if request.session.get('is_master_mode'):
        return True
    return False

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
            request.session['is_master_mode'] = False
            return redirect('portal:dashboard')

        # 2. Аутентификация администратора / мастера студии (Александр Попыкин, Наталья, admin)
        user = authenticate(request, username=phone, password=pin)
        if user is not None and (user.is_staff or user.is_superuser):
            django_login(request, user)
            request.session['is_master_mode'] = True
            request.session['client_phone'] = 'master'
            return redirect('portal:dashboard')

        # 3. Поиск реального договора по номеру телефона
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
            request.session['is_master_mode'] = False
            return redirect('portal:dashboard')
        else:
            return render(request, 'portal/login.html', {
                'error': 'Объект с данным номером пока не зарегистрирован. Перейдите во вкладку «Регистрация» или проверьте введенные данные.',
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
    is_master = check_is_master(request)
    all_clients = ClientAccount.objects.all().order_by('-created_at') if is_master else []
    just_registered = request.session.pop('just_registered', False)

    # Переключение клиента для режима Мастера
    if is_master:
        switch_id = request.GET.get('switch_client') or request.POST.get('switch_client')
        if switch_id:
            request.session['master_active_client_id'] = switch_id

    # Определение активного клиента
    client = None
    is_demo = False

    if is_master:
        active_id = request.session.get('master_active_client_id')
        if active_id == 'demo':
            is_demo = True
        elif active_id:
            try:
                client = ClientAccount.objects.filter(id=int(active_id)).first()
            except (ValueError, TypeError):
                client = None
        if not client and not is_demo:
            client = ClientAccount.objects.first()
            if client:
                request.session['master_active_client_id'] = client.id
            else:
                is_demo = True
    else:
        phone = request.session.get('client_phone')
        if not phone or phone == 'demo':
            is_demo = True
        else:
            client = ClientAccount.objects.filter(phone=phone).first()
            if not client:
                digits = re.sub(r'\D', '', phone)
                if len(digits) >= 10:
                    client = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()
            if not client:
                is_demo = True

    # Обработка действий Мастера (POST)
    if request.method == 'POST' and is_master:
        action = request.POST.get('action')

        if action == 'master_update_stage':
            stage_id = request.POST.get('stage_id')
            stage_status = request.POST.get('stage_status')
            try:
                stage = ProjectStage.objects.get(id=stage_id)
                stage.status = stage_status
                stage.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
                    return JsonResponse({'status': 'ok', 'stage_id': stage.id, 'new_status': stage.status, 'status_display': stage.get_status_display()})
            except ProjectStage.DoesNotExist:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax'):
                    return JsonResponse({'status': 'error', 'message': 'Этап не найден'}, status=404)
            return redirect('portal:dashboard')

        elif action == 'master_add_photo':
            if client and client.projects.exists():
                proj = client.projects.first()
                photo_file = request.FILES.get('photo_file')
                caption = request.POST.get('caption', '').strip()
                stage_id = request.POST.get('stage_id')
                stage = ProjectStage.objects.filter(id=stage_id, project=proj).first() if stage_id else None
                if photo_file:
                    StageUpdatePhoto.objects.create(
                        project=proj,
                        stage=stage,
                        image=photo_file,
                        caption=caption or 'Фотоотчет со стройки'
                    )
            return redirect('portal:dashboard')

        elif action == 'master_update_progress':
            if client and client.projects.exists():
                proj = client.projects.first()
                try:
                    pct = int(request.POST.get('progress_percent', proj.progress_percent))
                    proj.progress_percent = max(0, min(100, pct))
                except (ValueError, TypeError):
                    pass
                new_status = request.POST.get('status')
                if new_status in dict(ProjectContract.STATUS_CHOICES):
                    proj.status = new_status
                try:
                    total = float(request.POST.get('total_amount', proj.total_amount))
                    proj.total_amount = total
                except (ValueError, TypeError):
                    pass
                try:
                    paid = float(request.POST.get('paid_amount', proj.paid_amount))
                    proj.paid_amount = paid
                except (ValueError, TypeError):
                    pass
                proj.save()
            return redirect('portal:dashboard')

        elif action == 'master_add_stage':
            if client and client.projects.exists():
                proj = client.projects.first()
                title = request.POST.get('title', '').strip()
                desc = request.POST.get('description', '').strip()
                date_lbl = request.POST.get('date_label', '').strip()
                status = request.POST.get('status', 'pending')
                step_num = proj.stages.count() + 1
                try:
                    step_num = int(request.POST.get('step_number', step_num))
                except (ValueError, TypeError):
                    pass
                if title:
                    ProjectStage.objects.create(
                        project=proj,
                        step_number=step_num,
                        title=title,
                        description=desc,
                        date_label=date_lbl,
                        status=status
                    )
            return redirect('portal:dashboard')

        elif action == 'master_add_document':
            if client and client.projects.exists():
                proj = client.projects.first()
                title = request.POST.get('title', '').strip()
                doc_type = request.POST.get('doc_type', 'estimate')
                size_label = request.POST.get('size_label', '').strip()
                doc_file = request.FILES.get('doc_file')
                external_url = request.POST.get('external_url', '').strip() or None
                if title and (doc_file or external_url):
                    if doc_file and not size_label:
                        size_mb = doc_file.size / (1024 * 1024)
                        if size_mb < 1:
                            size_label = f"PDF, {max(1, int(doc_file.size / 1024))} КБ"
                        else:
                            size_label = f"PDF, {size_mb:.1f} МБ"
                    ProjectDocument.objects.create(
                        project=proj,
                        title=title,
                        doc_type=doc_type,
                        file=doc_file,
                        external_url=external_url,
                        size_label=size_label or 'PDF'
                    )
            return redirect('portal:dashboard')

        elif action == 'master_create_client':
            full_name = request.POST.get('full_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            company = request.POST.get('company', '').strip()
            email = request.POST.get('email', '').strip() or None
            client_type = request.POST.get('client_type', 'architect')
            pin = request.POST.get('pin', '').strip() or '1234'
            project_title = request.POST.get('project_title', '').strip()

            if full_name and phone:
                new_client = ClientAccount.objects.create(
                    full_name=full_name,
                    phone=phone,
                    company=company,
                    email=email,
                    client_type=client_type,
                    access_pin=pin,
                )
                if project_title:
                    proj = ProjectContract.objects.create(
                        client=new_client,
                        title=project_title,
                        contract_number=request.POST.get('contract_number', '').strip() or f"GB-{new_client.id:04d}",
                        address=request.POST.get('address', '').strip() or 'Москва',
                        total_area=request.POST.get('total_area', '200 м²').strip(),
                        total_amount=request.POST.get('total_amount', 750000) or 750000,
                        paid_amount=request.POST.get('paid_amount', 375000) or 375000,
                        progress_percent=15,
                        lead_artisan='Александр Попыкин',
                        status='active',
                    )
                    starter_stages = [
                        (1, 'Выездной аудит и лазерный замер геометрии стен', 'Инженерное обследование плоскостей, оценка влажности основания.', 'completed', 'Завершен'),
                        (2, 'Колеровка и согласование авторских образцов (Sample Box)', 'Изготовление планшетов с фактурами для утверждения заказчиком.', 'in_progress', 'В процессе'),
                        (3, 'Подготовка основания и армирование', 'Нанесение грунтовки глубокого проникновения и адгезионного слоя.', 'pending', 'Ожидает начала'),
                        (4, 'Художественное нанесение фактурных слоев', 'Ручная формовка минеральной фактуры шпателем.', 'pending', 'Ожидает начала'),
                        (5, 'Финишная гидрофобизация, защитный лак и сдача', 'Нанесение защитного полиуретанового лака и подписание КС-2.', 'pending', 'Ожидает начала'),
                    ]
                    for num, st_title, st_desc, st_stat, st_date in starter_stages:
                        ProjectStage.objects.create(
                            project=proj,
                            step_number=num,
                            title=st_title,
                            description=st_desc,
                            status=st_stat,
                            date_label=st_date
                        )
                request.session['master_active_client_id'] = new_client.id
                return redirect('portal:dashboard')

        elif action == 'master_create_project':
            if client:
                title = request.POST.get('title', '').strip() or 'Новый премиальный интерьер'
                proj = ProjectContract.objects.create(
                    client=client,
                    title=title,
                    contract_number=request.POST.get('contract_number', '').strip() or f"GB-{client.id:04d}",
                    address=request.POST.get('address', '').strip() or 'Москва',
                    total_area=request.POST.get('total_area', '200 м²').strip(),
                    total_amount=request.POST.get('total_amount', 800000) or 800000,
                    paid_amount=request.POST.get('paid_amount', 400000) or 400000,
                    progress_percent=10,
                    lead_artisan='Александр Попыкин',
                    status='active',
                )
                starter_stages = [
                    (1, 'Выездной аудит и лазерный замер геометрии стен', 'Инженерное обследование плоскостей, оценка влажности основания.', 'completed', 'Завершен'),
                    (2, 'Колеровка и согласование авторских образцов (Sample Box)', 'Изготовление планшетов с фактурами для утверждения заказчиком.', 'in_progress', 'В процессе'),
                    (3, 'Подготовка основания и армирование', 'Нанесение грунтовки глубокого проникновения и адгезионного слоя.', 'pending', 'Ожидает начала'),
                    (4, 'Художественное нанесение фактурных слоев', 'Ручная формовка минеральной фактуры шпателем.', 'pending', 'Ожидает начала'),
                    (5, 'Финишная гидрофобизация, защитный лак и сдача', 'Нанесение защитного полиуретанового лака и подписание КС-2.', 'pending', 'Ожидает начала'),
                ]
                for num, st_title, st_desc, st_stat, st_date in starter_stages:
                    ProjectStage.objects.create(
                        project=proj,
                        step_number=num,
                        title=st_title,
                        description=st_desc,
                        status=st_stat,
                        date_label=st_date
                    )
                return redirect('portal:dashboard')

    if is_demo or not client:
        demo_ctx = get_demo_context()
        demo_ctx['just_registered'] = just_registered
        return render(request, 'portal/dashboard.html', {
            'data': demo_ctx,
            'is_demo': True,
            'is_master': is_master,
            'all_clients': all_clients,
        })

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
            'is_master': is_master,
            'all_clients': all_clients,
        }
        return render(request, 'portal/dashboard.html', {
            'data': context,
            'is_demo': False,
            'is_master': is_master,
            'all_clients': all_clients,
        })

    stages = project.stages.all().order_by('step_number')
    photos = project.photos.all()
    documents = project.documents.all()

    formatted_photos = []
    for ph in photos:
        formatted_photos.append({
            'caption': ph.caption,
            'display_url': ph.get_display_url(),
            'date': ph.created_at.strftime('%d.%m.%Y'),
        })

    formatted_docs = []
    for doc in documents:
        formatted_docs.append({
            'title': doc.title,
            'doc_type_display': doc.get_doc_type_display(),
            'size_label': doc.size_label,
            'url': doc.file.url if doc.file else (doc.external_url or '#'),
        })

    context = {
        'client': client,
        'tier': tier_data,
        'project': project,
        'stages': stages,
        'photos': formatted_photos,
        'documents': formatted_docs,
        'is_demo': False,
        'has_active_project': True,
        'just_registered': just_registered,
        'is_master': is_master,
        'all_clients': all_clients,
    }
    return render(request, 'portal/dashboard.html', {
        'data': context,
        'is_demo': False,
        'is_master': is_master,
        'all_clients': all_clients,
    })

def portal_logout(request):
    django_logout(request)
    request.session.flush()
    return redirect('portal:login')

def portal_profile(request):
    """Страница персонального профиля клиента с детальным учетом всех пожеланий и техзадания."""
    is_master = check_is_master(request)
    all_clients = ClientAccount.objects.all().order_by('-created_at') if is_master else []

    # Переключение клиента для режима Мастера
    if is_master:
        switch_id = request.GET.get('switch_client') or request.POST.get('switch_client')
        if switch_id:
            request.session['master_active_client_id'] = switch_id

    is_demo = False
    client = None

    if is_master:
        active_id = request.session.get('master_active_client_id')
        if active_id == 'demo':
            is_demo = True
        elif active_id:
            try:
                client = ClientAccount.objects.filter(id=int(active_id)).first()
            except (ValueError, TypeError):
                client = None
        if not client and not is_demo:
            client = ClientAccount.objects.first()
            if client:
                request.session['master_active_client_id'] = client.id
            else:
                is_demo = True
    else:
        phone = request.session.get('client_phone')
        if phone and phone != 'demo':
            client = ClientAccount.objects.filter(phone=phone).first()
            if not client:
                digits = re.sub(r'\D', '', phone)
                if len(digits) >= 10:
                    client = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()
        elif hasattr(request, 'user') and request.user.is_authenticated and hasattr(request.user, 'client_account'):
            client = request.user.client_account
        if not client:
            is_demo = True

    MATERIAL_CHOICES = [
        ('microcement', 'Бесшовный микроцемент (Microcement)'),
        ('mineral_plaster', 'Минеральная фактурная штукатурка'),
        ('travertine', 'Парижский травертин и скальный рельеф'),
        ('basrelief', 'Скульптурные настенные барельефы'),
        ('gold_leaf', 'Сусальное золочение, поталь и патина'),
        ('mural', 'Авторская монументальная роспись стен'),
        ('venetian', 'Классическая венецианская штукатурка'),
        ('art_canvas', 'Картины и коллекционные арт-объекты Александра Попыкина'),
    ]

    SPACE_CHOICES = [
        ('living_rooms', 'Гостиные, холлы и мастер-спальни'),
        ('wet_zones', 'Мокрые зоны, ванные комнаты и SPA (100% гидроизоляция)'),
        ('commercial_horeca', 'Рестораны, бары, бутики и отели (высокая износостойкость)'),
        ('corporate_office', 'Представительские офисы и штаб-квартиры'),
        ('facades', 'Фасады, входные группы и террасы'),
        ('ceilings_accents', 'Сложные архитектурные потолки и купола'),
    ]

    SERVICE_CHOICES = [
        ('sample_box', 'Доставка фирменного Architect Sample Box с живыми выкрасами'),
        ('laser_audit', 'Выездной лазерный замер геометрии и аудит влажности стен'),
        ('art_fitting', 'Бесплатная примерка полотен Александра Попыкина в интерьере'),
        ('night_shifts', 'Возможность работы в ночные смены (для ТЦ и ресторанов)'),
        ('nda_signed', 'Строгий режим конфиденциальности объекта (NDA)'),
        ('edo_docs', 'Электронный документооборот (Диадок / КС-2 / КС-3 / НДС)'),
    ]

    status_message = None
    status_type = 'success'

    if request.method == 'POST':
        action = request.POST.get('action', 'save_profile')

        if is_master and action == 'master_update_crm' and client:
            client.custom_tier = request.POST.get('custom_tier', '')
            client.notes = request.POST.get('notes', '').strip() or None
            client.save()
            status_message = 'Служебные параметры CRM и персональный уровень лояльности успешно сохранены.'
            status_type = 'success'
        elif is_demo:
            status_message = 'В демонстрационном режиме изменения не сохраняются в базе данных. Зарегистрируйтесь в клубе, чтобы закрепить персональные условия.'
            status_type = 'info'
        else:
            if action == 'request_sample_box':
                try:
                    from leads.models import Lead
                    Lead.objects.create(
                        name=client.full_name,
                        company=client.company or '',
                        phone=client.phone,
                        email=client.email or '',
                        source='profile_sample_box',
                        object_type=f"Заказ кейса образцов ({client.get_client_type_display()})",
                        service_needed="Architect Sample Box по адресу из профиля",
                        message=f"Адрес доставки: {client.delivery_address or 'Уточнить у клиента'}. Связь через: {client.preferred_messenger}",
                    )
                    status_message = 'Заявка на Architect Sample Box принята! Образцы будут направлены по вашему адресу доставки.'
                except Exception:
                    status_message = 'Ошибка при создании заявки на образцы. Пожалуйста, свяжитесь с нами напрямую.'
                    status_type = 'error'

            elif action == 'request_art_fitting':
                try:
                    from leads.models import Lead
                    Lead.objects.create(
                        name=client.full_name,
                        company=client.company or '',
                        phone=client.phone,
                        email=client.email or '',
                        source='profile_art_fitting',
                        object_type=f"Примерка картин ({client.get_client_type_display()})",
                        service_needed="Бесплатная примерка картин в интерьере объекта",
                        message=f"Адрес объекта: {client.delivery_address or 'Уточнить'}. Пожелания: {client.client_wishes or 'Без примечаний'}",
                    )
                    status_message = 'Заявка на примерку картин принята! Куратор студии свяжется с вами для согласования удобного дня.'
                except Exception:
                    status_message = 'Ошибка при заказе примерки.'
                    status_type = 'error'

            elif action == 'request_laser_audit':
                try:
                    from leads.models import Lead
                    Lead.objects.create(
                        name=client.full_name,
                        company=client.company or '',
                        phone=client.phone,
                        email=client.email or '',
                        source='profile_audit',
                        object_type=f"Выездной аудит стен ({client.get_client_type_display()})",
                        service_needed="Лазерный замер геометрии и аудит основания",
                        message=f"Адрес объекта: {client.delivery_address or 'Уточнить'}",
                    )
                    status_message = 'Заявка на выездной аудит стен принята! Технолог Александр Попыкин свяжется с вами для подтверждения времени визита.'
                except Exception:
                    status_message = 'Ошибка при заказе аудита.'
                    status_type = 'error'

            else:
                client.full_name = request.POST.get('full_name', client.full_name).strip()
                client.email = request.POST.get('email', client.email or '').strip() or None
                client.company = request.POST.get('company', client.company or '').strip() or None
                client.client_type = request.POST.get('client_type', client.client_type)
                client.delivery_address = request.POST.get('delivery_address', client.delivery_address or '').strip() or None
                client.preferred_messenger = request.POST.get('preferred_messenger', client.preferred_messenger or 'telegram')
                client.client_wishes = request.POST.get('client_wishes', client.client_wishes or '').strip() or None

                pin = request.POST.get('pin', '').strip()
                if pin and len(pin) >= 4:
                    client.access_pin = pin

                client.preferred_materials = request.POST.getlist('preferred_materials')
                client.preferred_spaces = request.POST.getlist('preferred_spaces')
                client.service_options = request.POST.getlist('service_options')
                client.save()

                status_message = 'Все ваши индивидуальные пожелания, технические требования и реквизиты успешно сохранены в системе мастерской.'

    if is_demo or not client:
        demo_ctx = get_demo_context()
        profile_data = {
            'id': None,
            'full_name': demo_ctx['client']['full_name'],
            'phone': demo_ctx['client']['phone'],
            'company': demo_ctx['client']['company'],
            'email': demo_ctx['client']['email'],
            'client_type': 'architect',
            'client_type_display': 'Архитектурное бюро / Дизайн-студия',
            'delivery_address': 'Москва, Малый Козихинский пер., 12, офис 4',
            'preferred_messenger': 'telegram',
            'access_pin': '1234',
            'custom_tier': '',
            'notes': 'Партнерский статус подтвержден. Заказчику интересны фактуры травертина и микроцемента для пентхауса.',
            'preferred_materials': ['microcement', 'travertine', 'basrelief'],
            'preferred_spaces': ['living_rooms', 'wet_zones', 'commercial_horeca'],
            'service_options': ['sample_box', 'art_fitting', 'laser_audit', 'nda_signed'],
            'client_wishes': 'Интерьер в стиле современного теплого минимализма. Необходима бесшовная фактура стен в мастер-спальне и гостиной, устойчивая к влажной уборке. Также интересует подбор 2-3 коллекционных картин Александра Попыкина в гостиную зону.',
            'tier': demo_ctx['tier'],
            'project': demo_ctx['project'],
        }
    else:
        tier_info = client.next_tier_info
        profile_data = {
            'id': client.id,
            'full_name': client.full_name,
            'phone': client.phone,
            'company': client.company or '',
            'email': client.email or '',
            'client_type': client.client_type,
            'client_type_display': client.get_client_type_display(),
            'delivery_address': client.delivery_address or '',
            'preferred_messenger': client.preferred_messenger or 'telegram',
            'access_pin': client.access_pin,
            'custom_tier': client.custom_tier,
            'notes': client.notes or '',
            'preferred_materials': client.preferred_materials or [],
            'preferred_spaces': client.preferred_spaces or [],
            'service_options': client.service_options or [],
            'client_wishes': client.client_wishes or '',
            'tier': {
                'code': client.tier_code,
                'name': client.tier_name,
                'discount_materials': client.discount_materials,
                'discount_works': client.discount_works,
                'completed_projects': client.total_projects_count,
                'next_tier_label': tier_info['label'],
                'projects_needed': tier_info['projects_needed'],
                'progress_pct': tier_info['progress_pct'],
                'max_tier': tier_info['max_tier'],
            },
            'project': client.projects.first(),
        }

    context = {
        'profile': profile_data,
        'client': client,
        'material_choices': MATERIAL_CHOICES,
        'space_choices': SPACE_CHOICES,
        'service_choices': SERVICE_CHOICES,
        'is_demo': is_demo,
        'is_master': is_master,
        'all_clients': all_clients,
        'status_message': status_message,
        'status_type': status_type,
    }
    return render(request, 'portal/profile.html', context)

