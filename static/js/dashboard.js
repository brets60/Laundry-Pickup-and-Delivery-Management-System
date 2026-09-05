document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const menuButton = document.getElementById("menuButton");
    const closeButton = document.getElementById("sidebarClose");


    /* =====================================================
       OPEN SIDEBAR
    ===================================================== */

    function openSidebar() {

        if (!sidebar) return;

        sidebar.classList.add("open");

        if (overlay) {
            overlay.classList.add("active");
            overlay.setAttribute("aria-hidden", "false");
        }

        if (menuButton) {
            menuButton.setAttribute("aria-expanded", "true");
        }

        document.body.style.overflow = "hidden";
    }


    /* =====================================================
       CLOSE SIDEBAR
    ===================================================== */

    function closeSidebar() {

        if (!sidebar) return;

        sidebar.classList.remove("open");

        if (overlay) {
            overlay.classList.remove("active");
            overlay.setAttribute("aria-hidden", "true");
        }

        if (menuButton) {
            menuButton.setAttribute("aria-expanded", "false");
        }

        document.body.style.overflow = "";
    }


    /* =====================================================
       MOBILE MENU BUTTON
    ===================================================== */

    if (menuButton) {
        menuButton.addEventListener("click", function () {

            if (sidebar && sidebar.classList.contains("open")) {
                closeSidebar();
            } else {
                openSidebar();
            }

        });
    }


    /* =====================================================
       CLOSE BUTTON
    ===================================================== */

    if (closeButton) {
        closeButton.addEventListener("click", closeSidebar);
    }


    /* =====================================================
       OVERLAY
    ===================================================== */

    if (overlay) {
        overlay.addEventListener("click", closeSidebar);
    }


    /* =====================================================
       NAVIGATION
    ===================================================== */

    if (sidebar) {

        const navItems = sidebar.querySelectorAll(".lc-nav-item");

        navItems.forEach(function (item) {

            item.addEventListener("click", function () {

                /*
                 * Navigation is handled by the <a href="">
                 * element itself.
                 *
                 * On mobile, close the drawer before leaving.
                 */

                if (window.innerWidth <= 760) {
                    closeSidebar();
                }

            });

        });
    }


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            if (
                sidebar &&
                sidebar.classList.contains("open")
            ) {
                closeSidebar();
            }

        }

    });


    /* =====================================================
       WINDOW RESIZE
    ===================================================== */

    window.addEventListener("resize", function () {

        if (window.innerWidth > 760) {
            closeSidebar();
        }

    });

});

/* =========================================================
   STEP 17 — DASHBOARD NOTIFICATION BUTTON
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const notificationButton =
    document.querySelector(".new-header-notification");


if (!notificationButton) {
    return;
}

    notificationButton.addEventListener("click", function (event) {

        event.preventDefault();


        const existingMessage =
            document.querySelector(".dashboard-notification-message");

        if (existingMessage) {
            existingMessage.remove();
            return;
        }

        const message =
            document.createElement("div");

        message.className =
            "dashboard-notification-message";

        message.innerHTML = `
            <div class="dashboard-notification-icon">
                ✓
            </div>

            <div>
                <strong>System Notifications</strong>
                <span>
                    No new notifications at this time.
                </span>
            </div>
        `;

        document.body.appendChild(message);

        setTimeout(function () {

            if (message.parentNode) {
                message.classList.add("notification-hide");

                setTimeout(function () {

                    if (message.parentNode) {
                        message.remove();
                    }

                }, 250);

            }

        }, 3500);

    });

});