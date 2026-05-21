from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.template.response import TemplateResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from siteapp.models import Product, Category, Lead, Article
from siteapp.views import index, about, delivery, contacts, catalog, product_detail, articles, lead_create, politik, api_products, api_categories


def statistics_view(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    context = {
        'title': 'Статистика сайта',
        'total_products': Product.objects.count(),
        'active_products': Product.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.count(),
        'total_articles': Article.objects.count(),
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(status='new').count(),
        'work_leads': Lead.objects.filter(status='in_work').count(),
        'done_leads': Lead.objects.filter(status='done').count(),
        'week_leads': Lead.objects.filter(created_at__gte=week_ago).count(),
        'month_leads': Lead.objects.filter(created_at__gte=month_ago).count(),
        'leads_by_status': list(
            Lead.objects.values('status').annotate(count=Count('id')).order_by('status')
        ),
        'leads_by_type': list(
            Lead.objects.values('request_type').annotate(count=Count('id')).order_by('request_type')
        ),
        'products_by_category': list(
            Product.objects.values('category__name').annotate(count=Count('id')).order_by('-count')
        ),
    }
    return TemplateResponse(request, 'admin/siteapp/dashboard.html', context)


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('delivery/', delivery, name='delivery'),
    path('contacts/', contacts, name='contacts'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:slug>/', product_detail, name='product_detail'),
    path('articles/', articles, name='articles'),
    path('lead-create/', lead_create, name='lead_create'),
    path('politik/', politik, name='politik'),
    path('api/products/', api_products, name='api_products'),
    path('api/categories/', api_categories, name='api_categories'),
    path('admin/', admin.site.urls),
    path('admin/statistics/', admin.site.admin_view(statistics_view), name='statistics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)