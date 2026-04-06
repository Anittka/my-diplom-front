// ========== ПЕРЕМЕННЫЕ ==========
const burgerBtn = document.getElementById('burgerBtn');
const mobileMenu = document.getElementById('mobileMenu');
const scrollTopBtn = document.getElementById('scrollTop');
const botBox = document.getElementById('botBox');
const botMessages = document.getElementById('botMessages');
const botInput = document.getElementById('botInput');

// Объект для хранения индексов галерей
const galleryIndices = {};

// ========== БУРГЕР-МЕНЮ ==========
if (burgerBtn && mobileMenu) {
    burgerBtn.addEventListener('click', function() {
        mobileMenu.classList.toggle('active');
        
        if (mobileMenu.classList.contains('active')) {
            burgerBtn.innerHTML = '<i class="fas fa-times"></i>';
            burgerBtn.style.background = 'var(--wheat-dark)';
            document.body.style.overflow = 'hidden';
        } else {
            burgerBtn.innerHTML = '<i class="fas fa-bars"></i>';
            burgerBtn.style.background = 'var(--wheat)';
            document.body.style.overflow = '';
        }
    });
}

// Функция закрытия мобильного меню
function closeMobileMenu() {
    if (mobileMenu) {
        mobileMenu.classList.remove('active');
        document.body.style.overflow = '';
    }
    if (burgerBtn) {
        burgerBtn.innerHTML = '<i class="fas fa-bars"></i>';
        burgerBtn.style.background = 'var(--wheat)';
    }
}

// Закрытие меню при клике на ссылку
document.querySelectorAll('.mobile-menu a').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
});

// ========== ИЗБРАННОЕ ==========
function toggleFavorite(element) {
    element.classList.toggle('active');
    const icon = element.querySelector('i');
    if (icon) {
        icon.classList.toggle('far');
        icon.classList.toggle('fas');
    }
}

// ========== FAQ АККОРДЕОН ==========
function toggleFaq(element) {
    if (!element) return;
    
    const faqId = element.dataset.faqId;
    let answer;
    
    if (faqId) {
        answer = document.getElementById(faqId);
    } else {
        const item = element.parentElement;
        answer = item.querySelector('.faq-answer');
    }
    
    if (answer) {
        document.querySelectorAll('.faq-answer.visible').forEach(openAnswer => {
            if (openAnswer !== answer) {
                openAnswer.classList.remove('visible');
                const openQuestion = openAnswer.previousElementSibling;
                if (openQuestion) openQuestion.classList.remove('active');
            }
        });
        
        answer.classList.toggle('visible');
        element.classList.toggle('active');
        
        const icon = element.querySelector('i');
        if (icon) {
            icon.style.transform = element.classList.contains('active') 
                ? 'rotate(180deg)' : 'rotate(0)';
        }
    }
}

// Инициализация FAQ
document.addEventListener('DOMContentLoaded', function() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', function(e) {
            e.preventDefault();
            toggleFaq(this);
        });
        
        question.addEventListener('touchstart', function(e) {
            e.preventDefault();
            toggleFaq(this);
        }, { passive: false });
    });
});

// ========== МОДАЛЬНЫЕ ОКНА ==========
function openCallModal() {
    const modal = document.getElementById('callModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    } else {
        alert('Форма заказа звонка откроется здесь');
    }
}

function openReviewModal() {
    const modal = document.getElementById('reviewModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        const ratingInput = document.getElementById('review-rating');
        if (ratingInput) ratingInput.value = '5';
        
        const stars = document.querySelectorAll('.rating-input span');
        stars.forEach((star, index) => {
            if (index < 5) {
                star.style.opacity = '1';
                star.style.color = '#FFD966';
            }
        });
    } else {
        alert('Форма отзыва откроется здесь');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// ========== РЕЙТИНГ ДЛЯ ОТЗЫВОВ ==========
function setRating(rating) {
    const ratingInput = document.getElementById('review-rating');
    if (ratingInput) ratingInput.value = rating;
    
    const stars = document.querySelectorAll('.rating-input span');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.opacity = '1';
            star.style.color = '#FFD966';
        } else {
            star.style.opacity = '0.3';
        }
    });
}

