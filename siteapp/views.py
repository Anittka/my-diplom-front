import re
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Lead, Product, Category, Article, SiteSettings


ALLOWED_ATTACHMENT_TYPES = {
    'image/jpeg',
    'image/png',
    'image/webp',
    'application/pdf',
}

ALLOWED_ATTACHMENT_EXTENSIONS = {
    '.jpg',
    '.jpeg',
    '.png',
    '.webp',
    '.pdf',
}

MAX_ATTACHMENT_SIZE = 5 * 1024 * 1024


def get_site_settings():
    return SiteSettings.objects.filter(is_active=True).first()


def base_context(extra=None):
    context = {
        'site_settings': get_site_settings(),
    }

    if extra:
        context.update(extra)

    return context


def normalize_phone(value):
    digits = re.sub(r'\D', '', value or '')

    if len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]

    if len(digits) != 11 or not digits.startswith('7'):
        return None

    return f'+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}'


def validate_attachment(attachment):
    errors = []

    if not attachment:
        return errors

    if attachment.size > MAX_ATTACHMENT_SIZE:
        errors.append('размер файла не должен превышать 5 МБ')

    content_type = getattr(attachment, 'content_type', '')
    if content_type not in ALLOWED_ATTACHMENT_TYPES:
        errors.append('можно прикрепить только JPG, PNG, WEBP или PDF')

    suffix = Path(attachment.name).suffix.lower()
    if suffix not in ALLOWED_ATTACHMENT_EXTENSIONS:
        errors.append('недопустимое расширение файла')

    return errors


def lead_create(request):
    if request.method != 'POST':
        return redirect(reverse('index'))

    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    message_text = request.POST.get('message', '').strip()
    request_type = request.POST.get('request_type', 'general')
    source_page = request.POST.get('source_page', request.META.get('HTTP_REFERER', '')).strip()
    privacy = request.POST.get('privacy') in ('on', 'true', '1', 'yes')
    attachment = request.FILES.get('attachment')

    errors = []

    if not name:
        errors.append('укажите имя')

    normalized_phone = normalize_phone(phone)

    if not normalized_phone:
        errors.append('укажите корректный телефон в формате +7 (___) ___-__-__')

    if not privacy:
        errors.append('подтвердите согласие на обработку персональных данных')

    errors.extend(validate_attachment(attachment))

    if errors:
        messages.error(request, 'Заявка не отправлена: ' + ', '.join(errors) + '.')
        return redirect(request.META.get('HTTP_REFERER') or reverse('index'))

    lead = Lead.objects.create(
        name=name,
        phone=normalized_phone,
        email=email,
        message=message_text,
        request_type=request_type if request_type in dict(Lead.REQUEST_TYPES) else 'general',
        source_page=source_page,
        privacy_accepted=True,
        attachment=attachment,
    )

    if getattr(settings, 'ADMIN_EMAIL', ''):
        send_mail(
            'Новая заявка с сайта',
            (
                f'Имя: {lead.name}\n'
                f'Телефон: {lead.phone}\n'
                f'Email: {lead.email}\n'
                f'Тип: {lead.get_request_type_display()}\n'
                f'Страница: {lead.source_page}\n'
                f'Сообщение: {lead.message}'
            ),
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )

    messages.success(request, 'Заявка отправлена. Менеджер свяжется с вами в рабочее время.')
    return redirect(request.META.get('HTTP_REFERER') or reverse('index'))


def index(request):
    return render(
        request,
        'siteapp/index.html',
        base_context({
            'featured_products': Product.objects.filter(
                is_active=True,
                is_featured=True
            ).select_related('category').prefetch_related('images')[:8],

            'categories': Category.objects.filter(is_active=True)[:8],

            'articles': Article.objects.filter(is_active=True)[:3],
        })
    )


def catalog(request):
    return render(
        request,
        'siteapp/catalog.html',
        base_context({
            'products': Product.objects.filter(
                is_active=True
            ).select_related('category').prefetch_related('images'),

            'categories': Category.objects.filter(is_active=True),
        })
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        slug=slug,
        is_active=True
    )

    related = Product.objects.filter(
        is_active=True,
        category=product.category
    ).exclude(pk=product.pk).prefetch_related('images')[:4]

    return render(
        request,
        'siteapp/product_detail.html',
        base_context({
            'product': product,
            'related_products': related,
        })
    )


def articles(request):
    return render(
        request,
        'siteapp/articles.html',
        base_context({
            'articles': Article.objects.filter(is_active=True),
        })
    )


def about(request):
    return render(
        request,
        'siteapp/about.html',
        base_context()
    )


def delivery(request):
    return render(
        request,
        'siteapp/delivery.html',
        base_context()
    )


def contacts(request):
    return render(
        request,
        'siteapp/contacts.html',
        base_context()
    )


def politik(request):
    return render(
        request,
        'siteapp/politik.html',
        base_context()
    )


def sitemap(request):
    return render(
        request,
        'siteapp/sitemap.html',
        base_context()
    )


def api_products(request):
    products = Product.objects.filter(
        is_active=True
    ).select_related('category').prefetch_related('images')

    data = []

    for product in products:
        first_image = product.images.first()

        data.append({
            'title': product.title,
            'slug': product.slug,
            'article': product.article,
            'category': product.category.name if product.category else '',
            'availability': product.availability,
            'price_note': product.price_note,
            'image': first_image.image.url if first_image else '',
            'url': f'/catalog/{product.slug}/',
        })

    return JsonResponse({'products': data})


def api_categories(request):
    categories = Category.objects.filter(is_active=True)

    return JsonResponse({
        'categories': [
            {
                'name': c.name,
                'slug': c.slug,
                'description': c.description,
            }
            for c in categories
        ]
    })


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Sitemap: https://agromarkettorshenko.ru/sitemap.xml',
    ]

    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    base = 'https://agromarkettorshenko.ru'

    urls = [
        '',
        '/catalog/',
        '/articles/',
        '/about/',
        '/delivery/',
        '/contacts/',
        '/politika/',
        '/sitemap/',
    ]

    product_urls = [
        f'/catalog/{p.slug}/'
        for p in Product.objects.filter(is_active=True)
    ]

    xml_urls = ''.join(
        f'<url><loc>{base}{url}</loc></url>'
        for url in urls + product_urls
    )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'{xml_urls}'
        '</urlset>'
    )

    return HttpResponse(xml, content_type='application/xml')

