from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from siteapp.models import Category, Product, ProductImage, Article, SiteSettings, Lead


class Command(BaseCommand):
    help = 'Создаёт демо-данные для дипломного проекта'

    def attach_product_images(self, product, image_names):
        if product.images.exists():
            return
        static_img = Path(settings.BASE_DIR) / 'siteapp' / 'static' / 'siteapp' / 'img'
        for order, image_name in enumerate(image_names):
            src = static_img / image_name
            if not src.exists():
                src = static_img / 'placeholder-product.png'
            if src.exists():
                with src.open('rb') as f:
                    image = ProductImage(product=product, alt=product.title, order=order)
                    image.image.save(image_name, File(f), save=True)

    def handle(self, *args, **options):
        settings_obj, _ = SiteSettings.objects.get_or_create(is_active=True)
        settings_obj.company_name = 'АГРОМАРКЕТ ТОРШЕНКО'
        settings_obj.subtitle = 'Запчасти для сельхозтехники с 2014 года'
        settings_obj.phone = '8 (908) 188-11-11'
        settings_obj.phone_link = '+79081881111'
        settings_obj.manager_phone = '8 (908) 123-45-67'
        settings_obj.manager_phone_link = '+79081234567'
        settings_obj.email = 'info@agromarkettorshenko.ru'
        settings_obj.address = 'г. Аксай, ул. Ленина, 48'
        settings_obj.extra_address = 'Ростовская область, Аксайский район, рабочая выдача по согласованию'
        settings_obj.legal_address = 'Ростовская область, г. Аксай'
        settings_obj.work_time = 'Пн–Сб: 08:00–18:00'
        settings_obj.whatsapp_link = 'https://wa.me/79081881111'
        settings_obj.inn = 'Указывается в договорных документах'
        settings_obj.kpp = 'Указывается при наличии'
        settings_obj.ogrn = 'Указывается в договорных документах'
        settings_obj.hero_title = 'Запчасти для комбайнов, тракторов и сельхозтехники'
        settings_obj.hero_text = 'Помогаем быстро подобрать ходовые позиции, уточнить наличие и согласовать поставку без лишней переписки.'
        settings_obj.home_note = 'Если нужна консультация по подбору, отправьте заявку — менеджер свяжется с вами в рабочее время.'
        settings_obj.footer_text = '© 2026 АГРОМАРКЕТ ТОРШЕНКО. Все права защищены.'
        settings_obj.seo_description = 'Запчасти для сельхозтехники, подбор деталей, консультация и поставка по Ростовской области и России.'
        settings_obj.about_title = 'Подбор и поставка запчастей для сельхозтехники с опорой на реальную рабочую задачу'
        settings_obj.about_text = 'АГРОМАРКЕТ ТОРШЕНКО занимается подбором и поставкой запчастей для сельхозтехники. В работе важен не просто каталог, а понимание того, что именно нужно клиенту: артикул, совместимость, модель техники, срок поставки и удобный формат получения.'
        settings_obj.about_warehouse_note = 'Работа строится вокруг реальных запросов клиентов: подбор по артикулу, фото, модели техники и согласование поставки.'
        settings_obj.contacts_title = 'Как связаться с компанией'
        settings_obj.contacts_text = 'Для срочных вопросов удобнее сразу позвонить. Для плановых обращений, подбора и уточнения условий можно оставить заявку через сайт.'
        settings_obj.delivery_title = 'Как согласовывается получение и отправка заказа'
        settings_obj.delivery_text = 'После подтверждения позиции менеджер согласовывает наличие, сроки, самовывоз или транспортную компанию.'
        settings_obj.articles_title = 'Материалы по подбору, обслуживанию и сезонной подготовке техники'
        settings_obj.articles_text = 'Практические советы, которые помогают быстрее сформулировать запрос и избежать типовых ошибок при подборе деталей.'
        settings_obj.save()

        categories_data = [
            ('Жгуты', 'zhguty', 'Электрика, жгуты, разъёмы и элементы подключения для сельхозтехники.'),
            ('Ремни', 'remni', 'Приводные ремни, шкивы и сопутствующие элементы для обслуживания техники.'),
            ('Фильтры', 'filtry', 'Фильтры, датчики и элементы планового обслуживания.'),
            ('Подшипники', 'podshipniki', 'Подшипниковые узлы, корпусные подшипники и комплектующие.'),
            ('Гидравлика', 'gidravlika', 'Насосы, фланцы, муфты, гидроаккумуляторы и другие гидроэлементы.'),
        ]
        categories = {}
        for order, (name, slug, description) in enumerate(categories_data, start=1):
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={'name': name, 'description': description, 'order': order, 'is_active': True}
            )
            categories[slug] = category

        products = [
            ('Жгут верхнего решета', 'jgut-verhnego-resheta', '152.10.28.570A', 'zhguty', ['jgut-verh-1.jpg', 'jgut-verh-2.jpg', 'jgut-verh-3.jpg']),
            ('Жгут нижнего решета', 'jgut-nizhnego-resheta', '152.10.28.580', 'zhguty', ['jgut-niz-1.jpg', 'jgut-niz-2.jpg', 'jgut-niz-3.jpg']),
            ('Гидроаккумулятор', 'gidroakkumulyator', 'GA-120', 'gidravlika', ['gidroakkum-1.jpg', 'gidroakkum-2.jpg']),
            ('Фланец гидравлический', 'flanec-gidravlicheskiy', 'FL-300', 'gidravlika', ['flyanec-1.jpg', 'flyanec-2.jpg', 'flyanec-3.jpg']),
            ('Насос гидравлический', 'nasos-gidravlicheskiy', 'NS-204', 'gidravlika', ['nasos-1.jpg', 'nasos-2.jpg', 'nasos-3.jpg', 'nasos-4.jpg', 'nasos-5.jpg']),
            ('Подшипниковый узел', 'podshipnikovyy-uzel', 'POD-208', 'podshipniki', ['podshipnik-1.jpg', 'podshipnik-2.jpg', 'podshipnik-3.jpg']),
            ('Муфта соединительная', 'mufta-soedinitelnaya', 'MF-400', 'gidravlika', ['mufta-1.jpg', 'mufta-2.jpg']),
            ('Шкив приводной', 'shkiv-privodnoy', 'SHK-110', 'remni', ['golovka-1.jpg', 'golovka-2.jpg']),
            ('Датчик системы контроля', 'datchik-sistemy-kontrolya', 'DCH-01', 'filtry', ['datchik-1.jpg', 'datchik-2.jpg']),
            ('Крепёжный болт', 'krepezhnyy-bolt', 'BLT-01', 'remni', ['bolt-1.jpg', 'bolt-2.jpg']),
            ('Термостат', 'termostat', 'TRM-01', 'filtry', ['termostat-1.jpg', 'termostat-2.jpg']),
            ('Подшипник корпусной', 'podshipnik-korpusnoy', 'POD-KR-01', 'podshipniki', ['podshipnik-4.jpg', 'podshipnik-5.jpg']),
        ]
        for index, (title, slug, article, category_slug, image_names) in enumerate(products, start=1):
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'article': article,
                    'category': categories[category_slug],
                    'description': 'Позиция каталога. Название, артикул, фото и статус можно изменить в админ-панели.',
                    'availability': 'В наличии',
                    'price_note': 'Цена по телефону',
                    'is_featured': index <= 8,
                    'is_active': True,
                }
            )
            self.attach_product_images(product, image_names)

        articles = [
            {
                'slug': 'kak-vybrat-maslo-dlya-gidrosistemy-kombayna',
                'title': 'Как выбрать масло для гидросистемы комбайна',
                'tag': 'Гидросистема',
                'short_text': 'На что обратить внимание при выборе масла для гидросистемы сельхозтехники.',
                'text': 'Выбор масла начинается не с бренда, а с требований производителя техники, вязкости и условий работы. Перед заменой важно учитывать сезонность, рабочую температуру и состояние самой гидросистемы. Если техника работает в тяжёлых условиях, интервал обслуживания лучше уточнять заранее. В заявке менеджеру полезно указать модель техники, тип узла и текущую жидкость.'
            },
            {
                'slug': 'priznaki-iznosa-podshipnikov-pered-sezonom',
                'title': 'Признаки износа подшипников перед сезоном',
                'tag': 'Диагностика',
                'short_text': 'Шум, нагрев, люфт и вибрация — признаки, которые нельзя игнорировать.',
                'text': 'Повышенный шум, нагрев, люфт и вибрация — первые сигналы, которые нельзя откладывать до поломки. Перед сезоном лучше проверить рабочие узлы, состояние смазки, герметичность и посадочные места. При подборе подшипника важно знать размер, тип крепления, нагрузку и модель техники.'
            },
            {
                'slug': 'kak-podgotovit-kombayn-k-hraneniyu',
                'title': 'Как подготовить комбайн к хранению',
                'tag': 'Межсезонье',
                'short_text': 'Что проверить после сезона, чтобы весной не столкнуться с простоями.',
                'text': 'Перед хранением технику очищают, осматривают основные узлы и фиксируют позиции, которые лучше заменить заранее. Особое внимание уделяют ремням, фильтрам, подшипникам, гидравлическим соединениям и электрике. Такой подход помогает не переносить ремонт на начало сезона.'
            },
            {
                'slug': 'kak-podobrat-remen-po-razmeru-i-markirovke',
                'title': 'Как подобрать ремень по размеру и маркировке',
                'tag': 'Ремни',
                'short_text': 'Короткий ориентир по маркировке, длине, профилю и условиям работы ремня.',
                'text': 'Для подбора ремня желательно указать маркировку, ширину, профиль, длину и узел, где он установлен. Если маркировка стерта, помогает фото старого ремня и модель техники. Важно учитывать не только размер, но и условия работы: нагрузку, температуру, влажность и состояние шкивов.'
            },
            {
                'slug': 'kak-sformulirovat-zayavku-na-podbor-detali',
                'title': 'Как правильно отправить заявку на подбор детали',
                'tag': 'Подбор',
                'short_text': 'Какие данные помогают менеджеру быстрее подобрать нужную позицию.',
                'text': 'Чтобы менеджер быстрее подобрал деталь, укажите артикул, модель техники, фото узла, размеры и описание задачи. Если нужна срочная поставка, сразу напишите желаемый срок и город получения. Чем точнее исходные данные, тем меньше риск ошибки при подборе.'
            },
            {
                'slug': 'chto-proverit-v-gidravlike-pered-rabotoy',
                'title': 'Что проверить в гидравлике перед началом работы',
                'tag': 'Гидравлика',
                'short_text': 'Базовая проверка гидросистемы перед сезонной нагрузкой.',
                'text': 'Перед началом активной работы стоит проверить уровень жидкости, состояние шлангов, соединений, фланцев, насосов и гидроаккумуляторов. Следы подтекания, рывки в работе и посторонний шум лучше не игнорировать. При подборе гидравлической детали полезны фото, параметры и модель техники.'
            },
        ]
        for item in articles:
            Article.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'tag': item['tag'],
                    'short_text': item['short_text'],
                    'text': item['text'],
                    'is_active': True,
                }
            )

        demo_leads = [
            ('Алексей', '8 (900) 000-00-00', 'selection', 'Нужен подбор подшипника по фото', 'new'),
            ('Игорь', '8 (900) 111-22-33', 'price', 'Уточнить цену на жгут верхнего решета', 'in_work'),
            ('Сергей', '8 (900) 222-33-44', 'delivery', 'Интересует доставка транспортной компанией', 'done'),
            ('Марина', '8 (900) 333-44-55', 'callback', 'Перезвоните по заказу', 'new'),
            ('Павел', '8 (900) 444-55-66', 'product', 'Насос гидравлический, наличие и срок', 'done'),
        ]
        for name, phone, request_type, message, status in demo_leads:
            Lead.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'message': message,
                    'request_type': request_type,
                    'source_page': 'seed_demo',
                    'status': status,
                }
            )

        self.stdout.write(self.style.SUCCESS('Демо-данные для дипломного проекта созданы и обновлены.'))