// ========== КНОПКА НАВЕРХ ==========
function checkScroll() {
    if (!scrollTopBtn) return;
    
    const isBotOpen = botBox && botBox.classList.contains('active');
    
    if (window.scrollY > 300 && !isBotOpen) {
        scrollTopBtn.classList.add('visible');
        scrollTopBtn.style.opacity = '1';
        scrollTopBtn.style.visibility = 'visible';
    } else {
        scrollTopBtn.classList.remove('visible');
        scrollTopBtn.style.opacity = '0';
        scrollTopBtn.style.visibility = 'hidden';
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

window.addEventListener('scroll', checkScroll);

// ========== МАСКА ДЛЯ ТЕЛЕФОНА ==========
function applyPhoneMask(input) {
    if (!input) return;
    
    input.addEventListener('input', function(e) {
        let x = e.target.value.replace(/\D/g, '').match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
        e.target.value = !x[2] ? x[1] : '+7 (' + x[2] + ') ' + x[3] + (x[4] ? '-' + x[4] : '') + (x[5] ? '-' + x[5] : '');
    });
}

document.querySelectorAll('input[type="tel"]').forEach(input => {
    applyPhoneMask(input);
});

// ========== ОБРАБОТКА ФОРМ ==========
function handleFormSubmit(form) {
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Проверяем заполнение обязательных полей
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#ff4444';
                field.style.backgroundColor = '#fff0f0';
                
                setTimeout(() => {
                    field.style.borderColor = '';
                    field.style.backgroundColor = '';
                }, 2000);
            } else {
                field.style.borderColor = '';
                field.style.backgroundColor = '';
            }
        });
        
        if (!isValid) {
            alert('Пожалуйста, заполните все обязательные поля');
            return;
        }
        
        // Проверяем согласие на обработку данных
        const checkbox = form.querySelector('input[type="checkbox"][required]');
        if (checkbox && !checkbox.checked) {
            alert('Необходимо согласие на обработку персональных данных');
            checkbox.style.outline = '2px solid #ff4444';
            setTimeout(() => {
                checkbox.style.outline = '';
            }, 2000);
            return;
        }
        
        alert('Спасибо! Мы свяжемся с вами в ближайшее время.');
        this.reset();
        
        const modal = this.closest('.modal-overlay');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Обработка всех форм
document.querySelectorAll('form').forEach(form => {
    if (!form.classList.contains('search-form')) {
        handleFormSubmit(form);
    }
});

// Специальная обработка для формы в блоке "Или напишите нам"
const feedbackFormShort = document.getElementById('feedbackFormShort');
if (feedbackFormShort) {
    feedbackFormShort.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('feedback-name-short')?.value.trim();
        const phone = document.getElementById('feedback-phone-short')?.value.trim();
        const message = document.getElementById('feedback-message-short')?.value.trim();
        const checkbox = this.querySelector('input[type="checkbox"]');
        
        if (!name) {
            alert('Пожалуйста, введите ваше имя');
            return;
        }
        
        if (!phone) {
            alert('Пожалуйста, введите ваш телефон');
            return;
        }
        
        if (checkbox && !checkbox.checked) {
            alert('Необходимо согласие на обработку персональных данных');
            return;
        }
        
        alert('Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.');
        this.reset();
    });
}

