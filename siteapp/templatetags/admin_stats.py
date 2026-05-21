from datetime import timedelta
from django import template
from django.db.models import Count
from django.utils import timezone
from siteapp.models import Category, Product, Article, Lead

register = template.Library()

@register.simple_tag
def get_admin_stats():
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    return {
        'total_products': Product.objects.count(),
        'active_products': Product.objects.filter(is_active=True).count(),
        'featured_products': Product.objects.filter(is_featured=True).count(),
        'total_categories': Category.objects.count(),
        'total_articles': Article.objects.count(),
        'active_articles': Article.objects.filter(is_active=True).count(),
        'total_leads': Lead.objects.count(),
        'new_leads': Lead.objects.filter(status='new').count(),
        'work_leads': Lead.objects.filter(status='in_work').count(),
        'waiting_leads': Lead.objects.filter(status='waiting').count(),
        'done_leads': Lead.objects.filter(status='done').count(),
        'high_priority_leads': Lead.objects.filter(priority='high').count(),
        'week_leads': Lead.objects.filter(created_at__gte=week_ago).count(),
        'month_leads': Lead.objects.filter(created_at__gte=month_ago).count(),
        'status_rows': list(Lead.objects.values('status').annotate(count=Count('id')).order_by('status')),
        'products_without_images': Product.objects.filter(images__isnull=True).count(),
        'latest_leads': Lead.objects.order_by('-created_at')[:5],
    }
