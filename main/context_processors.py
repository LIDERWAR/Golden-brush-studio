from .models import HomePageConfig

def site_settings(request):
    """Глобальный контекст-процессор для передачи контактов и настроек студии во все шаблоны"""
    return {
        'home_config': HomePageConfig.get_solo(),
    }
