/* =========================================================
   MAIN.JS
   АГРОМАРКЕТ ТОРШЕНКО
   ФИНАЛЬНАЯ ВЕРСИЯ (шапка не скрывается на мобильных)
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  initHeaderRevealOnScroll();
  initMobileMenu();
  initModals();
  initPhoneMask();
  initFormSecurityFields();
  initToastForms();
  initFaq();
  initScrollTop();

  initProductGalleries();
  initImageLightbox();

  initCatalogFiltering();
  initCatalogSorting();
  initCatalogSearch();
  initCatalogState();
  initRequestButtons();
  
  initSiteSearch();
});


/* =========================================================
   0. ШАПКА: НЕ СКРЫВАЕТСЯ НА МОБИЛЬНЫХ
   ========================================================= */

function initHeaderRevealOnScroll() {
  const header = document.getElementById("siteHeader");
  if (!header) return;

  // На мобильных устройствах шапка НЕ СКРЫВАЕТСЯ
  if (window.innerWidth <= 980) {
    header.classList.remove("is-compact");
    header.style.transform = "translateY(0)";
    header.style.position = "sticky";
    header.style.top = "0";
    return;
  }

  let lastY = window.scrollY;
  let ticking = false;
  let hidden = false;

  const updateHeader = () => {
    const currentY = window.scrollY;

    if (currentY > 100) {
      header.classList.add("is-compact");
    } else {
      header.classList.remove("is-compact");
    }

    if (currentY <= 120) {
      header.style.transform = "translateY(0)";
      hidden = false;
      lastY = currentY;
      ticking = false;
      return;
    }

    if (currentY > lastY && !hidden && currentY > 120) {
      header.style.transform = "translateY(-100%)";
      hidden = true;
    }

    if (currentY < lastY && hidden) {
      header.style.transform = "translateY(0)";
      hidden = false;
    }

    lastY = currentY;
    ticking = false;
  };

  window.addEventListener("scroll", () => {
    if (window.innerWidth <= 980) return; // на мобильных не реагируем
    if (!ticking) {
      requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });
}


/* =========================================================
   1. МОБИЛЬНОЕ МЕНЮ — ИСПРАВЛЕНО
   ========================================================= */

function initMobileMenu() {
  const toggle = document.getElementById("mobileToggle");
  const menu = document.getElementById("mobileMenu");

  if (!toggle || !menu) return;

  const openMenu = () => {
    menu.classList.add("is-open");
    menu.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("modal-open");
  };

  const closeMenu = () => {
    menu.classList.remove("is-open");
    menu.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("modal-open");
  };

  toggle.addEventListener("click", (event) => {
    event.stopPropagation();
    const expanded = toggle.getAttribute("aria-expanded") === "true";
    expanded ? closeMenu() : openMenu();
  });

  // Кнопка закрытия (если есть)
  const closeBtn = menu.querySelector(".mobile-menu__close");
  if (closeBtn) {
    closeBtn.addEventListener("click", closeMenu);
  }

  // Закрываем меню при клике на ссылку или кнопку
  menu.querySelectorAll("a, button").forEach((item) => {
    item.addEventListener("click", closeMenu);
  });

  // Закрываем меню при клике вне его
  document.addEventListener("click", (event) => {
    if (menu.hidden) return;
    if (!menu.contains(event.target) && !toggle.contains(event.target)) {
      closeMenu();
    }
  });

  // При изменении размера окна на десктоп — закрываем меню
  window.addEventListener("resize", () => {
    if (window.innerWidth > 980) {
      closeMenu();
    }
  });
}


/* =========================================================
   2. МОДАЛКИ (без изменений)
   ========================================================= */

function initModals() {
  const openButtons = document.querySelectorAll("[data-open-modal]");
  const closeButtons = document.querySelectorAll("[data-close-modal]");
  const modals = document.querySelectorAll(".modal");

  if (!modals.length) return;

  const applyModalContext = (trigger, modal) => {
    if (!modal || !trigger) return;

    const titleEl = modal.querySelector("#callbackModalTitle");
    const requestType = modal.querySelector("#modalRequestType");
    const requestMessage = modal.querySelector("#modalRequestMessage");
    const sourcePage = modal.querySelector("#modalSourcePage");

    const buttonText = (trigger.textContent || "").trim();
    const modalTitle = trigger.dataset.modalTitle || buttonText || "Оставить заявку";
    const type = trigger.dataset.requestType || inferRequestType(buttonText);
    const message = trigger.dataset.requestMessage || "";

    if (titleEl) titleEl.textContent = modalTitle;
    if (requestType) requestType.value = type;
    if (requestMessage) requestMessage.value = message;

    if (sourcePage) {
      sourcePage.value =
        document.body.dataset.page ||
        window.location.pathname ||
        "Главная страница";
    }
  };

  const openModal = (modalId, trigger = null) => {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    applyModalContext(trigger, modal);

    modal.hidden = false;
    document.body.classList.add("modal-open");

    const firstField = modal.querySelector(
      "input:not([type=hidden]), textarea, select, button"
    );

    if (firstField) {
      setTimeout(() => firstField.focus(), 50);
    }
  };

  const closeModal = (modalId) => {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.hidden = true;
    document.body.classList.remove("modal-open");
  };

  openButtons.forEach((button) => {
    button.addEventListener("click", () => {
      openModal(button.dataset.openModal, button);
    });
  });

  closeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      closeModal(button.dataset.closeModal);
    });
  });

  modals.forEach((modal) => {
    modal.addEventListener("click", (event) => {
      const dialog = modal.querySelector(".modal__dialog");
      if (!dialog) return;

      if (
        !dialog.contains(event.target) &&
        event.target.classList.contains("modal__overlay")
      ) {
        modal.hidden = true;
        document.body.classList.remove("modal-open");
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;

    modals.forEach((modal) => {
      if (!modal.hidden) {
        modal.hidden = true;
        document.body.classList.remove("modal-open");
      }
    });
  });
}

function inferRequestType(text) {
  const normalized = (text || "").toLowerCase();

  if (normalized.includes("звон")) return "callback";
  if (normalized.includes("подбор") || normalized.includes("детал")) return "selection";
  if (normalized.includes("достав")) return "delivery";
  if (normalized.includes("прайс") || normalized.includes("цен")) return "price";
  if (normalized.includes("товар") || normalized.includes("позици")) return "product";

  return "general";
}


/* =========================================================
   3. ФОРМЫ + TOAST
   ========================================================= */

function initPhoneMask() {
  const inputs = document.querySelectorAll('input[type="tel"], input[name="phone"]');

  const formatPhone = (value) => {
    let digits = (value || "").replace(/\D/g, "");

    if (digits.startsWith("8")) {
      digits = "7" + digits.slice(1);
    }

    if (!digits.startsWith("7")) {
      digits = "7" + digits;
    }

    digits = digits.slice(0, 11);

    const p1 = digits.slice(1, 4);
    const p2 = digits.slice(4, 7);
    const p3 = digits.slice(7, 9);
    const p4 = digits.slice(9, 11);

    let result = "+7";

    if (p1) result += ` (${p1}`;
    if (p1.length === 3) result += ")";
    if (p2) result += ` ${p2}`;
    if (p3) result += `-${p3}`;
    if (p4) result += `-${p4}`;

    return result;
  };

  inputs.forEach((input) => {
    input.setAttribute("placeholder", "+7 (___) ___-__-__");
    input.setAttribute("maxlength", "18");
    input.setAttribute("inputmode", "tel");
    input.setAttribute("pattern", "\\+7 \\(\\d{3}\\) \\d{3}-\\d{2}-\\d{2}");

    input.addEventListener("focus", () => {
      if (!input.value.trim()) {
        input.value = "+7 ";
      }
    });

    input.addEventListener("input", () => {
      input.value = formatPhone(input.value);

      const complete = /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(input.value);
      input.setCustomValidity(
        complete ? "" : "Введите номер полностью: +7 (___) ___-__-__"
      );
    });

    input.addEventListener("blur", () => {
      if (input.value.trim() === "+7") {
        input.value = "";
      }
    });
  });
}

function initFormSecurityFields() {
  const startedAtFields = document.querySelectorAll(".js-form-started-at");

  if (!startedAtFields.length) return;

  const startedAt = String(Math.floor(Date.now() / 1000));

  startedAtFields.forEach((field) => {
    field.value = startedAt;
  });
}

function initToastForms() {
  const forms = document.querySelectorAll(".js-form");
  const toast = document.getElementById("toast");

  if (!forms.length) return;

  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (form.dataset.djangoForm === "lead") {
        if (!form.checkValidity()) {
          event.preventDefault();
          form.reportValidity();
        }

        return;
      }

      event.preventDefault();

      const requiredFields = form.querySelectorAll("[required]");
      let valid = true;

      requiredFields.forEach((field) => {
        if (field.type === "checkbox") {
          if (!field.checked) valid = false;
        } else if (!field.value.trim()) {
          valid = false;
        }
      });

      if (!valid) {
        showToast("Заполните обязательные поля.");
        return;
      }
      form.reset();
      showToast("Спасибо! Заявка сохранена.");

      const modal = form.closest(".modal");
      if (modal) {
        setTimeout(() => {
          modal.hidden = true;
          document.body.classList.remove("modal-open");
        }, 500);
      }
    });
  });
  function showToast(message) {
    if (!toast) return;

    toast.textContent = message;
    toast.classList.add("is-visible");

    clearTimeout(toast._hideTimer);
    toast._hideTimer = setTimeout(() => {
      toast.classList.remove("is-visible");
    }, 2600);
  }
}
/* =========================================================
   5. КНОПКА "НАВЕРХ" (SCROLL TOP)
   ========================================================= */
   
