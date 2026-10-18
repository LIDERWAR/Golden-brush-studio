from .models import HomePageConfig
from portal.models import ClientAccount
import re

def site_settings(request):
    """Глобальный контекст-процессор для передачи контактов и статуса авторизации клиента во все шаблоны"""
    client_phone = request.session.get('client_phone')
    client_user = None
    is_client_authenticated = False
    is_master = False

    # Проверка прав администратора / мастера студии
    if hasattr(request, 'user') and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        is_master = True
        is_client_authenticated = True
    elif request.session.get('is_master_mode'):
        is_master = True
        is_client_authenticated = True

    if client_phone and client_phone not in ('demo', 'master'):
        client_user = ClientAccount.objects.filter(phone=client_phone).first()
        if not client_user:
            digits = re.sub(r'\D', '', client_phone)
            if len(digits) >= 10:
                client_user = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()
        if client_user:
            is_client_authenticated = True
    elif is_master:
        active_client_id = request.session.get('master_active_client_id')
        if active_client_id:
            client_user = ClientAccount.objects.filter(id=active_client_id).first()
        if not client_user:
            client_user = ClientAccount.objects.first()

    return {
        'home_config': HomePageConfig.get_solo(),
        'client_user': client_user,
        'is_client_authenticated': is_client_authenticated,
        'is_master': is_master,
    }
