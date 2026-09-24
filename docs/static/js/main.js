/**
 * POPYKIN ATELIER & FIT-OUT PRODUCTION — INTERACTIVE JAVASCRIPT
 * Multi-Step B2B Quiz Funnel, Sample Box Order, Modals, Lightbox
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Header scroll effect
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Mobile Menu Toggle
    const burgerBtn = document.getElementById('burgerBtn') || document.querySelector('.burger-btn');
    const mobileDrawer = document.getElementById('mobileDrawer') || document.querySelector('.mobile-drawer');
    const drawerBackdrop = document.getElementById('drawerBackdrop');
    const drawerClose = document.getElementById('drawerClose');

    function openMobileDrawer() {
        if (mobileDrawer) {
            mobileDrawer.classList.add('active');
            document.body.classList.add('drawer-open');
        }
    }

    function closeMobileDrawer() {
        if (mobileDrawer) {
            mobileDrawer.classList.remove('active');
            document.body.classList.remove('drawer-open');
        }
    }

    if (burgerBtn) {
        burgerBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (mobileDrawer && mobileDrawer.classList.contains('active')) {
                closeMobileDrawer();
            } else {
                openMobileDrawer();
            }
        });
    }

    if (drawerClose) {
        drawerClose.addEventListener('click', (e) => {
            e.preventDefault();
            closeMobileDrawer();
        });
    }

    if (drawerBackdrop) {
        drawerBackdrop.addEventListener('click', () => {
            closeMobileDrawer();
        });
    }

    // Auto-close on link click
    if (mobileDrawer) {
        const drawerLinks = mobileDrawer.querySelectorAll('.drawer-link, .drawer-cta');
        drawerLinks.forEach(link => {
            link.addEventListener('click', () => {
                closeMobileDrawer();
            });
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileDrawer && mobileDrawer.classList.contains('active')) {
            closeMobileDrawer();
        }
    });

    // 3. B2B Multi-Step Quiz (Natalia's Lead Machine)
    initQuiz();

    // 4. Sample Box Modal
    initSampleBoxModal();

    // 5. Lightbox for Artworks & Projects
    initLightbox();

    // 6. Architectural Hero Showcase Slider
    initHeroSlider();
});

// Toast notification helper
function showToast(message, isSuccess = true) {
    let toast = document.getElementById('toastNotification');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toastNotification';
        toast.className = 'toast-msg';
        document.body.appendChild(toast);
    }
    toast.innerHTML = `
        <span style="color: ${isSuccess ? 'var(--accent-gold)' : '#ff4d4f'}; font-size: 1.2rem;">
            ${isSuccess ? '✓' : '⚠'}
        </span>
        <span>${message}</span>
    `;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4500);
}

// B2B Quiz Logic
function initQuiz() {
    const quizEl = document.getElementById('b2bQuiz');
    if (!quizEl) return;

    let currentStep = 1;
    const totalSteps = 4;

    const quizData = {
        object_type: 'Предприятие / Завод (АБК, цеха)',
        area_range: '1500–5000 м²',
        service_needed: 'Комплексный fit-out под ключ',
        timeline: 'В течение 1-3 месяцев',
        estimated_cost: 'от 18 000 000 ₽',
        name: '',
        company: '',
        phone: '',
        email: '',
        message: ''
    };

    const stepElements = quizEl.querySelectorAll('.quiz-step');
    const progressFill = quizEl.querySelector('.quiz-progress-fill');
    const stepCounter = quizEl.querySelector('.quiz-step-counter');

    // Update Step UI
    function updateStep() {
        stepElements.forEach((el, idx) => {
            el.style.display = (idx + 1 === currentStep) ? 'block' : 'none';
        });

        if (progressFill) {
            const percent = (currentStep / totalSteps) * 100;
            progressFill.style.width = `${percent}%`;
        }

        if (stepCounter) {
            stepCounter.textContent = `Шаг ${currentStep} из ${totalSteps}`;
        }

        // Update estimated preview on step 4
        if (currentStep === 4) {
            calculateEstimate();
        }
    }

    // Option selection
    quizEl.querySelectorAll('.quiz-option').forEach(opt => {
        opt.addEventListener('click', () => {
            const parent = opt.closest('.quiz-options-grid');
            parent.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
            opt.classList.add('selected');

            const key = opt.dataset.key;
            const val = opt.dataset.value;
            if (key && val) {
                quizData[key] = val;
            }
        });
    });

    // Next button
    quizEl.querySelectorAll('.btn-quiz-next').forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep < totalSteps) {
                currentStep++;
                updateStep();
            }
        });
    });

    // Prev button
    quizEl.querySelectorAll('.btn-quiz-prev').forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateStep();
            }
        });
    });

    // Estimate calculation formula
    function calculateEstimate() {
        let baseRate = 12000; // base rub/sqm for commercial
        if (quizData.object_type.includes('Отель')) baseRate = 18000;
        if (quizData.object_type.includes('Офис')) baseRate = 15000;
        if (quizData.object_type.includes('Резиденция')) baseRate = 28000;

        let sqm = 1000;
        if (quizData.area_range.includes('500 м²')) sqm = 400;
        if (quizData.area_range.includes('500–1500')) sqm = 1000;
        if (quizData.area_range.includes('1500–5000')) sqm = 3000;
        if (quizData.area_range.includes('5000')) sqm = 7000;

        const est = (baseRate * sqm).toLocaleString('ru-RU');
        quizData.estimated_cost = `от ${est} ₽`;

        const estEl = quizEl.querySelector('.quiz-estimate-val');
        if (estEl) {
            estEl.textContent = quizData.estimated_cost;
        }
    }

    // Submit Quiz Form
    const quizForm = quizEl.querySelector('#quizContactForm');
    if (quizForm) {
        quizForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = quizForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Отправка расчета...';

            quizData.name = quizForm.querySelector('input[name="name"]').value;
            quizData.company = quizForm.querySelector('input[name="company"]').value;
            quizData.phone = quizForm.querySelector('input[name="phone"]').value;
            quizData.email = quizForm.querySelector('input[name="email"]').value;
            quizData.message = quizForm.querySelector('textarea[name="message"]').value;

            try {
                
        // GitHub Pages Demo Mode: Return simulated success if on static host
        if (window.location.hostname.includes('github.io') || window.location.protocol === 'file:') {
            await new Promise(r => setTimeout(r, 600));
            res = { success: true };
        } else {
        
            const response = await fetch('/api/quiz-lead/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(quizData)
                });

                const res = await response.json();
        }
                if (res.success) {
                    quizEl.querySelector('.quiz-body-wrap').innerHTML = `
                        <div style="text-align: center; padding: 3rem 1rem;">
                            <div style="width: 70px; height: 70px; border-radius: 50%; background: rgba(197, 155, 109, 0.15); border: 2px solid var(--accent-gold); display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; font-size: 2rem; color: var(--accent-gold);">✓</div>
                            <h3 style="font-size: 2.2rem; color: #fff; margin-bottom: 1rem;">Расчет объекта успешно сформирован!</h3>
                            <p style="font-size: 1.1rem; color: var(--text-muted); max-width: 580px; margin: 0 auto 2rem; line-height: 1.7;">
                                Предварительная смета: <strong style="color: var(--accent-gold);">${quizData.estimated_cost}</strong>.<br>
                                Руководитель B2B-направления <strong>Наталья</strong> уже получила параметры вашего объекта и свяжется с вами по номеру <strong>${quizData.phone}</strong> для согласования выезда главного инженера.
                            </p>
                            <a href="/" class="btn btn-secondary">Вернуться на главную</a>
                        </div>
                    `;
                    showToast('Заявка на расчет объекта принята! Наталья свяжется с вами.');
                } else {
                    showToast(res.error || 'Ошибка при отправке', false);
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Получить смету и ТКП';
                }
            } catch (err) {
                showToast('Ошибка соединения с сервером', false);
                submitBtn.disabled = false;
                submitBtn.textContent = 'Получить смету и ТКП';
            }
        });
    }

    updateStep();
}

// Sample Box Modal
function initSampleBoxModal() {
    const modal = document.getElementById('sampleBoxModal');
    const openBtns = document.querySelectorAll('.btn-open-samplebox');
    if (!modal) return;

    openBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            modal.classList.add('active');
        });
    });

    const closeBtn = modal.querySelector('.modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    const form = modal.querySelector('#sampleBoxForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.textContent = 'Оформление...';

            const payload = {
                name: form.querySelector('input[name="name"]').value,
                company: form.querySelector('input[name="company"]').value,
                phone: form.querySelector('input[name="phone"]').value,
                address: form.querySelector('input[name="address"]').value,
            };

            try {
                
        // GitHub Pages Demo Mode: Return simulated success if on static host
        if (window.location.hostname.includes('github.io') || window.location.protocol === 'file:') {
            await new Promise(r => setTimeout(r, 600));
            res = { success: true };
        } else {
        
            const response = await fetch('/api/sample-box/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(payload)
                });

                const res = await response.json();
        }
                if (res.success) {
                    modal.classList.remove('active');
                    showToast('Кейс с образцами успешно заказан! Мы отправим трек-номер в WhatsApp.');
                    form.reset();
                } else {
                    showToast(res.error || 'Ошибка отправки', false);
                }
            } catch (e) {
                showToast('Ошибка сети', false);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Заказать кейс образцов';
            }
        });
    }
}

// Lightbox for Artwork Details
function initLightbox() {
    const modal = document.getElementById('artworkModal');
    if (!modal) return;

    document.querySelectorAll('.btn-view-artwork').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const title = btn.dataset.title || '';
            const medium = btn.dataset.medium || '';
            const dimensions = btn.dataset.dimensions || '';
            const price = btn.dataset.price || '';
            const desc = btn.dataset.desc || '';
            const img = btn.dataset.img || '';

            modal.querySelector('.art-modal-title').textContent = title;
            modal.querySelector('.art-modal-medium').textContent = medium;
            modal.querySelector('.art-modal-dim').textContent = dimensions;
            modal.querySelector('.art-modal-price').textContent = price;
            modal.querySelector('.art-modal-desc').textContent = desc;
            modal.querySelector('.art-modal-img').src = img;

            const inputTitle = modal.querySelector('#artModalInputTitle');
            if (inputTitle) inputTitle.value = title;

            modal.classList.add('active');
        });
    });

    // Handle Art Inquiry Form
    const artForm = modal.querySelector('#artInquiryForm');
    if (artForm) {
        artForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = artForm.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.textContent = 'Отправка...';

            const payload = {
                name: artForm.querySelector('input[name="name"]').value,
                phone: artForm.querySelector('input[name="phone"]').value,
                service_needed: `Бронирование картины/керамики: ${modal.querySelector('#artModalInputTitle').value}`,
                source: 'art_inquiry',
                object_type: 'Частная коллекция'
            };

            try {
                
        // GitHub Pages Demo Mode: Return simulated success if on static host
        if (window.location.hostname.includes('github.io') || window.location.protocol === 'file:') {
            await new Promise(r => setTimeout(r, 600));
            res = { success: true };
        } else {
        
            const response = await fetch('/api/quiz-lead/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(payload)
                });
                const res = await response.json();
        }
                if (res.success) {
                    modal.classList.remove('active');
                    showToast('Запрос на бронирование отправлен! Мы свяжемся с вами в течение 15 минут.');
                    artForm.reset();
                } else {
                    showToast(res.error || 'Ошибка бронирования', false);
                }
            } catch (err) {
                showToast('Ошибка сети при отправке', false);
            } finally {
                btn.disabled = false;
                btn.textContent = 'Забронировать работу';
            }
        });
    }

    const closeBtn = modal.querySelector('.modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    }
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
    });
}

// CSRF Token Helper
function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

// 6. Architectural Hero Showcase Slider
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    if (!slides.length) return;

    const slideNumEl = document.getElementById('heroSlideNum');
    const slideCatEl = document.getElementById('heroSlideCat');
    const slideTitleEl = document.getElementById('heroSlideTitle');
    const slideMetaEl = document.getElementById('heroSlideMeta');
    const progressBar = document.getElementById('heroProgressBar');
    const prevBtn = document.getElementById('heroPrevBtn');
    const nextBtn = document.getElementById('heroNextBtn');
    const cardEl = document.querySelector('.hero-project-card');

    const slideData = [
        {
            num: '01',
            cat: 'Лаборатория фактур & Рельефы',
            title: 'Авторские минеральные поверхности и арт-декор',
            meta: 'Собственная лаборатория • Барельефы, микроцемент, латунь'
        },
        {
            num: '02',
            cat: 'Корпоративные Штаб-квартиры',
            title: 'Представительский офис «ПромХолдинг»',
            meta: '4 200 м² • Москва-Сити • Fit-out под ключ со сдачей СРО'
        },
        {
            num: '03',
            cat: 'Гостиничный сектор (HoReCa 5*)',
            title: 'Премиальный атриум и лаунж гранд-отеля',
            meta: 'Скульптурные криволинейные объемы лобби, акустические панели'
        },
        {
            num: '04',
            cat: 'Музейное искусство & Private Collection',
            title: 'Оригинальные полотна Александра Попыкина',
            meta: 'Фактурная живопись на холсте и керамика в представительские интерьеры'
        }
    ];

    let currentIndex = 0;
    const duration = 7000; // 7 seconds per slide
    let startTime = null;
    let animationFrame = null;
    let isPaused = false;

    function goToSlide(index) {
        slides[currentIndex].classList.remove('active');
        currentIndex = (index + slides.length) % slides.length;
        slides[currentIndex].classList.add('active');

        if (slideNumEl) slideNumEl.textContent = slideData[currentIndex].num;
        if (slideCatEl) slideCatEl.textContent = slideData[currentIndex].cat;
        if (slideTitleEl) slideTitleEl.textContent = slideData[currentIndex].title;
        if (slideMetaEl) slideMetaEl.textContent = slideData[currentIndex].meta;

        startTime = performance.now();
        if (progressBar) progressBar.style.width = '0%';
    }

    function tick(now) {
        if (!startTime) startTime = now;

        if (!isPaused) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            if (progressBar) {
                progressBar.style.width = (progress * 100) + '%';
            }
            if (progress >= 1) {
                goToSlide(currentIndex + 1);
            }
        } else {
            // Adjust start time so pause doesn't skip
            startTime += 16;
        }

        animationFrame = requestAnimationFrame(tick);
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
            e.preventDefault();
            goToSlide(currentIndex - 1);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
            e.preventDefault();
            goToSlide(currentIndex + 1);
        });
    }

    if (cardEl) {
        cardEl.addEventListener('mouseenter', () => { isPaused = true; });
        cardEl.addEventListener('mouseleave', () => { isPaused = false; });
    }

    // Start auto slider
    animationFrame = requestAnimationFrame(tick);
}