/** Функция initScrollTop — управляет кнопкой, которая появляется при скролле вниз и плавно поднимает пользователя в начало страницы при нажатии.*/
function initScrollTop() {                  // Находим кнопку по ID "scrollTop"  
  const button = document.getElementById("scrollTop");
  if (!button) return;                    // Если кнопки нет на странице — выходим
                                          /** Функция toggleVisibility — показывает или скрывает кнопку в зависимости от того, как далеко прокручена страница. */
  const toggleVisibility = () => {    
    if (window.scrollY > 500) {           // Если прокрутили больше чем на 500px — показываем кнопку
      button.classList.add("is-visible");
    } else {                           // Иначе — скрываем
      button.classList.remove("is-visible");
    }
  };
  
  window.addEventListener("scroll", toggleVisibility, { passive: true });   // Отслеживаем событие прокрутки страницы
   toggleVisibility();                  // Вызываем один раз при загрузке, чтобы проверить начальное состояние

   button.addEventListener("click", (event) => {  // Обработчик клика по кнопке "Наверх"
    event.preventDefault();             // Отменяем стандартное поведение браузера
    event.stopPropagation();            // Останавливаем всплытие события
    
    window.scrollTo({                   // Плавно прокручиваем страницу в самое начало
      top: 0,
      behavior: "smooth"
    });
    
    setTimeout(() => {                  // Дополнительная страховка: если плавная прокрутка не сработала,                                       
      if (window.scrollY > 0) {           // через 80 миллисекунд принудительно ставим scrollTop = 0
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
      }
    }, 80);
  });
}


