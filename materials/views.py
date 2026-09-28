from django.shortcuts import render, get_object_or_404
from .models import DecorativeMaterial, MaterialCategory
from main.models import HomePageConfig

def material_list(request):
    """Каталог декоративных минеральных покрытий, штукатурок и микроцемента с калькулятором"""
    category_slug = request.GET.get('category', '').strip()
    materials = DecorativeMaterial.objects.filter(is_active=True)
    
    if category_slug:
        materials = materials.filter(category__slug=category_slug)
        
    categories = MaterialCategory.objects.all()
    home_config = HomePageConfig.get_solo()
    
    context = {
        'materials': materials,
        'categories': categories,
        'current_category': category_slug,
        'home_config': home_config,
    }
    return render(request, 'materials/list.html', context)


def material_detail(request, slug):
    """Детальная страница материала / фактурного покрытия"""
    material = get_object_or_404(DecorativeMaterial, slug=slug, is_active=True)
    related_materials = DecorativeMaterial.objects.filter(is_active=True).exclude(id=material.id)[:3]
    
    context = {
        'material': material,
        'related_materials': related_materials,
    }
    return render(request, 'materials/detail.html', context)
