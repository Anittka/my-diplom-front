from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse


class Category(models.Model):
    name        = models.CharField('Название', max_length=120)
    slug        = models.SlugField('URL-имя', max_length=140, unique=True)
    description = models.TextField('Описание', blank=True)
    image       = models.ImageField('Изображение', upload_to='categories/', blank=True, null=True)
    is_active   = models.BooleanField('Активна', default=True)
    order       = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name        = 'Категория'
        verbose_name_plural = 'Категории'
        ordering            = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog') + f'?category={self.slug}'


class Product(models.Model):
    category    = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products',
        verbose_name='Категория',
    )
    title        = models.CharField('Название', max_length=180)
    slug         = models.SlugField('URL-имя', max_length=200, unique=True)
    article      = models.CharField('Артикул', max_length=120, blank=True)
    description  = models.TextField('Описание', blank=True)
    availability = models.CharField('Наличие', max_length=120, default='В наличии')
    price_note   = models.CharField('Цена/пометка', max_length=120, default='Цена по телефону')
    is_featured  = models.BooleanField('Показывать на главной', default=False)
    is_active    = models.BooleanField('Показывать на сайте', default=True)
    created_at   = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name        = 'Товар'
        verbose_name_plural = 'Товары'
        ordering            = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    def first_image(self):
        """Первое фото товара или None."""
        return self.images.first()

    @property
    def has_images(self):
        return self.images.exists()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар',
    )
    image = models.ImageField('Изображение', upload_to='products/')
    alt   = models.CharField('Alt-текст', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name        = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering            = ['order']

    def __str__(self):
        return self.alt or self.product.title


class Lead(models.Model):
    REQUEST_TYPES = [
        ('callback',  'Заказать звонок'),
        ('selection', 'Подбор детали'),
        ('delivery',  'Доставка'),
        ('product',   'Заявка по товару'),
        ('price',     'Уточнение цены'),
        ('general',   'Общий вопрос'),
    ]

    STATUS_CHOICES = [
        ('new',      'Новая'),
        ('in_work',  'В работе'),
        ('waiting',  'Ждёт уточнения'),
        ('answered', 'Ответ отправлен клиенту'),
        ('done',     'Завершена'),
        ('rejected', 'Неактуально / отказ'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Обычная'),
        ('high',   'Срочная'),
        ('season', 'Сезонная'),
        ('large',  'Крупный заказ'),
    ]

    name             = models.CharField('Имя', max_length=120)
    phone            = models.CharField('Телефон', max_length=40)
    email            = models.EmailField('Email', blank=True)
    message          = models.TextField('Сообщение', blank=True)
    request_type     = models.CharField('Тип заявки', max_length=80, choices=REQUEST_TYPES, default='general')
    source_page      = models.CharField('Страница отправки', max_length=200, blank=True)
    status           = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    priority         = models.CharField('Приоритет', max_length=20, choices=PRIORITY_CHOICES, default='normal')
    manager_comment  = models.TextField('Комментарий менеджера', blank=True)
    privacy_accepted = models.BooleanField('Согласие на обработку ПДн', default=False)
    attachment       = models.FileField('Файл/фото к заявке', upload_to='lead_attachments/', blank=True, null=True)
    created_at       = models.DateTimeField('Дата заявки', auto_now_add=True)
    updated_at       = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name        = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering            = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone}'

    @property
    def is_new(self):
        return self.status == 'new'

    @property
    def is_high_priority(self):
        return self.priority == 'high'

    @property
    def phone_digits(self):
        """Только цифры из номера телефона — для href и WhatsApp."""
        return ''.join(ch for ch in self.phone if ch.isdigit())

    @property
    def whatsapp_url(self):
        d = self.phone_digits
        return f'https://wa.me/{d}' if d else '#'

    @property
    def tel_href(self):
        d = self.phone_digits
        return f'+{d}' if d else self.phone

    @property
    def has_attachment(self):
        return bool(self.attachment)


class LeadStatusHistory(models.Model):
    lead       = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Заявка',
    )
    old_status = models.CharField('Старый статус', max_length=20, blank=True)
    new_status = models.CharField('Новый статус', max_length=20)
    comment    = models.CharField('Комментарий', max_length=255, blank=True)
    created_at = models.DateTimeField('Дата изменения', auto_now_add=True)

    class Meta:
        verbose_name        = 'История статуса заявки'
        verbose_name_plural = 'История статусов заявок'
        ordering            = ['-created_at']

    def __str__(self):
        return f'Заявка #{self.lead_id}: {self.old_status} → {self.new_status}'