/* =========================================================
   6. ГАЛЕРЕИ ТОВАРОВ (ЛИСТАНИЕ ФОТО)
   ========================================================= */

/** Функция initProductGalleries — создаёт галереи для каждого товара: - листание фото (влево/вправо) - пагинация (точки внизу) - клик по фото для открытия полноэкранного режима (лайтбокс) */
function initProductGalleries() {
    const galleries = document.querySelectorAll("[data-gallery]");    // Находим все элементы, у которых есть атрибут data-gallery

    galleries.forEach((gallery) => {    // Для каждой найденной галереи настраиваем логику
    const track = gallery.querySelector(".product-track");       // Контейнер с фото (движущаяся лента)
    const slides = Array.from(gallery.querySelectorAll(".product-slide")); // Все отдельные фото
    const prevBtn = gallery.querySelector("[data-gallery-prev]"); // Кнопка "назад"
    const nextBtn = gallery.querySelector("[data-gallery-next]"); // Кнопка "вперёд"
    const dotsWrap = gallery.querySelector("[data-gallery-dots]"); // Контейнер для точек пагинации
                                                // Если нет контейнера с фото или самих фото — выходим
    if (!track || !slides.length) return;

    let currentIndex = 0;                    // Индекс текущего отображаемого фото (начинаем с 0)

      if (slides.length <= 1) {               // Если фото всего одно или меньше — скрываем кнопки навигации и точки
      if (prevBtn) prevBtn.hidden = true;
      if (nextBtn) nextBtn.hidden = true;
      if (dotsWrap) dotsWrap.hidden = true;
    }

      if (dotsWrap) {                        // Если есть контейнер для точек — создаём их по количеству фото
      dotsWrap.innerHTML = "";               // Очищаем на случай повторного вызова

      slides.forEach((_, index) => {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "dot";
        dot.setAttribute("aria-label", `Показать фото ${index + 1}`);
        
        dot.addEventListener("click", (event) => {// При клике на точку переключаемся на соответствующее фото
          event.preventDefault();
          event.stopPropagation();
          goToSlide(index);
        });

        dotsWrap.appendChild(dot);
      });
    }
    /** Функция updateGallery — обновляет положение ленты с фото и подсвечивает активную точку пагинации.  */
    const updateGallery = () => {      
      track.style.transform = `translateX(-${currentIndex * 100}%)`; // Сдвигаем трек на нужный процент (100% на каждое фото)

       if (dotsWrap) {                         // Обновляем активный класс у точек
        const dots = dotsWrap.querySelectorAll(".dot, button");
        dots.forEach((dot, index) => {
          dot.classList.toggle("is-active", index === currentIndex);
        });
      }
    };
    /** Функция goToSlide — переключает галерею на указанный индекс. Если индекс выходит за пределы, зацикливаем (первое ↔ последнее).  */
    const goToSlide = (index) => {
      if (slides.length <= 1) return;

      if (index < 0) {
        currentIndex = slides.length - 1; // Переход на последнее
      } else if (index >= slides.length) {
        currentIndex = 0; // Переход на первое
      } else {
        currentIndex = index;
      }

      updateGallery();
    };
    
    if (prevBtn) {     // Обработчик для кнопки "назад"
      prevBtn.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        goToSlide(currentIndex - 1);
      });
    }
    
    if (nextBtn) {     // Обработчик для кнопки "вперёд"
      nextBtn.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        goToSlide(currentIndex + 1);
      });
    }
    
    slides.forEach((slide, index) => {    // Для каждого фото внутри галереи настраиваем открытие лайтбокса при клике
      const img = slide.querySelector("img");
      if (!img) return;
      
      img.style.cursor = "zoom-in";    // Меняем курсор на "лупа" (zoom-in), чтобы показать, что фото можно увеличить

      img.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        
        currentIndex = index;         // Сначала переключаем галерею на это фото (делаем его текущим)
        updateGallery();
        
        const images = slides        // Собираем все фото галереи в массив для лайтбокса
          .map((item) => {
            const image = item.querySelector("img");
            if (!image) return null;

            return {
              src: image.getAttribute("src"),
              alt: image.getAttribute("alt") || "Фото товара"
            };
          })
          .filter(Boolean);          // Убираем пустые значения
        
        openImageLightbox(images, currentIndex);  // Открываем полноэкранный просмотр (лайтбокс) с текущим индексом
      });
    });
    
    updateGallery();                    // Инициализируем галерею (показываем первое фото)
  });
}
/* =========================================================
   4. FAQ
   ========================================================= */

