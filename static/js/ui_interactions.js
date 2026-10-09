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

    /**
     * 5. Universal Mobile Sidebar Toggle & Drawer Support
     */
    function initMobileSidebar() {
        const topHeaders = document.querySelectorAll(
            '.orders-top-header, .deliveries-top-header, .pickups-top-header, .dashboard-topbar, .customers-top-header, .payments-top-header, .topbar'
        );

        topHeaders.forEach(header => {
            if (!header.querySelector('.mobile-menu-toggle')) {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'mobile-menu-toggle';
                btn.setAttribute('aria-label', 'Toggle Navigation Menu');
                btn.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    document.body.classList.toggle('sidebar-open');
                });
                header.insertBefore(btn, header.firstChild);
            }
        });

        let overlay = document.querySelector('.lc-sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'lc-sidebar-overlay';
            document.body.appendChild(overlay);
        }
        overlay.addEventListener('click', () => {
            document.body.classList.remove('sidebar-open');
        });
    /**
     * 6. Universal Shop Staff Notification Engine & Real-Time Chime
     */
    let lastSeenNotifId = parseInt(localStorage.getItem('lc_last_seen_notif_id') || '0', 10);
    let notifPanelOpen = false;

    // First interaction unlocks AudioContext across modern mobile & desktop browsers
    document.addEventListener('click', function unlockAudioContext() {
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) {
                const ctx = new AudioCtx();
                ctx.resume();
            }
        } catch (e) {}
        document.removeEventListener('click', unlockAudioContext);
    }, { once: true });

    function playStaffChime() {
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            if (ctx.state === 'suspended') {
                ctx.resume();
            }
            const now = ctx.currentTime;

            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(587.33, now); // D5
            osc.frequency.setValueAtTime(880.00, now + 0.12); // A5

            gain.gain.setValueAtTime(0.20, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.45);
        } catch (e) {
            // Browser autoplay safeguard
        }
    }

    function showStaffToast(title, message, type) {
        let container = document.getElementById('lc-universal-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'lc-universal-toast-container';
            container.style.cssText = 'position:fixed; top:20px; right:20px; z-index:999999; display:flex; flex-direction:column; gap:10px; pointer-events:none; max-width:390px; width:calc(100vw - 40px);';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.style.cssText = 'pointer-events:auto; background:#ffffff; border:1.5px solid #3b82f6; border-left:6px solid #2563eb; border-radius:12px; padding:13px 15px; box-shadow:0 12px 30px rgba(0,0,0,0.18); display:flex; gap:12px; align-items:flex-start; animation:slideInRight 0.3s ease-out; font-family:Inter,system-ui,sans-serif;';

        const isDel = type === 'delivery_completed';
        const icon = isDel ? '🚚' : '🧺';

        toast.innerHTML = `
            <div style="font-size:24px; line-height:1; flex-shrink:0;">${icon}</div>
            <div style="flex:1; min-width:0;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                    <strong style="font-size:13px; color:#0f172a;">${title}</strong>
                    <span style="font-size:10px; font-weight:800; color:#2563eb; background:#eff6ff; padding:2px 6px; border-radius:6px;">LIVE ALERT</span>
                </div>
                <div style="font-size:11.5px; color:#475569; line-height:1.35;">${message}</div>
                <div style="margin-top:6px; display:flex; gap:10px; align-items:center;">
                    <a href="/notifications-page" style="font-size:11px; font-weight:700; color:#2563eb; text-decoration:none;">Open Alert Center &rarr;</a>
                </div>
            </div>
            <button type="button" style="background:none; border:none; color:#94a3b8; font-size:18px; cursor:pointer; padding:0; line-height:1;" onclick="this.closest('div[style*=\"pointer-events\"]').remove()">&times;</button>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.transition = 'opacity 0.4s, transform 0.4s';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(50px)';
            setTimeout(() => toast.remove(), 400);
        }, 8000);
    }

    function initStaffNotifications() {
        // Notification Popover Panel
        let panel = document.getElementById('lcNotificationPanel');
        if (!panel) {
            panel = document.createElement('div');
            panel.id = 'lcNotificationPanel';
            panel.style.cssText = 'display:none; position:fixed; z-index:99998; width:340px; max-width:92vw; background:#ffffff; border-radius:12px; box-shadow:0 14px 36px rgba(0,0,0,0.20); border:1px solid #cbd5e1; overflow:hidden; font-family:Inter,system-ui,sans-serif;';
            panel.innerHTML = `
                <div style="background:#0f172a; color:#fff; padding:12px 16px; display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:16px;">🔔</span>
                        <strong style="font-size:13.5px;">Shop Activity Alerts</strong>
                    </div>
                    <button type="button" id="lcMarkReadBtn" style="background:rgba(255,255,255,0.18); border:none; color:#93c5fd; font-size:11px; font-weight:700; padding:4px 8px; border-radius:6px; cursor:pointer;">Mark Read</button>
                </div>
                <div id="lcNotifList" style="max-height:340px; overflow-y:auto; padding:4px 0;">
                    <div style="padding:24px; text-align:center; color:#94a3b8; font-size:12.5px;">No new rider alerts yet.</div>
                </div>
                <a href="/notifications-page" style="display:block; text-align:center; padding:10px; background:#f8fafc; color:#2563eb; font-weight:700; font-size:12px; text-decoration:none; border-top:1px solid #e2e8f0;">View All in Notification Center &rarr;</a>
            `;
            document.body.appendChild(panel);

            const markBtn = panel.querySelector('#lcMarkReadBtn');
            if (markBtn) {
                markBtn.addEventListener('click', () => {
                    fetch('/api/notifications/mark-read', { credentials: 'same-origin', method: 'POST', headers: { 'Content-Type': 'application/json' } })
                        .then(() => {
                            document.querySelectorAll('.bell-badge').forEach(b => b.style.display = 'none');
                            document.querySelectorAll('.sidebar-notif-badge, #sidebarNotifBadge').forEach(sb => sb.style.display = 'none');
                            poll();
                        })
                        .catch(() => {});
                });
            }
        }

        function positionPanel(targetBell) {
            if (!targetBell || !panel) return;
            const rect = targetBell.getBoundingClientRect();
            panel.style.top = (rect.bottom + 8) + 'px';
            const leftPos = Math.max(10, rect.right - 340);
            panel.style.left = leftPos + 'px';
        }

        function togglePanel(targetBell) {
            if (panel.style.display === 'none' || !panel.style.display) {
                positionPanel(targetBell);
                panel.style.display = 'block';
                notifPanelOpen = true;
            } else {
                panel.style.display = 'none';
                notifPanelOpen = false;
            }
        }

        // Bind all bells across top headers
        document.querySelectorAll('.bell-btn').forEach(btn => {
            btn.onclick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                togglePanel(btn);
            };
        });

        document.addEventListener('click', (e) => {
            if (panel && notifPanelOpen && !panel.contains(e.target) && !e.target.closest('.bell-btn')) {
                panel.style.display = 'none';
                notifPanelOpen = false;
            }
        });

        function renderNotifs(notifs) {
            const listEl = document.getElementById('lcNotifList');
            if (!listEl) return;
            if (!notifs || notifs.length === 0) {
                listEl.innerHTML = '<div style="padding:24px; text-align:center; color:#94a3b8; font-size:12.5px;">No recent rider alerts.</div>';
                return;
            }
            listEl.innerHTML = notifs.map(n => {
                const isDel = n.type === 'delivery_completed';
                const icon = isDel ? '🚚' : '🧺';
                const bg = isDel ? '#ecfdf5' : '#eff6ff';
                const iconBg = isDel ? '#10b981' : '#2563eb';
                const link = isDel ? '/delivery-records-page' : '/pickup-schedules-page';
                return `
                    <div style="display:flex; gap:10px; padding:10px 14px; border-bottom:1px solid #f1f5f9; background:${n.is_read ? '#fff' : bg}; transition:background 0.2s;">
                        <div style="width:30px; height:30px; border-radius:8px; background:${iconBg}; color:#fff; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:14px;">
                            ${icon}
                        </div>
                        <div style="flex:1; min-width:0;">
                            <div style="font-weight:700; font-size:12.5px; color:#0f172a; display:flex; justify-content:space-between;">
                                <span>${n.title}</span>
                                <span style="font-size:10px; font-weight:500; color:#94a3b8;">${n.created_at ? n.created_at.slice(11, 16) : ''}</span>
                            </div>
                            <div style="font-size:11.5px; color:#475569; margin-top:2px; line-height:1.3;">${n.message}</div>
                            <a href="${link}" style="display:inline-block; margin-top:4px; font-size:10.5px; font-weight:700; color:#2563eb; text-decoration:none;">View in Registry →</a>
                        </div>
                    </div>
                `;
            }).join('');
        }

        // Live Poll Function
        function poll() {
            fetch('/api/notifications/poll?last_id=' + lastSeenNotifId, { credentials: 'same-origin' })
                .then(res => {
                    if (!res.ok) throw new Error('Unauth or error');
                    return res.json();
                })
                .then(data => {
                    if (data && data.status === 200) {
                        // Update all bell badges
                        document.querySelectorAll('.bell-badge').forEach(b => {
                            if (data.unread_count > 0) {
                                b.style.display = 'flex';
                                b.textContent = data.unread_count;
                            } else {
                                b.style.display = 'none';
                            }
                        });

                        // Update all sidebar badges
                        document.querySelectorAll('.sidebar-notif-badge, #sidebarNotifBadge').forEach(sb => {
                            if (data.unread_count > 0) {
                                sb.style.display = 'inline-block';
                                sb.textContent = data.unread_count;
                            } else {
                                sb.style.display = 'none';
                            }
                        });

                        // Play chime and toast for newly arrived completions
                        if (data.new_notifications && data.new_notifications.length > 0) {
                            data.new_notifications.forEach(n => {
                                if (n.id > lastSeenNotifId) {
                                    lastSeenNotifId = n.id;
                                    localStorage.setItem('lc_last_seen_notif_id', lastSeenNotifId);
                                }
                                playStaffChime();
                                showStaffToast('🔔 ' + n.title, n.message, n.type);
                            });
                        } else if (data.unread_count > 0 && data.recent && data.recent.length > 0) {
                            // Check if the latest unread alert has been toasted on this browser
                            const topNotif = data.recent[0];
                            const lastToasted = parseInt(localStorage.getItem('lc_last_toasted_id') || '0', 10);
                            if (topNotif.id > lastToasted) {
                                localStorage.setItem('lc_last_toasted_id', topNotif.id);
                                playStaffChime();
                                showStaffToast('🔔 ' + topNotif.title, topNotif.message, topNotif.type);
                            }
                        }

                        if (data.recent) {
                            renderNotifs(data.recent);
                            if (data.recent.length > 0) {
                                const maxId = Math.max(...data.recent.map(r => r.id));
                                if (maxId > lastSeenNotifId) {
                                    lastSeenNotifId = maxId;
                                    localStorage.setItem('lc_last_seen_notif_id', lastSeenNotifId);
                                }
                            }

                            const dashList = document.getElementById('dashboardLiveNotifList');
                            if (dashList && data.recent.length > 0) {
                                dashList.innerHTML = data.recent.slice(0, 5).map(n => {
                                    const isDel = n.type === 'delivery_completed';
                                    const bg = isDel ? '#f0fdf4' : '#eff6ff';
                                    const border = isDel ? '#bbf7d0' : '#bfdbfe';
                                    const icon = isDel ? '🚚' : '🧺';
                                    const timeStr = n.created_at ? n.created_at.slice(11, 16) : '';
                                    return `
                                        <div style="display: flex; gap: 10px; align-items: center; padding: 10px 12px; background: ${bg}; border: 1px solid ${border}; border-radius: 10px;">
                                            <div style="font-size: 18px;">${icon}</div>
                                            <div style="flex: 1; min-width: 0;">
                                                <div style="font-size: 12.5px; font-weight: 700; color: #0f172a;">${n.title}</div>
                                                <div style="font-size: 11.5px; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${n.message}</div>
                                            </div>
                                            <span style="font-size: 10px; font-weight: 600; color: #94a3b8; white-space: nowrap;">${timeStr}</span>
                                        </div>
                                    `;
                                }).join('');
                            }
                        }
                    }
                })
                .catch(() => {});
        }

        poll();
        setInterval(poll, 5000);
    }

    // Auto-init on DOMContentLoaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initCounters();
            initStaggeredTables();
            initButtonFeedback();
            initMobileSidebar();
            initStaffNotifications();
        });
    } else {
        initCounters();
        initStaggeredTables();
        initButtonFeedback();
        initMobileSidebar();
        initStaffNotifications();
    }
})();
