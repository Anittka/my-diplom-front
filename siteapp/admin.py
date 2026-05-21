from datetime import timedelta

from django.contrib import admin, messages
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Product,
    ProductImage,
    Lead,
    LeadStatusHistory,
    Article,
    SiteSettings,
)
from .utils import (
    export_queryset_to_xlsx,
    export_queryset_to_html,
    export_queryset_to_csv,
)


admin.site.site_header = 'АГРОМАРКЕТ ТОРШЕНКО — админ-панель'
admin.site.site_title = 'АГРОМАРКЕТ'
admin.site.index_title = 'Панель управления сайтом'
admin.site.index_template = 'admin/siteapp/custom_index.html'


def image_preview_html(image_field, height=54):
    if not image_field:
        return 'Нет фото'

    return format_html(
        '<img src="{}" style="height:{}px;max-width:120px;object-fit:cover;border-radius:10px;border:1px solid #d8e1ea;background:#fff;padding:3px;" alt="preview">',
        image_field.url,
        height,
    )


def product_first_image(product):
    first = product.images.first()
    return first.image if first else None


def export_leads_excel(modeladmin, request, queryset):
    return export_queryset_to_xlsx(
        queryset,
        'leads.xlsx',
        [
            'ID',
            'Имя',
            'Телефон',
            'Email',
            'Тип',
            'Сообщение',
            'Источник',
            'Статус',
            'Приоритет',
            'Согласие ПДн',
            'Комментарий',
            'Дата',
        ],
        lambda o: [
            o.id,
            o.name,
            o.phone,
            o.email,
            o.get_request_type_display(),
            o.message,
            o.source_page,
            o.get_status_display(),
            o.get_priority_display(),
            'Да' if o.privacy_accepted else 'Нет',
            o.manager_comment,
            o.created_at.strftime('%d.%m.%Y %H:%M') if o.created_at else '',
        ],
    )


export_leads_excel.short_description = 'Выгрузить выбранные заявки в Excel'


def export_leads_html(modeladmin, request, queryset):
    return export_queryset_to_html(
        queryset,
        'leads.html',
        'Заявки сайта',
        [
            'ID',
            'Имя',
            'Телефон',
            'Email',
            'Тип',
            'Сообщение',
            'Источник',
            'Статус',
            'Приоритет',
            'Согласие ПДн',
            'Комментарий',
            'Дата',
        ],
        lambda o: [
            o.id,
            o.name,
            o.phone,
            o.email,
            o.get_request_type_display(),
            o.message,
            o.source_page,
            o.get_status_display(),
            o.get_priority_display(),
            'Да' if o.privacy_accepted else 'Нет',
            o.manager_comment,
            o.created_at.strftime('%d.%m.%Y %H:%M') if o.created_at else '',
        ],
    )


export_leads_html.short_description = 'Выгрузить выбранные заявки в HTML'


def export_products_excel(modeladmin, request, queryset):
    return export_queryset_to_xlsx(
        queryset,
        'products.xlsx',
        ['ID', 'Название', 'Артикул', 'Категория', 'Наличие', 'Цена', 'Активен'],
        lambda o: [
            o.id,
            o.title,
            o.article,
            o.category.name if o.category else '',
            o.availability,
            o.price_note,
            'Да' if o.is_active else 'Нет',
        ],
    )


export_products_excel.short_description = 'Выгрузить выбранные товары в Excel'


def export_products_html(modeladmin, request, queryset):
    return export_queryset_to_html(
        queryset,
        'products.html',
        'Товары сайта',
        ['ID', 'Название', 'Артикул', 'Категория', 'Наличие', 'Цена', 'Активен'],
        lambda o: [
            o.id,
            o.title,
            o.article,
            o.category.name if o.category else '',
            o.availability,
            o.price_note,
            'Да' if o.is_active else 'Нет',
        ],
    )


export_products_html.short_description = 'Выгрузить выбранные товары в HTML'