function initFaq() {
  const faqButtons = document.querySelectorAll(".faq-question");
  if (!faqButtons.length) return;

  faqButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const item = button.closest(".faq-item");
      if (!item) return;

      const isOpen = item.classList.contains("is-open");

      item.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(!isOpen));
    });
  });
}


/* =========================================================
   7. LIGHTBOX ФОТО ТОВАРОВ
   ========================================================= */

let lightboxImages = [];
let lightboxIndex = 0;

function initImageLightbox() {
  if (document.querySelector(".image-lightbox")) return;

  const lightbox = document.createElement("div");
  lightbox.className = "image-lightbox";
  lightbox.innerHTML = `
    <button class="image-lightbox__close" type="button" aria-label="Закрыть фото">
      <i class="fa-solid fa-xmark"></i>
    </button>

    <button class="image-lightbox__nav image-lightbox__nav--prev" type="button" aria-label="Предыдущее фото">
      <i class="fa-solid fa-chevron-left"></i>
    </button>

    <img class="image-lightbox__img" src="" alt="">

    <button class="image-lightbox__nav image-lightbox__nav--next" type="button" aria-label="Следующее фото">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
  `;

  document.body.appendChild(lightbox);

  const closeBtn = lightbox.querySelector(".image-lightbox__close");
  const prevBtn = lightbox.querySelector(".image-lightbox__nav--prev");
  const nextBtn = lightbox.querySelector(".image-lightbox__nav--next");

  if (closeBtn) {
    closeBtn.addEventListener("click", closeImageLightbox);
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      moveLightbox(-1);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      moveLightbox(1);
    });
  }

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      closeImageLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!lightbox.classList.contains("is-open")) return;

    if (event.key === "Escape") {
      closeImageLightbox();
    }

    if (event.key === "ArrowLeft") {
      moveLightbox(-1);
    }

    if (event.key === "ArrowRight") {
      moveLightbox(1);
    }
  });
}

