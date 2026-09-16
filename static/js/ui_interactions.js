/**
 * LAUNDRYCARE UI INTERACTIONS & MOTION ENGINE
 * Lightweight, vanilla JavaScript for micro-interactions, counters, and toasts.
 */

(function () {
    'use strict';

    // Respect user's reduced-motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /**
     * 1. Animated Number Counter Tally
     */
    function initCounters() {
        if (prefersReducedMotion) return;

        const counterElements = document.querySelectorAll('[data-counter]');
        counterElements.forEach(el => {
            const rawTarget = el.getAttribute('data-counter');
            const prefix = el.getAttribute('data-counter-prefix') || '';
            const suffix = el.getAttribute('data-counter-suffix') || '';
            const target = parseFloat(rawTarget.replace(/[^0-9.-]+/g, ''));
            if (isNaN(target)) return;

            const duration = 1200; // ms
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease out quart
                const easeProgress = 1 - Math.pow(1 - progress, 4);
                const currentVal = Math.floor(easeProgress * target);

                el.textContent = prefix + currentVal.toLocaleString() + suffix;

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    el.textContent = prefix + target.toLocaleString() + suffix;
                }
            }

            requestAnimationFrame(updateCounter);
        });
    }

    /**
     * 2. Table Row Stagger Animations
     */
    function initStaggeredTables() {
        if (prefersReducedMotion) return;

        const tables = document.querySelectorAll('table.anim-stagger-rows tbody');
        tables.forEach(tbody => {
            const rows = tbody.querySelectorAll('tr');
            rows.forEach((row, index) => {
                if (index < 15) { // Cap at first 15 rows for performance
                    row.classList.add('anim-fade-up');
                    row.style.animationDelay = (index * 0.045) + 's';
                }
            });
        });
    }

    /**
     * 3. Toast Notification API
     */
    window.showToast = function (title, message, type = 'info', duration = 3800) {
        let container = document.getElementById('laundrycare-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'laundrycare-toast-container';
            container.style.cssText = 'position:fixed; top:20px; right:20px; z-index:99999; display:flex; flex-direction:column; gap:10px; pointer-events:none;';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `laundrycare-toast toast-${type}`;

        const iconMap = {
            success: '<span style="color:#10b981; font-weight:bold; font-size:16px;">✓</span>',
            info: '<span style="color:#2563eb; font-weight:bold; font-size:16px;">ℹ</span>',
            warning: '<span style="color:#f59e0b; font-weight:bold; font-size:16px;">⚠</span>',
            danger: '<span style="color:#ef4444; font-weight:bold; font-size:16px;">✕</span>'
        };

        toast.innerHTML = `
            <div style="flex-shrink:0;">${iconMap[type] || iconMap.info}</div>
            <div style="flex-grow:1;">
                <div style="font-weight:700; font-size:13px; color:#0f172a; line-height:1.2;">${title}</div>
                ${message ? `<div style="font-size:11px; color:#64748b; margin-top:3px; line-height:1.3;">${message}</div>` : ''}
            </div>
            <button onclick="this.parentElement.remove()" style="background:none; border:none; color:#94a3b8; font-size:14px; cursor:pointer; padding:0 4px; line-height:1;">&times;</button>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('toast-out');
            setTimeout(() => toast.remove(), 250);
        }, duration);
    };

    /**
     * 4. Interactive Button Active Press Feedback
     */
    function initButtonFeedback() {
        document.querySelectorAll('.btn-interactive, .btn-primary, .btn-secondary, button[type="submit"]').forEach(btn => {
            btn.classList.add('btn-interactive');
        });
    }

    // Auto-init on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initCounters();
            initStaggeredTables();
            initButtonFeedback();
        });
    } else {
        initCounters();
        initStaggeredTables();
        initButtonFeedback();
    }
})();
