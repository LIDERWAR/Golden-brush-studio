from .models import HomePageConfig
from portal.models import ClientAccount
import re

def site_settings(request):
    """Глобальный контекст-процессор для передачи контактов и статуса авторизации клиента во все шаблоны"""
    client_phone = request.session.get('client_phone')
    client_user = None
    is_client_authenticated = False

    if client_phone and client_phone != 'demo':
        client_user = ClientAccount.objects.filter(phone=client_phone).first()
        if not client_user:
            digits = re.sub(r'\D', '', client_phone)
            if len(digits) >= 10:
                client_user = ClientAccount.objects.filter(phone__icontains=digits[-10:]).first()
        if client_user:
            is_client_authenticated = True
    elif hasattr(request, 'user') and request.user.is_authenticated:
        if hasattr(request.user, 'client_account'):
            client_user = request.user.client_account
            is_client_authenticated = True

    return {
        'home_config': HomePageConfig.get_solo(),
        'client_user': client_user,
        'is_client_authenticated': is_client_authenticated,
    }