function openImageLightbox(images, startIndex = 0) {
  const lightbox = document.querySelector(".image-lightbox");
  const img = lightbox ? lightbox.querySelector(".image-lightbox__img") : null;
  const prevBtn = lightbox ? lightbox.querySelector(".image-lightbox__nav--prev") : null;
  const nextBtn = lightbox ? lightbox.querySelector(".image-lightbox__nav--next") : null;

  if (!lightbox || !img || !images || !images.length) return;

  lightboxImages = images;
  lightboxIndex = Math.max(0, Math.min(startIndex, lightboxImages.length - 1));

  updateLightboxImage();

  if (prevBtn) prevBtn.hidden = lightboxImages.length <= 1;
  if (nextBtn) nextBtn.hidden = lightboxImages.length <= 1;

  lightbox.classList.add("is-open");
  document.body.classList.add("modal-open");
}

function updateLightboxImage() {
  const lightbox = document.querySelector(".image-lightbox");
  const img = lightbox ? lightbox.querySelector(".image-lightbox__img") : null;

  if (!img || !lightboxImages.length) return;

  img.src = lightboxImages[lightboxIndex].src;
  img.alt = lightboxImages[lightboxIndex].alt || "Фото товара";
}

function closeImageLightbox() {
  const lightbox = document.querySelector(".image-lightbox");
  const img = lightbox ? lightbox.querySelector(".image-lightbox__img") : null;

  if (!lightbox) return;

  lightbox.classList.remove("is-open");
  document.body.classList.remove("modal-open");

  if (img) {
    img.src = "";
    img.alt = "";
  }

  lightboxImages = [];
  lightboxIndex = 0;
}

function moveLightbox(direction) {
  if (!lightboxImages.length) return;

  lightboxIndex += direction;

  if (lightboxIndex < 0) {
    lightboxIndex = lightboxImages.length - 1;
  }

  if (lightboxIndex >= lightboxImages.length) {
    lightboxIndex = 0;
  }

  updateLightboxImage();
}


/* =========================================================
   8. КНОПКИ ЗАЯВОК В КАТАЛОГЕ
   ========================================================= */

