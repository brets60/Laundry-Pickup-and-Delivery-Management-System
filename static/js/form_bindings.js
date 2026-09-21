/**
 * ============================================================================
 * LAUNDRYCARE - ASYNC FORM BINDING ENGINE (Week 7 / Phase 3)
 * Handles client-side async fetch, double-submit locking, spinner indicators,
 * field-level 422 inline errors, success toasts, and modal workflows.
 * ============================================================================
 */

(function () {
    'use strict';

    /**
     * Display a floating toast notification.
     * @param {string} message - Message to display
     * @param {'success'|'error'|'info'} type - Toast type
     * @param {number} duration - Milliseconds before auto-dismiss
     */
    function showToast(message, type = 'success', duration = 3500) {
        let container = document.querySelector('.lc-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'lc-toast-container';
            container.setAttribute('aria-live', 'polite');
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `lc-toast ${type}`;

        const iconSvg = type === 'success'
            ? `<svg class="lc-toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`
            : `<svg class="lc-toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;

        toast.innerHTML = `
            ${iconSvg}
            <span class="lc-toast-msg">${message}</span>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('closing');
            setTimeout(() => {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 300);
        }, duration);
    }

    // Expose showToast globally
    window.showToast = showToast;

    /**
     * Clear all error banners and inline field error badges from form.
     * @param {HTMLFormElement} form
     */
    function clearFormErrors(form) {
        // Remove field-level errors
        form.querySelectorAll('.field-error-text').forEach(el => el.remove());

        // Remove invalid border highlights
        form.querySelectorAll('.input-invalid').forEach(el => {
            el.classList.remove('input-invalid');
            el.removeAttribute('aria-invalid');
        });

        // Remove form-level error banners
        form.querySelectorAll('.form-error-banner').forEach(el => el.remove());
    }

    /**
     * Display structured field-level 422 errors under their respective inputs.
     * @param {HTMLFormElement} form
     * @param {Object|string} errors - Dictionary of { fieldName: errorMessage } or general string
     */
    function displayFieldErrors(form, errors) {
        clearFormErrors(form);

        if (typeof errors === 'string') {
            renderBannerError(form, errors);
            return;
        }

        let firstInvalidField = null;

        Object.keys(errors || {}).forEach(fieldName => {
            const message = errors[fieldName];
            const field = form.querySelector(`[name="${fieldName}"], #${fieldName}`);

            if (field) {
                field.classList.add('input-invalid');
                field.setAttribute('aria-invalid', 'true');

                const errDiv = document.createElement('div');
                errDiv.className = 'field-error-text';
                errDiv.id = `error-${fieldName}`;
                errDiv.setAttribute('role', 'alert');
                errDiv.innerHTML = `
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    <span>${message}</span>
                `;

                // If inside an input-group or wrapper, append after the wrapper
                const parent = field.closest('.input-wrapper, .input-group, .form-group') || field.parentElement;
                if (parent && parent !== form && !parent.classList.contains('form-grid')) {
                    parent.appendChild(errDiv);
                } else {
                    field.insertAdjacentElement('afterend', errDiv);
                }

                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            } else {
                // Fallback for fields not directly matched
                renderBannerError(form, `${fieldName}: ${message}`);
            }
        });

        if (firstInvalidField) {
            firstInvalidField.focus();
        }
    }

    /**
     * Render a top-level form error banner.
     * @param {HTMLFormElement} form
     * @param {string} message
     */
    function renderBannerError(form, message) {
        let banner = form.querySelector('.form-error-banner');
        if (!banner) {
            banner = document.createElement('div');
            banner.className = 'form-error-banner';
            banner.setAttribute('role', 'alert');
            form.prepend(banner);
        }
        banner.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <div>
                <strong>Submission Failed:</strong> ${message}
            </div>
        `;
    }

    /**
     * Closes an active modal if the form is inside one.
     * Supports standard Bootstrap modal, dialogs, or custom modals.
     * @param {HTMLFormElement} form
     */
    function closeModalIfPresent(form) {
        // 1. Bootstrap 5 Modal
        const bsModalEl = form.closest('.modal');
        if (bsModalEl && window.bootstrap && window.bootstrap.Modal) {
            const instance = window.bootstrap.Modal.getInstance(bsModalEl);
            if (instance) {
                instance.hide();
                return;
            }
        }

        // 2. Custom backdrop or overlay modal
        const modalContainer = form.closest('.modal-overlay, .modal-backdrop, .modal, [data-modal]');
        if (modalContainer) {
            modalContainer.style.display = 'none';
            modalContainer.classList.remove('active', 'show', 'is-open');
            document.body.classList.remove('modal-open');
        }
    }

    /**
     * Bind a form to asynchronous backend submission.
     * @param {HTMLFormElement} form
     */
    function bindAsyncForm(form) {
        if (form.dataset.boundAsync === 'true') return;
        form.dataset.boundAsync = 'true';

        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            const originalBtnHTML = submitBtn ? submitBtn.innerHTML : '';

            // Step 1: Clear previous errors
            clearFormErrors(form);

            // Step 2: Double-Submit Prevention & Loading State
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.setAttribute('aria-busy', 'true');
                submitBtn.classList.add('btn-loading');
                submitBtn.innerHTML = `<span class="btn-spinner"></span> Saving...`;
            }

            // Step 3: Extract form data as JSON
            const formData = new FormData(form);
            const payload = {};
            formData.forEach((value, key) => {
                // If key already exists in payload (e.g. multi-select), turn into array
                if (key in payload) {
                    if (!Array.isArray(payload[key])) {
                        payload[key] = [payload[key]];
                    }
                    payload[key].push(value);
                } else {
                    payload[key] = value;
                }
            });

            const action = form.getAttribute('action') || window.location.pathname;
            const method = (form.getAttribute('method') || 'POST').toUpperCase();

            try {
                const response = await fetch(action, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify(payload)
                });

                const responseData = await response.json().catch(() => null);

                // Step 4: Handle 200/201 Success
                if (response.status === 200 || response.status === 201) {
                    const successMsg = responseData?.message || 'Record saved successfully!';
                    showToast(successMsg, 'success');

                    // Reset form fields
                    form.reset();

                    // Close modal if present
                    closeModalIfPresent(form);

                    // Dispatch event for page-specific DOM updates
                    form.dispatchEvent(new CustomEvent('form:success', {
                        bubbles: true,
                        detail: responseData
                    }));

                    // Refresh table or page smoothly after short interval
                    setTimeout(() => {
                        window.location.reload();
                    }, 900);
                }
                // Step 5: Handle 422 Validation Errors
                else if (response.status === 422) {
                    const errorObj = responseData?.error || responseData?.message || 'Invalid form input.';
                    displayFieldErrors(form, errorObj);
                    showToast('Please fix the highlighted errors.', 'error');
                }
                // Step 6: Handle 401/403/500 Errors
                else {
                    const errMsg = responseData?.error || responseData?.message || `Server responded with status ${response.status}.`;
                    renderBannerError(form, errMsg);
                    showToast('Submission failed. Please check form data.', 'error');
                }
            } catch (err) {
                // Network failure or unhandled exception
                console.error('Async form binding error:', err);
                renderBannerError(form, 'A network error occurred. Please check your connection and try again.');
                showToast('Network error occurred.', 'error');
            } finally {
                // Step 7: Restore Submit Button
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.removeAttribute('aria-busy');
                    submitBtn.classList.remove('btn-loading');
                    submitBtn.innerHTML = originalBtnHTML;
                }
            }
        });
    }

    /**
     * Auto-bind all matching forms on page load
     */
    function initAsyncForms() {
        const selector = 'form[data-async-form], form.async-form';
        document.querySelectorAll(selector).forEach(bindAsyncForm);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAsyncForms);
    } else {
        initAsyncForms();
    }

    // Expose binding helper
    window.bindAsyncForm = bindAsyncForm;
    window.initAsyncForms = initAsyncForms;
})();