// ========== ФУНКЦИИ ДЛЯ КАТАЛОГА ==========
document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы каталога
    const products = document.querySelectorAll('.product-card');
    const filterChips = document.querySelectorAll('.filter-chip');
    const sortSelect = document.getElementById('sortSelect');
    const searchInput = document.querySelector('.search-form input');
    const productsCountSpan = document.getElementById('productsCount');
    
    if (products.length === 0) return;
    
    // Соответствие между текстом фильтра и значением data-category
    const categoryMap = {
        'Все': 'all',
        'Жгуты': 'жгуты',
        'Гидравлика': 'гидравлика',
        'Двигатель': 'двигатель',
        'Трансмиссия': 'трансмиссия',
        'Подшипники': 'подшипники',
        'Электрика': 'электрика',
        'Крепёж': 'крепёж',
        'Привод': 'привод',
        'Ротор': 'ротор'
    };
    
    // Функция фильтрации и поиска
    function filterProducts() {
        const activeFilter = document.querySelector('.filter-chip.active');
        let category = 'all';
        
        if (activeFilter) {
            const filterText = activeFilter.textContent.trim();
            category = categoryMap[filterText] || 'all';
        }
        
        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
        let visibleCount = 0;
        
        products.forEach(product => {
            const productCategory = product.dataset.category || '';
            const productTitle = product.querySelector('.product-title')?.textContent.toLowerCase() || '';
            const productArticle = product.querySelector('.product-article')?.textContent.toLowerCase() || '';
            
            const categoryMatch = category === 'all' || productCategory === category;
            const searchMatch = searchTerm === '' || 
                productTitle.includes(searchTerm) || 
                productArticle.includes(searchTerm);
            
            if (categoryMatch && searchMatch) {
                product.style.display = '';
                visibleCount++;
            } else {
                product.style.display = 'none';
            }
        });
        
        if (productsCountSpan) {
            productsCountSpan.textContent = visibleCount;
        }
        
        // Показываем сообщение, если ничего не найдено
        let noResultsMessage = document.querySelector('.no-results-message');
        if (visibleCount === 0) {
            if (!noResultsMessage) {
                noResultsMessage = document.createElement('div');
                noResultsMessage.className = 'no-results-message';
                noResultsMessage.innerHTML = `
                    <i class="fas fa-search" style="font-size: 3rem; color: var(--wheat); margin-bottom: 15px;"></i>
                    <p>По вашему запросу ничего не найдено.</p>
                    <p>Попробуйте изменить фильтр или позвоните нам!</p>
                    <div class="phone-large">
                        <i class="fas fa-phone-alt"></i>
                        <a href="tel:+79081881111">8 (908) 188-11-11</a>
                    </div>
                `;
                const productsGrid = document.querySelector('.products-grid');
                if (productsGrid && productsGrid.parentNode) {
                    productsGrid.parentNode.insertBefore(noResultsMessage, productsGrid.nextSibling);
                }
            }
            noResultsMessage.style.display = 'block';
        } else if (noResultsMessage) {
            noResultsMessage.style.display = 'none';
        }
        
        // После фильтрации применяем сортировку
        if (sortSelect && sortSelect.value !== 'default') {
            applySorting();
        }
    }
    
    // Функция применения сортировки
    function applySorting() {
        if (!sortSelect) return;
        
        const sortValue = sortSelect.value;
        const productsGrid = document.querySelector('.products-grid');
        if (!productsGrid) return;
        
        // Получаем только видимые товары
        const visibleProducts = Array.from(products).filter(product => product.style.display !== 'none');
        
        if (sortValue === 'default') {
            // Восстанавливаем исходный порядок по data-product-id
            visibleProducts.sort((a, b) => {
                const idA = parseInt(a.dataset.productId) || 0;
                const idB = parseInt(b.dataset.productId) || 0;
                return idA - idB;
            });
        } 
        else if (sortValue === 'name') {
            // Сортировка по названию (А-Я)
            visibleProducts.sort((a, b) => {
                const titleA = a.querySelector('.product-title')?.textContent.trim() || '';
                const titleB = b.querySelector('.product-title')?.textContent.trim() || '';
                return titleA.localeCompare(titleB, 'ru');
            });
        }
        else if (sortValue === 'name-desc') {
            // Сортировка по названию (Я-А)
            visibleProducts.sort((a, b) => {
                const titleA = a.querySelector('.product-title')?.textContent.trim() || '';
                const titleB = b.querySelector('.product-title')?.textContent.trim() || '';
                return titleB.localeCompare(titleA, 'ru');
            });
        }
        else if (sortValue === 'article') {
            // Сортировка по артикулу
            visibleProducts.sort((a, b) => {
                const articleA = a.querySelector('.product-article')?.textContent.trim() || '';
                const articleB = b.querySelector('.product-article')?.textContent.trim() || '';
                return articleA.localeCompare(articleB);
            });
        }
        
        // Переставляем элементы в DOM
        visibleProducts.forEach(product => {
            productsGrid.appendChild(product);
        });
    }
    
    // Добавляем обработчики на фильтры
    if (filterChips.length > 0) {
        filterChips.forEach(chip => {
            chip.addEventListener('click', function(e) {
                e.preventDefault();
                filterChips.forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                filterProducts();
            });
        });
    }
    
    // Добавляем обработчик на поиск
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterProducts();
        });
    }
    
    // Добавляем обработчик на сортировку
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            applySorting();
        });
    }
    
    // Инициализация - показываем все товары
    filterProducts();
});

// ========== ФУНКЦИИ ДЛЯ ГАЛЕРЕИ ТОВАРОВ ==========
function slideGallery(direction, productId) {
    const gallery = document.getElementById(`gallery-${productId}`);
    if (!gallery) return;
    
    const track = gallery.querySelector('.gallery-track');
    const slides = track.children;
    const totalSlides = slides.length;
    
    if (galleryIndices[productId] === undefined) {
        galleryIndices[productId] = 0;
    }
    
    let newIndex = galleryIndices[productId] + direction;
    
    if (newIndex < 0) newIndex = totalSlides - 1;
    if (newIndex >= totalSlides) newIndex = 0;
    
    track.style.transform = `translateX(-${newIndex * 100}%)`;
    galleryIndices[productId] = newIndex;
    
    updateDots(productId, newIndex);
}