function initRequestButtons() {
  const buttons = document.querySelectorAll(".js-request-btn");
  if (!buttons.length) return;

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const modal = document.getElementById("callbackModal");
      const requestType = document.getElementById("modalRequestType");
      const requestMessage = document.getElementById("modalRequestMessage");
      const titleEl = document.getElementById("callbackModalTitle");
      const sourcePage = document.getElementById("modalSourcePage");

      if (!modal) return;

      const type = button.dataset.requestType || "product";
      const message = button.dataset.requestMessage || "";
      const title = button.dataset.modalTitle || "Оставить заявку по позиции";

      if (requestType) requestType.value = type;
      if (requestMessage) requestMessage.value = message;
      if (titleEl) titleEl.textContent = title;

      if (sourcePage) {
        sourcePage.value =
          document.body.dataset.page ||
          window.location.pathname ||
          "Каталог";
      }

      modal.hidden = false;
      document.body.classList.add("modal-open");

      const firstField = modal.querySelector(
        "input:not([type=hidden]), textarea, select"
      );

      if (firstField) {
        setTimeout(() => firstField.focus(), 50);
      }
    });
  });
}


/* =========================================================
   9. КАТАЛОГ: ФИЛЬТРЫ
   ========================================================= */

function initCatalogFiltering() {
  const filterButtons = document.querySelectorAll("[data-filter]");
  if (!filterButtons.length) return;

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      filterButtons.forEach((btn) => btn.classList.remove("is-active"));
      button.classList.add("is-active");
      applyCatalogState();
    });
  });
}


/* =========================================================
   10. КАТАЛОГ: СОРТИРОВКА
   ========================================================= */

function initCatalogSorting() {
  const sortSelect = document.querySelector("[data-catalog-sort]");
  if (!sortSelect) return;

  sortSelect.addEventListener("change", applyCatalogState);
}


/* =========================================================
   11. КАТАЛОГ: ПОИСК
   ========================================================= */

function initCatalogSearch() {
  const searchInput = document.querySelector("[data-catalog-search]");
  if (!searchInput) return;

  searchInput.addEventListener("input", applyCatalogState);
}


/* =========================================================
   12. КАТАЛОГ: СОСТОЯНИЕ
   ========================================================= */

function initCatalogState() {
  applyCatalogState();
}

function syncCatalogState() {
  const grid = document.querySelector("[data-catalog-grid]");
  const countEl = document.querySelector("[data-catalog-count]");
  const emptyState = document.querySelector("[data-catalog-empty]");

  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".product-card"));
  const visibleCards = cards.filter((card) => !card.hidden);

  if (countEl) countEl.textContent = String(visibleCards.length);
  if (emptyState) emptyState.hidden = visibleCards.length !== 0;
}

function applyCatalogState() {
  const grid = document.querySelector("[data-catalog-grid]");
  if (!grid) return;

  const searchInput = document.querySelector("[data-catalog-search]");
  const activeFilterButton = document.querySelector("[data-filter].is-active");
  const sortSelect = document.querySelector("[data-catalog-sort]");

  const filter = activeFilterButton ? activeFilterButton.dataset.filter : "all";
  const query = searchInput ? searchInput.value.trim().toLowerCase() : "";
  const sortValue = sortSelect ? sortSelect.value : "default";

  const cards = Array.from(grid.querySelectorAll(".product-card"));

  cards.forEach((card) => {
    const title = (card.dataset.title || "").toLowerCase();
    const article = (card.dataset.article || "").toLowerCase();
    const category = (card.dataset.category || "").toLowerCase();
    const text = (card.textContent || "").toLowerCase();

    const matchesFilter = filter === "all" || category === filter;

    const matchesQuery =
      !query ||
      title.includes(query) ||
      article.includes(query) ||
      category.includes(query) ||
      text.includes(query);

    card.hidden = !(matchesFilter && matchesQuery);
  });

  const visibleCards = cards.filter((card) => !card.hidden);
  const hiddenCards = cards.filter((card) => card.hidden);

  if (sortValue === "title-asc") {
    visibleCards.sort((a, b) =>
      (a.dataset.title || "").localeCompare(b.dataset.title || "", "ru")
    );
  }

  if (sortValue === "title-desc") {
    visibleCards.sort((a, b) =>
      (b.dataset.title || "").localeCompare(a.dataset.title || "", "ru")
    );
  }

  [...visibleCards, ...hiddenCards].forEach((card) => {
    grid.appendChild(card);
  });

  syncCatalogState();
}