def export_products_csv(modeladmin, request, queryset):
    return export_queryset_to_csv(
        queryset,
        'products.csv',
        ['ID', 'Название', 'Артикул', 'Категория', 'Наличие', 'Цена', 'Активен'],
        lambda o: [
            o.id,
            o.title,
            o.article,
            o.category.name if o.category else '',
            o.availability,
            o.price_note,
            'Да' if o.is_active else 'Нет',
        ],
    )


export_products_csv.short_description = 'Выгрузить выбранные товары в CSV'


def export_articles_excel(modeladmin, request, queryset):
    return export_queryset_to_xlsx(
        queryset,
        'articles.xlsx',
        ['ID', 'Заголовок', 'Рубрика', 'Краткое описание', 'Активна', 'Дата'],
        lambda o: [
            o.id,
            o.title,
            o.tag,
            o.short_text,
            'Да' if o.is_active else 'Нет',
            o.created_at.strftime('%d.%m.%Y') if o.created_at else '',
        ],
    )


export_articles_excel.short_description = 'Выгрузить выбранные статьи в Excel'


def export_articles_html(modeladmin, request, queryset):
    return export_queryset_to_html(
        queryset,
        'articles.html',
        'Статьи сайта',
        ['ID', 'Заголовок', 'Рубрика', 'Краткое описание', 'Активна', 'Дата'],
        lambda o: [
            o.id,
            o.title,
            o.tag,
            o.short_text,
            'Да' if o.is_active else 'Нет',
            o.created_at.strftime('%d.%m.%Y') if o.created_at else '',
        ],
    )


export_articles_html.short_description = 'Выгрузить выбранные статьи в HTML'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image_preview', 'image', 'alt', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return image_preview_html(obj.image) if obj.pk else 'После сохранения появится предпросмотр'

    image_preview.short_description = 'Превью'


class LeadStatusHistoryInline(admin.TabularInline):
    model = LeadStatusHistory
    extra = 0
    can_delete = False
    fields = ('old_status', 'new_status', 'comment', 'created_at')
    readonly_fields = ('old_status', 'new_status', 'comment', 'created_at')