function goToSlide(index, productId) {
    const gallery = document.getElementById(`gallery-${productId}`);
    if (!gallery) return;
    
    const track = gallery.querySelector('.gallery-track');
    const slides = track.children;
    
    if (index < 0 || index >= slides.length) return;
    
    track.style.transform = `translateX(-${index * 100}%)`;
    galleryIndices[productId] = index;
    
    updateDots(productId, index);
}

function updateDots(productId, activeIndex) {
    const gallery = document.getElementById(`gallery-${productId}`);
    if (!gallery) return;
    
    const productCard = gallery.closest('.product-card');
    if (!productCard) return;
    
    const dots = productCard.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
        if (index === activeIndex) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

// Инициализация галерей и свайпов
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.product-card').forEach(card => {
        const productId = card.dataset.productId;
        if (productId) {
            galleryIndices[productId] = 0;
        }
    });
    
    document.querySelectorAll('.gallery-container').forEach(container => {
        let startX = 0;
        let endX = 0;
        
        container.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        }, { passive: true });
        
        container.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            const diff = endX - startX;
            
            const gallery = container.closest('.product-gallery');
            const productCard = gallery?.closest('.product-card');
            const productId = productCard?.dataset.productId;
            
            if (productId && Math.abs(diff) > 30) {
                if (diff > 0) {
                    slideGallery(-1, productId);
                } else {
                    slideGallery(1, productId);
                }
            }
        }, { passive: true });
    });
});

// ===== ФУНКЦИИ БОТА =====
let waitingForArticle = false;
let waitingForModel = false;

function toggleBot(event) {
    if (event) event.stopPropagation();
    const botBox = document.getElementById('botBox');
    if (botBox) {
        botBox.classList.toggle('active');
    }
}

function closeBot() {
    const botBox = document.getElementById('botBox');
    if (botBox) {
        botBox.classList.remove('active');
    }
}

function addMessage(text, isUser = false) {
    const container = document.getElementById('botMessages');
    if (!container) return;
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    div.innerHTML = text.replace(/\n/g, '<br>');
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function showTyping() {
    const container = document.getElementById('botMessages');
    if (!container) return;
    const typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.id = 'typingIndicator';
    typing.innerHTML = '<span></span><span></span><span></span>';
    container.appendChild(typing);
    container.scrollTop = container.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById('typingIndicator');
    if (el) el.remove();
}

function botAnswer(topic) {
    waitingForArticle = false;
    waitingForModel = false;
    switch(topic) {
        case 'наличие':
            addMessage('Введите артикул запчасти (например: 152.10.28.570A):');
            waitingForArticle = true;
            break;
        case 'цена':
            addMessage('💰 Для уточнения цены лучше позвонить: <strong>8 (908) 188-11-11</strong>');
            break;
        case 'подбор':
            addMessage('🔧 Напишите модель комбайна (Дон, Вектор, Торум, Акрос, Бюлер)');
            waitingForModel = true;
            break;
        case 'заявка':
            addMessage('📝 Оставьте заявку через форму на сайте или звоните: <strong>8 (908) 188-11-11</strong>');
            break;
        case 'каталог':
            addMessage('📚 Наш каталог запчастей: <a href="catalog.html" style="color: #D4A55C;">Перейти в каталог →</a>');
            break;
        case 'адрес':
            addMessage('📍 Наш адрес: г. Аксай, ул. Ленина, 48<br>📞 Телефон: <strong>8 (908) 188-11-11</strong>');
            break;
        default:
            addMessage('Напишите: наличие, цена, подбор, заявка, каталог, адрес');
    }
}

function sendBotMessage() {
    const input = document.getElementById('botInput');
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, true);
    input.value = '';
    showTyping();
    setTimeout(() => {
        hideTyping();
        if (waitingForArticle) {
            addMessage(`📞 По запросу "${text}" лучше позвонить: 8 (908) 188-11-11`);
            waitingForArticle = false;
        } else if (waitingForModel) {
            addMessage(`🔧 По модели "${text}" поможем подобрать. Звоните: 8 (908) 188-11-11`);
            waitingForModel = false;
        } else {
            addMessage('📞 Лучше позвонить по телефону <strong>8 (908) 188-11-11</strong>. Там ответят быстрее!');
        }
    }, 1000);
}

// Закрытие бота при клике вне его области
document.addEventListener('click', function(e) {
    const widget = document.getElementById('botWidget');
    const box = document.getElementById('botBox');
    if (box && box.classList.contains('active') && widget && !widget.contains(e.target)) {
        closeBot();
    }
});

// Enter в поле ввода
document.getElementById('botInput')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendBotMessage();
});