/* =========================================================
   14. ПОИСК ПО САЙТУ
   ========================================================= */
function initSiteSearch() {
  const siteSearches = document.querySelectorAll(".header-search input");

  if (!siteSearches.length) return;

  const staticPages = [
    { title: "Каталог", subtitle: "Раздел сайта", url: "/catalog/" },
    { title: "О компании", subtitle: "Раздел сайта", url: "/about/" },
    { title: "Доставка", subtitle: "Раздел сайта", url: "/delivery/" },
    { title: "Контакты", subtitle: "Раздел сайта", url: "/contacts/" },
    { title: "Полезные материалы", subtitle: "Раздел сайта", url: "/articles/" },
    { title: "Политика конфиденциальности", subtitle: "Документ", url: "/politika/" }
  ];

  let productResults = [];

  // Загружаем товары через API
  fetch("/api/products/")
    .then(response => response.json())
    .then(data => {
      productResults = (data.products || []).map(product => ({
        title: product.title,
        subtitle: product.article ? `Товар · ${product.article}` : "Товар",
        url: product.url
      }));
      console.log("✅ Товары загружены:", productResults.length);
    })
    .catch(err => {
      console.error("Ошибка загрузки товаров:", err);
      productResults = [];
    });

  const buildResults = (query) => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) return [];

    const matches = [];

    // Поиск по статическим страницам
    staticPages.forEach(item => {
      if (item.title.toLowerCase().includes(normalized)) {
        matches.push(item);
      }
    });

    // Поиск по товарам
    productResults.forEach(item => {
      if (item.title.toLowerCase().includes(normalized)) {
        matches.push(item);
      }
    });

    // Убираем дубликаты по URL
    const unique = [];
    const urls = new Set();
    for (const item of matches) {
      if (!urls.has(item.url)) {
        urls.add(item.url);
        unique.push(item);
      }
    }

    return unique.slice(0, 8);
  };

  siteSearches.forEach((input) => {
    const form = input.closest(".header-search");
    if (!form) return;

    let dropdown = form.querySelector(".site-search-results");
    if (!dropdown) {
      dropdown = document.createElement("div");
      dropdown.className = "site-search-results";
      dropdown.hidden = true;
      form.appendChild(dropdown);
    }

    const closeDropdown = () => {
      dropdown.hidden = true;
      dropdown.innerHTML = "";
    };

    const openResults = (items) => {
      if (!items.length) {
        dropdown.innerHTML = '<div class="site-search-results__empty">Ничего не найдено. Попробуйте изменить запрос.</div>';
        dropdown.hidden = false;
        return;
      }

      dropdown.innerHTML = items
        .map((item, index) => `
          <a class="site-search-results__item" href="${item.url}" data-search-result="${index}">
            <span class="site-search-results__title">${escapeHtml(item.title)}</span>
            <span class="site-search-results__meta">${escapeHtml(item.subtitle || "Раздел сайта")}</span>
          </a>
        `)
        .join("");
      dropdown.hidden = false;
    };

    input.addEventListener("input", () => {
      const query = input.value.trim();
      if (!query) {
        closeDropdown();
        return;
      }
      openResults(buildResults(query));
    });

    input.addEventListener("keydown", (event) => {
      const items = dropdown.querySelectorAll("a.site-search-results__item");
      if (event.key === "Enter") {
        event.preventDefault();
        if (items[0]) {
          window.location.href = items[0].getAttribute("href");
        }
      }
      if (event.key === "Escape") closeDropdown();
    });

    document.addEventListener("click", (event) => {
      if (!form.contains(event.target)) closeDropdown();
    });
  });
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}