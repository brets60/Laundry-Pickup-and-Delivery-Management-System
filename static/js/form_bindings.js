/**
 * ============================================================================
 * LAUNDRYCARE - ASYNC FORM BINDING ENGINE (Weeks 6-8 / Deliverable 3)
 * Handles client-side async fetch, double-submit locking, spinner indicators,
 * field-level 422 inline errors (both Phase 2 & Phase 3 envelopes),
 * humanized 404/500/network feedback, success toasts, and modal workflows.
 * ============================================================================
 */

(function () {
    'use strict';

    /**
     * Display a floating toast notification.
     * @param {string} message - Message to display
     * @param {'success'|'error'|'info'|'warning'} type - Toast type
     * @param {number} duration - Milliseconds before auto-dismiss
     */
    function showToast(message, type = 'success', duration = 3500) {
        if (arguments.length >= 3 && typeof type === 'string' && (arguments[2] === 'success' || arguments[2] === 'error' || arguments[2] === 'info')) {
            const title = message;
            message = `<strong>${title}</strong>: ${type}`;
            type = arguments[2];
            duration = arguments[3] || 4000;
        }
        if (typeof duration !== 'number' || isNaN(duration)) {
            duration = 4000;
        }

        let container = document.querySelector('.lc-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'lc-toast-container';
            container.setAttribute('aria-live', 'polite');
            document.body.appendChild(container);
        }

        const validTypes = ['success', 'error', 'info', 'warning'];
        const cleanType = validTypes.includes(type) ? type : 'success';
        const toast = document.createElement('div');
        toast.className = `lc-toast ${cleanType}`;

        const iconSvg = cleanType === 'success'
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
     * Normalize error payload from either Phase 2 standardized envelope
     * ({ error: { code, message, fields: {...} } }) or Phase 3 dictionary ({ error: {...} }).
     */
    function extractErrorMessage(responseData, fallbackMessage) {
        if (!responseData) return fallbackMessage;
        const err = responseData.error;
        if (typeof err === 'string' && err.trim()) return err;
        if (err && typeof err === 'object' && typeof err.message === 'string' && err.message.trim()) {
            return err.message;
        }
        if (typeof responseData.message === 'string' && responseData.message.trim()) {
            return responseData.message;
        }
        return fallbackMessage;
    }

    /**
     * Clear all error banners and inline field error badges from form.
     * @param {HTMLFormElement} form
     */
    function clearFormErrors(form) {
        form.querySelectorAll('.field-error-text').forEach(el => el.remove());

        form.querySelectorAll('.input-invalid').forEach(el => {
            el.classList.remove('input-invalid');
            el.removeAttribute('aria-invalid');
        });

        form.querySelectorAll('.form-error-banner').forEach(el => el.remove());
    }

    /**
     * Display structured field-level 422 errors under their respective inputs.
     * Supports both { field: msg } and { code: 'VALIDATION_ERROR', fields: { field: msg } }.
     * @param {HTMLFormElement} form
     * @param {Object|string} errors
     */
    function displayFieldErrors(form, errors) {
        clearFormErrors(form);

        if (typeof errors === 'string') {
            renderBannerError(form, errors);
            return;
        }

        // Unwrap Phase 2 standardized envelope if present
        const fieldsMap = (errors && typeof errors === 'object' && errors.fields && typeof errors.fields === 'object')
            ? errors.fields
            : (errors || {});

        let firstInvalidField = null;

        Object.keys(fieldsMap).forEach(fieldName => {
            const message = fieldsMap[fieldName];
            if (typeof message !== 'string') return;

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
                renderBannerError(form, message);
            }
        });

        if (firstInvalidField) {
            firstInvalidField.focus();
        }
    }

    /**
     * Render a top-level form error banner with humanized copy (no raw status codes).
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
                <strong>Unable to complete action:</strong> ${message}
            </div>
        `;
    }

    /**
     * Closes an active modal if the form is inside one.
     * @param {HTMLFormElement} form
     */
    function closeModalIfPresent(form) {
        const bsModalEl = form.closest('.modal');
        if (bsModalEl && window.bootstrap && window.bootstrap.Modal) {
            const instance = window.bootstrap.Modal.getInstance(bsModalEl);
            if (instance) {
                instance.hide();
                return;
            }
        }

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
                    const successMsg = responseData?.message || 'Your changes have been saved.';
                    showToast(successMsg, 'success');

                    // Only reset form if it is a create modal form (preserve values on edit screens)
                    const isEditForm = (form.dataset.asyncForm || '').includes('edit') || action.includes('/edit/');
                    if (!isEditForm) {
                        form.reset();
                    }

                    closeModalIfPresent(form);

                    form.dispatchEvent(new CustomEvent('form:success', {
                        bubbles: true,
                        detail: responseData
                    }));

                    setTimeout(() => {
                        window.location.reload();
                    }, 900);
                }
                // Step 5: Handle 422 Validation Errors (inline per-field messages)
                else if (response.status === 422) {
                    const errorObj = responseData?.error || responseData?.message || 'Please check the highlighted fields and try again.';
                    displayFieldErrors(form, errorObj);
                    showToast('Please review the highlighted fields and try again.', 'error');
                }
                // Step 6: Handle 404 Missing Record Errors
                else if (response.status === 404) {
                    const notFoundMsg = extractErrorMessage(
                        responseData,
                        'We could not find that record. It may have already been removed.'
                    );
                    renderBannerError(form, notFoundMsg);
                    showToast(notFoundMsg, 'error');
                }
                // Step 7: Handle 401/403/500 Server Errors without leaking internals
                else {
                    const serverMsg = extractErrorMessage(
                        responseData,
                        'Something went wrong on our end while saving your changes. Please try again in a moment.'
                    );
                    renderBannerError(form, serverMsg);
                    showToast(serverMsg, 'error');
                }
            } catch (err) {
                // Step 8: Network failure or offline connection
                console.error('Async form binding error:', err);
                const netMsg = 'Unable to reach the server. Please check your internet connection and try again.';
                renderBannerError(form, netMsg);
                showToast(netMsg, 'error');
            } finally {
                // Step 9: Restore Submit Button
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
     * Display an accessible, themed Destructive Action Confirmation Modal.
     * Prevents accidental one-click deletions (Week 8 Task 3).
     */
    function confirmDestructiveAction({ title, message, confirmBtnText = 'Yes, Delete', onConfirm }) {
        let existing = document.getElementById('lcConfirmModal');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'lcConfirmModal';
        overlay.className = 'lc-confirm-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-labelledby', 'lcConfirmTitle');

        overlay.innerHTML = `
            <div class="lc-confirm-card">
                <div class="lc-confirm-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                        <line x1="12" y1="9" x2="12" y2="13"/>
                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                </div>
                <h3 class="lc-confirm-title" id="lcConfirmTitle">${title}</h3>
                <p class="lc-confirm-msg">${message}</p>
                <div class="lc-confirm-actions">
                    <button type="button" class="lc-confirm-btn lc-confirm-btn-cancel" id="lcCancelBtn">Cancel</button>
                    <button type="button" class="lc-confirm-btn lc-confirm-btn-danger" id="lcDangerConfirmBtn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="3 6 5 6 21 6"/>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        </svg>
                        ${confirmBtnText}
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        const cancelBtn = overlay.querySelector('#lcCancelBtn');
        const confirmBtn = overlay.querySelector('#lcDangerConfirmBtn');

        const dismiss = () => {
            overlay.classList.add('closing');
            setTimeout(() => overlay.remove(), 200);
        };

        cancelBtn.addEventListener('click', dismiss);
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) dismiss();
        });

        cancelBtn.focus();

        confirmBtn.addEventListener('click', () => {
            if (typeof onConfirm === 'function') {
                onConfirm(confirmBtn, overlay);
            }
        });
    }

    /**
     * Executes an asynchronous deletion with pending spinner, toast, and row removal.
     */
    function handleAsyncDelete(url, rowEl, itemName = 'Record') {
        confirmDestructiveAction({
            title: `Delete ${itemName}?`,
            message: `Are you sure you want to permanently delete this ${itemName.toLowerCase()}? This action cannot be undone.`,
            confirmBtnText: 'Yes, Delete',
            onConfirm: async (confirmBtn, overlay) => {
                confirmBtn.disabled = true;
                confirmBtn.setAttribute('aria-busy', 'true');
                confirmBtn.innerHTML = `<span class="btn-spinner"></span> Deleting...`;

                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    });

                    const data = await response.json().catch(() => null);

                    if (response.status === 200) {
                        const msg = data?.message || data?.data?.message || `${itemName} deleted successfully.`;
                        showToast(msg, 'success');
                        overlay.remove();

                        if (rowEl) {
                            rowEl.classList.add('row-fade-out');
                            setTimeout(() => {
                                rowEl.remove();
                            }, 350);
                        } else {
                            setTimeout(() => window.location.reload(), 700);
                        }
                    } else if (response.status === 404) {
                        const msg404 = extractErrorMessage(data, 'This record was not found or has already been deleted.');
                        showToast(msg404, 'error');
                        overlay.remove();
                    } else {
                        const msg500 = extractErrorMessage(data, 'We could not delete this record right now. Please try again.');
                        showToast(msg500, 'error');
                        overlay.remove();
                    }
                } catch (err) {
                    console.error('Async delete error:', err);
                    showToast('Unable to reach the server while deleting this record. Please check your connection.', 'error');
                    overlay.remove();
                }
            }
        });
    }

    /**
     * Bind click events on all delete buttons with [data-delete-url] or destructive triggers
     */
    function initAsyncDeletes() {
        document.addEventListener('click', function (e) {
            const deleteTrigger = e.target.closest('[data-delete-url], .btn-action-delete, .btn-delete');
            if (deleteTrigger && deleteTrigger.dataset.deleteUrl) {
                e.preventDefault();
                const url = deleteTrigger.dataset.deleteUrl;
                const rowEl = deleteTrigger.closest('tr, .data-row, .order-row, .delivery-row, .pickup-row, .customer-row, .payment-row');
                const itemName = deleteTrigger.dataset.itemName || 'Record';
                handleAsyncDelete(url, rowEl, itemName);
            }
        });
    }

    /**
     * Auto-bind all matching forms on page load
     */
    function initAsyncForms() {
        const selector = 'form[data-async-form], form.async-form';
        document.querySelectorAll(selector).forEach(bindAsyncForm);
        initAsyncDeletes();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAsyncForms);
    } else {
        initAsyncForms();
    }

    window.bindAsyncForm = bindAsyncForm;
    window.initAsyncForms = initAsyncForms;
    window.confirmDestructiveAction = confirmDestructiveAction;
    window.handleAsyncDelete = handleAsyncDelete;
})();