class Article(models.Model):
    title      = models.CharField('Заголовок', max_length=200)
    slug       = models.SlugField('URL-имя', max_length=220, unique=True)
    tag        = models.CharField('Метка/рубрика', max_length=120, blank=True)
    short_text = models.TextField('Краткое описание', blank=True)
    text       = models.TextField('Текст')
    image      = models.ImageField('Изображение', upload_to='articles/', blank=True, null=True)
    is_active  = models.BooleanField('Показывать', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name        = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering            = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])


class SiteSettings(models.Model):
    company_name = models.CharField(
        'Название компании', max_length=150,
        default='АГРОМАРКЕТ ТОРШЕНКО',
    )
    subtitle = models.CharField(
        'Подзаголовок', max_length=200,
        default='Запчасти для сельхозтехники с 2014 года',
    )

    logo_image = models.ImageField('Логотип сайта', upload_to='site/', blank=True, null=True)
    favicon    = models.ImageField('Favicon сайта', upload_to='site/', blank=True, null=True)
    og_image   = models.ImageField('OpenGraph-изображение', upload_to='site/', blank=True, null=True)

    # ── Главная страница — фото ──────────────────────────────
    hero_background      = models.ImageField('Фон главного экрана', upload_to='site/home/', blank=True, null=True,
                                              help_text='Большое фоновое изображение первого экрана.')
    hero_card_image      = models.ImageField('Фото в карточке главного экрана', upload_to='site/home/', blank=True, null=True,
                                              help_text='Фото справа в блоке «Как удобнее начать работу».')
    metric_positions_image  = models.ImageField('Фото метрики: позиции', upload_to='site/home/', blank=True, null=True)
    metric_experience_image = models.ImageField('Фото метрики: опыт', upload_to='site/home/', blank=True, null=True)
    metric_response_image   = models.ImageField('Фото метрики: время ответа', upload_to='site/home/', blank=True, null=True)
    metric_delivery_image   = models.ImageField('Фото метрики: доставка', upload_to='site/home/', blank=True, null=True)
    category_combines_image = models.ImageField('Фото категории: комбайны', upload_to='site/home/', blank=True, null=True)
    category_tractors_image = models.ImageField('Фото категории: тракторы', upload_to='site/home/', blank=True, null=True)
    category_popular_image  = models.ImageField('Фото категории: ремни, фильтры, подшипники', upload_to='site/home/', blank=True, null=True)
    article_filters_image   = models.ImageField('Фото материала: фильтры', upload_to='site/home/', blank=True, null=True)
    article_bearings_image  = models.ImageField('Фото материала: подшипники', upload_to='site/home/', blank=True, null=True)
    article_belt_image      = models.ImageField('Фото материала: ремень', upload_to='site/home/', blank=True, null=True)

    # ── Контакты ─────────────────────────────────────────────
    phone              = models.CharField('Основной телефон', max_length=50, default='8 (908) 188-11-11')
    phone_link         = models.CharField('Основной телефон для ссылки', max_length=50, default='+79081881111',
                                          help_text='Формат: +79081881111')
    manager_phone      = models.CharField('Телефон менеджера', max_length=50, default='8 (908) 123-45-67')
    manager_phone_link = models.CharField('Телефон менеджера для ссылки', max_length=50, default='+79081234567',
                                          help_text='Формат: +79081234567')
    email              = models.EmailField('Email', default='info@agromarkettorshenko.ru')
    address            = models.CharField('Основной адрес / склад', max_length=255, default='г. Аксай, ул. Ленина, 48')
    extra_address      = models.CharField('Дополнительный склад', max_length=255, blank=True,
                                          default='Ростовская область, Аксайский район, рабочая выдача по согласованию')
    legal_address      = models.CharField('Юридический адрес', max_length=255, blank=True,
                                          default='Ростовская область, г. Аксай')
    work_time          = models.CharField('Режим работы', max_length=120, default='Пн–Сб: 08:00–18:00')
    whatsapp_link      = models.URLField('Ссылка WhatsApp', blank=True, default='https://wa.me/79081881111',
                                         help_text='Например: https://wa.me/79081881111')
    telegram_link      = models.URLField('Ссылка Telegram', blank=True)
    vk_link            = models.URLField('Ссылка VK', blank=True)
    inn                = models.CharField('ИНН', max_length=300, blank=True, default='Указывается в договорных документах')
    kpp                = models.CharField('КПП', max_length=300, blank=True, default='Указывается при наличии')
    ogrn               = models.CharField('ОГРН', max_length=300, blank=True, default='Указывается в договорных документах')

    # ── Тексты главной страницы ──────────────────────────────
    hero_title       = models.CharField('Заголовок главной страницы', max_length=255,
                                         default='Запчасти для комбайнов, тракторов и сельхозтехники')
    hero_text        = models.TextField('Текст главного экрана',
                                         default='Помогаем быстро подобрать ходовые позиции, уточнить наличие и согласовать поставку без лишней переписки.')
    home_note        = models.CharField('Короткая заметка на главной', max_length=255, blank=True,
                                         default='Если нужна консультация по подбору, отправьте заявку — менеджер свяжется с вами в рабочее время.')
    metric_positions = models.CharField('Метрика: количество позиций', max_length=50, blank=True, default='5000+')
    metric_experience= models.CharField('Метрика: опыт', max_length=50, blank=True, default='10+ лет')
    metric_response  = models.CharField('Метрика: время ответа', max_length=50, blank=True, default='15 минут')
    metric_delivery  = models.CharField('Метрика: доставка', max_length=50, blank=True, default='По РФ')
    footer_text      = models.CharField('Текст подвала', max_length=255, blank=True,
                                         default='© 2026 АГРОМАРКЕТ ТОРШЕНКО. Все права защищены.')
    footer_subnote   = models.CharField('Описание в подвале', max_length=255, blank=True,
                                         default='Подбор и поставка запчастей для сельхозтехники: каталог, заявка, доставка и контакты в одном рабочем маршруте.')
    seo_description  = models.CharField('SEO-описание по умолчанию', max_length=255, blank=True,
                                         default='Запчасти для сельхозтехники, подбор деталей, консультация и поставка по Ростовской области и России.')

    # ── О компании ───────────────────────────────────────────
    about_title           = models.CharField('Заголовок страницы О компании', max_length=255,
                                              default='Подбор и поставка запчастей для сельхозтехники с опорой на реальную рабочую задачу')
    about_text            = models.TextField('Основной текст страницы О компании',
                                              default='АГРОМАРКЕТ ТОРШЕНКО занимается подбором и поставкой запчастей для сельхозтехники.')
    about_warehouse_note  = models.TextField('Описание склада / фото на странице О компании', blank=True,
                                              default='Работа строится вокруг реальных запросов клиентов.')
    about_warehouse_image = models.ImageField('Фото склада / компании', upload_to='site/', blank=True, null=True)
    #about_preparing_image = models.ImageField('Фото подготовки заказа', upload_to='site/about/', blank=True, null=True)
    #about_delivery_image = models.ImageField('Фото выдачи/отправки', upload_to='site/about/', blank=True, null=True)

    # ── Тексты остальных страниц ─────────────────────────────
    contacts_title  = models.CharField('Заголовок страницы Контакты', max_length=255, default='Как связаться с компанией')
    contacts_text   = models.TextField('Описание страницы Контакты',
                                        default='Для срочных вопросов удобнее сразу позвонить.')
    delivery_title  = models.CharField('Заголовок страницы Доставка', max_length=255,
                                        default='Как согласовывается получение и отправка заказа')
    delivery_text   = models.TextField('Описание страницы Доставка',
                                        default='После подтверждения позиции менеджер согласовывает наличие, сроки, самовывоз или транспортную компанию.')
    articles_title  = models.CharField('Заголовок страницы Полезные советы', max_length=255,
                                        default='Материалы по подбору, обслуживанию и сезонной подготовке техники')
    articles_text   = models.TextField('Описание страницы Полезные советы',
                                        default='Короткие практические материалы, которые помогают быстрее сформулировать запрос.')

    is_active = models.BooleanField('Активные настройки', default=True)

    class Meta:
        verbose_name        = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.company_name

    @property
    def seo_default_description(self):
        return self.seo_description

    def clean(self):
        if self.is_active and SiteSettings.objects.exclude(pk=self.pk).filter(is_active=True).exists():
            raise ValidationError('Активной может быть только одна запись настроек сайта.')

    def save(self, *args, **kwargs):
        if self.is_active:
            SiteSettings.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)