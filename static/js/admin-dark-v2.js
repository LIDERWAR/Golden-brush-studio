/* ==============================================================================
   GB STUDIO — Force Dark Architecture Theme & Admin Helpers (v2)
   ============================================================================== */
(function() {
    try {
        localStorage.setItem('jazzmin-theme-mode', 'dark');
        document.documentElement.setAttribute('data-bs-theme', 'dark');
    } catch (e) {
        // Storage access may be restricted in private browsing
    }
})();

document.addEventListener('DOMContentLoaded', function() {
    const priceInput = document.getElementById('id_price');
    if (!priceInput) return;

    // Helper functions for Russian Ruble formatting
    function formatPriceVal(val) {
        if (!val) return 'По запросу';
        val = val.trim();
        if (!val || /запрос/i.test(val)) return 'По запросу';
        const digits = val.replace(/\D/g, '');
        if (digits) {
            const hasOtherChars = val.replace(/[\d\s₽.,руб\.rubRUB]/gi, '').trim();
            if (!hasOtherChars) {
                const num = parseInt(digits, 10);
                return num.toLocaleString('ru-RU') + ' ₽';
            }
        }
        return val;
    }

    // Container for quick action buttons under price field
    const helperContainer = document.createElement('div');
    helperContainer.className = 'price-helper-bar';
    helperContainer.style.cssText = 'display: flex; align-items: center; gap: 8px; margin-top: 8px; flex-wrap: wrap;';

    const rubleBtn = document.createElement('button');
    rubleBtn.type = 'button';
    rubleBtn.innerText = '+ ₽ (Добавить знак рубля)';
    rubleBtn.style.cssText = 'background: rgba(197, 160, 89, 0.15); border: 1px solid #c5a059; color: #dfb279; font-size: 0.8rem; padding: 4px 10px; border-radius: 4px; font-weight: 500; cursor: pointer; transition: all 0.2s;';
    rubleBtn.onmouseover = function() { this.style.background = '#c5a059'; this.style.color = '#000'; };
    rubleBtn.onmouseout = function() { this.style.background = 'rgba(197, 160, 89, 0.15)'; this.style.color = '#dfb279'; };

    const requestBtn = document.createElement('button');
    requestBtn.type = 'button';
    requestBtn.innerText = 'По запросу';
    requestBtn.style.cssText = 'background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15); color: #cbd5e1; font-size: 0.8rem; padding: 4px 10px; border-radius: 4px; font-weight: 500; cursor: pointer; transition: all 0.2s;';
    requestBtn.onmouseover = function() { this.style.background = 'rgba(255, 255, 255, 0.12)'; this.style.color = '#fff'; };
    requestBtn.onmouseout = function() { this.style.background = 'rgba(255, 255, 255, 0.05)'; this.style.color = '#cbd5e1'; };

    const hintSpan = document.createElement('span');
    hintSpan.style.cssText = 'font-size: 0.78rem; color: #8c939d; margin-left: 6px;';
    hintSpan.innerHTML = 'Подсказка: на клавиатуре Windows знак рубля вводится через <strong>Правый Alt + 8</strong>';

    rubleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (priceInput.value) {
            priceInput.value = formatPriceVal(priceInput.value);
            if (!priceInput.value.includes('₽') && !/запрос/i.test(priceInput.value)) {
                priceInput.value = priceInput.value.trim() + ' ₽';
            }
        } else {
            priceInput.value = '₽';
        }
        priceInput.focus();
    });

    requestBtn.addEventListener('click', function(e) {
        e.preventDefault();
        priceInput.value = 'По запросу';
        priceInput.focus();
    });

    // Auto-format on input blur (if digits entered without ruble sign)
    priceInput.addEventListener('blur', function() {
        if (priceInput.value) {
            priceInput.value = formatPriceVal(priceInput.value);
        }
    });

    helperContainer.appendChild(rubleBtn);
    helperContainer.appendChild(requestBtn);
    helperContainer.appendChild(hintSpan);

    priceInput.parentNode.appendChild(helperContainer);
});