class LeadAttachmentFilter(admin.SimpleListFilter):
    title = 'Вложение'
    parameter_name = 'has_attachment'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'С файлом'),
            ('no', 'Без файла'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(attachment='')
        if self.value() == 'no':
            return queryset.filter(attachment='')
        return queryset


class ProductImageFilter(admin.SimpleListFilter):
    title = 'Фото'
    parameter_name = 'has_image'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'С фото'),
            ('no', 'Без фото'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(images__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(images__isnull=True)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'preview',
        'title',
        'article',
        'category',
        'availability',
        'price_note',
        'is_featured',
        'is_active',
        'open_on_site',
    )
    list_editable = ('availability', 'price_note', 'is_featured', 'is_active')
    list_filter = ('category', 'is_active', 'is_featured', ProductImageFilter)
    search_fields = ('title', 'article', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    actions = [export_products_excel, export_products_csv, export_products_html]

    def preview(self, obj):
        return image_preview_html(product_first_image(obj), 46)

    preview.short_description = 'Фото'

    def open_on_site(self, obj):
        if not obj.slug:
            return '-'
        return format_html('<a href="{}" target="_blank">Открыть</a>',
                         reverse('product_detail', args=[obj.slug]))

    open_on_site.short_description = 'На сайте'


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone_link_admin',
        'request_type',
        'attachment_badge',
        'priority',
        'status_badge',
        'created_at',
    )
    list_editable = ('priority',)
    list_filter = (
        'request_type',
        'status',
        'priority',
        LeadAttachmentFilter,
        'privacy_accepted',
        'created_at',
    )
    search_fields = (
        'name',
        'phone',
        'email',
        'message',
        'manager_comment',
        'source_page',
    )
    readonly_fields = ('created_at', 'updated_at', 'attachment_preview')
    inlines = [LeadStatusHistoryInline]
    actions = [
        'mark_as_work',
        'mark_as_waiting',
        'mark_as_answered',
        'mark_as_done',
        'mark_as_rejected',
        'mark_priority_high',
        export_leads_excel,
        export_leads_html,
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        (
            'Контактные данные клиента',
            {
                'fields': (
                    'name',
                    'phone',
                    'email',
                    'privacy_accepted',
                )
            },
        ),
        (
            'Информация по заявке',
            {
                'fields': (
                    'request_type',
                    'message',
                    'source_page',
                    'attachment',
                    'attachment_preview',
                )
            },
        ),
        (
            'Работа менеджера',
            {
                'fields': (
                    'status',
                    'priority',
                    'manager_comment',
                )
            },
        ),
        (
            'Служебные даты',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )

    def phone_link_admin(self, obj):
        digits = ''.join(ch for ch in obj.phone if ch.isdigit())
        href = '+' + digits if digits else obj.phone
        whatsapp = 'https://wa.me/' + digits if digits else '#'

        return format_html(
            '<a href="tel:{}">{}</a><br><a href="{}" target="_blank" style="font-size:12px;">WhatsApp</a>',
            href,
            obj.phone,
            whatsapp,
        )

    phone_link_admin.short_description = 'Телефон'

    def attachment_badge(self, obj):
        if obj.attachment:
            return mark_safe('<span style="color:#15803d;font-weight:700;">✓ Есть</span>')
        return 'Нет'

    attachment_badge.short_description = 'Файл'

    def attachment_preview(self, obj):
        if not obj.attachment:
            return 'Файл не прикреплён'

        name = obj.attachment.name.lower()

        if name.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height:120px;border-radius:12px;border:1px solid #d8e1ea;padding:4px;background:#fff;"></a>',
                obj.attachment.url,
                obj.attachment.url,
            )

        return format_html(
            '<a href="{}" target="_blank">Открыть файл</a>',
            obj.attachment.url,
        )

    attachment_preview.short_description = 'Предпросмотр файла'

    def status_badge(self, obj):
        colors = {
            'new': '#b45309',
            'in_work': '#2563eb',
            'waiting': '#7c3aed',
            'answered': '#0f766e',
            'done': '#15803d',
            'rejected': '#991b1b',
        }

        color = colors.get(obj.status, '#4b5563')

        return mark_safe(
            f'<span style="display:inline-block;padding:4px 9px;border-radius:999px;background:{color}18;color:{color};font-weight:700;">{obj.get_status_display()}</span>'
        )

    status_badge.short_description = 'Статус'

    def save_model(self, request, obj, form, change):
        old_status = None

        if change and obj.pk:
            old_status = Lead.objects.filter(pk=obj.pk).values_list('status', flat=True).first()

        super().save_model(request, obj, form, change)

        if old_status is not None and old_status != obj.status:
            LeadStatusHistory.objects.create(
                lead=obj,
                old_status=old_status,
                new_status=obj.status,
                comment=f'Статус изменил администратор: {request.user}',
            )

    def _set_status(self, request, queryset, status, comment):
        count = 0

        for lead in queryset:
            old_status = lead.status
            lead.status = status
            lead.save(update_fields=['status', 'updated_at'])

            if old_status != status:
                LeadStatusHistory.objects.create(
                    lead=lead,
                    old_status=old_status,
                    new_status=status,
                    comment=comment,
                )
                count += 1

        self.message_user(request, f'Обновлено заявок: {count}', messages.SUCCESS)

    def mark_as_done(self, request, queryset):
        self._set_status(request, queryset, 'done', 'Массовое действие: завершить')

    mark_as_done.short_description = 'Отметить как завершённые'

    def mark_as_work(self, request, queryset):
        self._set_status(request, queryset, 'in_work', 'Массовое действие: взять в работу')

    mark_as_work.short_description = 'Отметить как в работе'

    def mark_as_waiting(self, request, queryset):
        self._set_status(request, queryset, 'waiting', 'Массовое действие: ждёт уточнения')

    mark_as_waiting.short_description = 'Отметить как ожидающие уточнения'

    def mark_as_answered(self, request, queryset):
        self._set_status(request, queryset, 'answered', 'Массовое действие: ответ отправлен')

    mark_as_answered.short_description = 'Отметить как отвеченные'

    def mark_as_rejected(self, request, queryset):
        self._set_status(request, queryset, 'rejected', 'Массовое действие: отказ/неактуально')

    mark_as_rejected.short_description = 'Отметить как неактуальные'

    def mark_priority_high(self, request, queryset):
        count = queryset.update(priority='high')
        self.message_user(
            request,
            f'Высокий приоритет установлен для заявок: {count}',
            messages.SUCCESS,
        )

    mark_priority_high.short_description = 'Поставить высокий приоритет'


@admin.register(LeadStatusHistory)
class LeadStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('lead', 'old_status', 'new_status', 'comment', 'created_at')
    list_filter = ('new_status', 'created_at')
    search_fields = ('lead__name', 'lead__phone', 'comment')
    readonly_fields = ('lead', 'old_status', 'new_status', 'comment', 'created_at')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'tag', 'slug', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'tag', 'created_at')
    search_fields = ('title', 'text', 'short_text')
    prepopulated_fields = {'slug': ('title',)}
    actions = [export_articles_excel, export_articles_html]

    def image_preview(self, obj):
        return image_preview_html(obj.image, 42)

    image_preview.short_description = 'Фото'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'phone',
        'email',
        'address',
        'work_time',
        'is_active',
    )
    list_editable = ('is_active',)

    readonly_fields = (
        'logo_preview',
        'favicon_preview',
        'og_preview',
        'hero_background_preview',
        'hero_card_preview',
        'metric_positions_preview',
        'metric_experience_preview',
        'metric_response_preview',
        'metric_delivery_preview',
        'category_combines_preview',
        'category_tractors_preview',
        'category_popular_preview',
        'article_filters_preview',
        'article_bearings_preview',
        'article_belt_preview',
        'warehouse_preview',
    )

    fieldsets = (
        (
            'Основная информация',
            {
                'fields': (
                    'company_name',
                    'subtitle',
                    'is_active',
                )
            },
        ),
        (
            'Брендинг и SEO',
            {
                'fields': (
                    'logo_image',
                    'logo_preview',
                    'favicon',
                    'favicon_preview',
                    'og_image',
                    'og_preview',
                    'seo_description',
                )
            },
        ),
        (
            'Контакты',
            {
                'fields': (
                    'phone',
                    'phone_link',
                    'manager_phone',
                    'manager_phone_link',
                    'email',
                    'address',
                    'extra_address',
                    'legal_address',
                    'work_time',
                    'whatsapp_link',
                    'telegram_link',
                    'vk_link',
                )
            },
        ),
        (
            'Реквизиты',
            {
                'fields': (
                    'inn',
                    'kpp',
                    'ogrn',
                )
            },
        ),
        (
            'Главная страница — тексты',
            {
                'fields': (
                    'hero_title',
                    'hero_text',
                    'home_note',
                    'metric_positions',
                    'metric_experience',
                    'metric_response',
                    'metric_delivery',
                    'footer_text',
                    'footer_subnote',
                )
            },
        ),
        (
            'Главная страница — фото первого экрана',
            {
                'fields': (
                    'hero_background',
                    'hero_background_preview',
                    'hero_card_image',
                    'hero_card_preview',
                )
            },
        ),
        (
            'Главная страница — фото метрик',
            {
                'fields': (
                    'metric_positions_image',
                    'metric_positions_preview',
                    'metric_experience_image',
                    'metric_experience_preview',
                    'metric_response_image',
                    'metric_response_preview',
                    'metric_delivery_image',
                    'metric_delivery_preview',
                )
            },
        ),
        (
            'Главная страница — фото категорий',
            {
                'fields': (
                    'category_combines_image',
                    'category_combines_preview',
                    'category_tractors_image',
                    'category_tractors_preview',
                    'category_popular_image',
                    'category_popular_preview',
                )
            },
        ),
        (
            'Главная страница — фото материалов',
            {
                'fields': (
                    'article_filters_image',
                    'article_filters_preview',
                    'article_bearings_image',
                    'article_bearings_preview',
                    'article_belt_image',
                    'article_belt_preview',
                )
            },
        ),
        (
            'Страница «О компании»',
            {
                'fields': (
                    'about_title',
                    'about_text',
                    'about_warehouse_note',
                    'about_warehouse_image',
                    'warehouse_preview',
                )
            },
        ),
        (
            'Тексты страниц',
            {
                'fields': (
                    'contacts_title',
                    'contacts_text',
                    'delivery_title',
                    'delivery_text',
                    'articles_title',
                    'articles_text',
                )
            },
        ),
    )

    def logo_preview(self, obj):
        return image_preview_html(obj.logo_image)
    logo_preview.short_description = 'Предпросмотр логотипа'

    def favicon_preview(self, obj):
        return image_preview_html(obj.favicon, 32)
    favicon_preview.short_description = 'Предпросмотр favicon'

    def og_preview(self, obj):
        return image_preview_html(obj.og_image)
    og_preview.short_description = 'Предпросмотр OpenGraph'

    def hero_background_preview(self, obj):
        return image_preview_html(obj.hero_background, 80)
    hero_background_preview.short_description = 'Предпросмотр фона главного экрана'

    def hero_card_preview(self, obj):
        return image_preview_html(obj.hero_card_image, 80)
    hero_card_preview.short_description = 'Предпросмотр фото карточки'

    def metric_positions_preview(self, obj):
        return image_preview_html(obj.metric_positions_image, 60)
    metric_positions_preview.short_description = 'Предпросмотр фото метрики "позиции"'

    def metric_experience_preview(self, obj):
        return image_preview_html(obj.metric_experience_image, 60)
    metric_experience_preview.short_description = 'Предпросмотр фото метрики "опыт"'

    def metric_response_preview(self, obj):
        return image_preview_html(obj.metric_response_image, 60)
    metric_response_preview.short_description = 'Предпросмотр фото метрики "время ответа"'

    def metric_delivery_preview(self, obj):
        return image_preview_html(obj.metric_delivery_image, 60)
    metric_delivery_preview.short_description = 'Предпросмотр фото метрики "доставка"'

    def category_combines_preview(self, obj):
        return image_preview_html(obj.category_combines_image, 70)
    category_combines_preview.short_description = 'Предпросмотр фото категории "комбайны"'

    def category_tractors_preview(self, obj):
        return image_preview_html(obj.category_tractors_image, 70)
    category_tractors_preview.short_description = 'Предпросмотр фото категории "тракторы"'

    def category_popular_preview(self, obj):
        return image_preview_html(obj.category_popular_image, 70)
    category_popular_preview.short_description = 'Предпросмотр фото категории "ремни/фильтры"'

    def article_filters_preview(self, obj):
        return image_preview_html(obj.article_filters_image, 70)
    article_filters_preview.short_description = 'Предпросмотр фото материала "фильтры"'

    def article_bearings_preview(self, obj):
        return image_preview_html(obj.article_bearings_image, 70)
    article_bearings_preview.short_description = 'Предпросмотр фото материала "подшипники"'

    def article_belt_preview(self, obj):
        return image_preview_html(obj.article_belt_image, 70)
    article_belt_preview.short_description = 'Предпросмотр фото материала "ремень"'

    def warehouse_preview(self, obj):
        return image_preview_html(obj.about_warehouse_image, 70)
    warehouse_preview.short_description = 'Предпросмотр фото склада'


_original_get_urls = admin.site.get_urls


def get_custom_admin_urls():
    urls = _original_get_urls()

    def dashboard_view(request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        context = {
            **admin.site.each_context(request),
            'title': 'Статистика сайта',
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

    return [
        path('dashboard/', admin.site.admin_view(dashboard_view), name='dashboard'),
        path('site-statistics/', admin.site.admin_view(dashboard_view), name='site_statistics'),
    ] + urls


admin.site.get_urls = get_custom_admin_urls