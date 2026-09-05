/* =========================================================
   LAUNDRYCARE DELIVERY CONTROL CENTER
   Delivery Records JavaScript
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    "use strict";


    /* =====================================================
       ELEMENTS
    ====================================================== */

    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const mobileMenuButton = document.getElementById("mobileMenuButton");

    const newDeliveryButton =
        document.getElementById("newDeliveryButton");

    const emptyCreateButton =
        document.getElementById("emptyCreateButton");

    const createDeliverySection =
        document.getElementById("createDeliverySection");

    const deliveryForm =
        document.getElementById("deliveryForm");

    const customerInput =
        document.getElementById("customer");

    const deliveryDateInput =
        document.getElementById("delivery_date");

    const customerError =
        document.getElementById("customerError");

    const deliveryDateError =
        document.getElementById("deliveryDateError");

    const submitDeliveryButton =
        document.getElementById("submitDeliveryButton");

    const deliverySearch =
        document.getElementById("deliverySearch");

    const clearSearch =
        document.getElementById("clearSearch");

    const searchEmpty =
        document.getElementById("searchEmpty");

    const deliveryRows =
        Array.from(document.querySelectorAll(".delivery-row"));

    const deleteModal =
        document.getElementById("deleteModal");

    const closeDeleteModal =
        document.getElementById("closeDeleteModal");

    const cancelDelete =
        document.getElementById("cancelDelete");

    const confirmDelete =
        document.getElementById("confirmDelete");

    const deleteDeliveryId =
        document.getElementById("deleteDeliveryId");

    const deleteCustomer =
        document.getElementById("deleteCustomer");

    const deleteDate =
        document.getElementById("deleteDate");


    let deleteTargetForm = null;
    let previousFocusedElement = null;


    /* =====================================================
       SIDEBAR
    ====================================================== */

    function openSidebar() {

        if (!sidebar) {
            return;
        }

        sidebar.classList.add("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.add("visible");
            sidebarOverlay.setAttribute("aria-hidden", "false");
        }

        if (mobileMenuButton) {
            mobileMenuButton.setAttribute(
                "aria-expanded",
                "true"
            );
        }

        document.body.style.overflow = "hidden";
    }


    function closeSidebar() {

        if (!sidebar) {
            return;
        }

        sidebar.classList.remove("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("visible");
            sidebarOverlay.setAttribute("aria-hidden", "true");
        }

        if (mobileMenuButton) {
            mobileMenuButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }

        document.body.style.overflow = "";
    }


    if (mobileMenuButton) {

        mobileMenuButton.addEventListener(
            "click",
            function () {

                if (sidebar.classList.contains("open")) {
                    closeSidebar();
                } else {
                    openSidebar();
                }

            }
        );

    }


    if (sidebarOverlay) {

        sidebarOverlay.addEventListener(
            "click",
            closeSidebar
        );

    }


    document.querySelectorAll(".nav-link, .logout-link")
        .forEach(function (link) {

            link.addEventListener(
                "click",
                function () {

                    if (window.innerWidth <= 720) {
                        closeSidebar();
                    }

                }
            );

        });


    window.addEventListener(
        "resize",
        function () {

            if (window.innerWidth > 720) {
                closeSidebar();
            }

        }
    );


    /* =====================================================
       SCROLL TO CREATE FORM
    ====================================================== */

    function focusCreateForm() {

        if (!createDeliverySection) {
            return;
        }

        createDeliverySection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


        window.setTimeout(
            function () {

                if (customerInput) {

                    if (!customerInput.readOnly) {
                        customerInput.focus();
                    } else if (deliveryDateInput) {
                        deliveryDateInput.focus();
                    }

                }

            },
            500
        );

    }


    if (newDeliveryButton) {

        newDeliveryButton.addEventListener(
            "click",
            focusCreateForm
        );

    }


    if (emptyCreateButton) {

        emptyCreateButton.addEventListener(
            "click",
            focusCreateForm
        );

    }


    /* =====================================================
       DATE FORMATTER
    ====================================================== */

    function formatDate(value) {

        if (!value) {
            return "";
        }

        const trimmed =
            String(value).trim();

        /*
         * Existing backend stores dates as YYYY-MM-DD.
         * We only change visual presentation.
         */

        const isoMatch =
            trimmed.match(
                /^(\d{4})-(\d{2})-(\d{2})$/
            );

        if (isoMatch) {

            const year =
                Number(isoMatch[1]);

            const month =
                Number(isoMatch[2]);

            const day =
                Number(isoMatch[3]);

            const date =
                new Date(
                    year,
                    month - 1,
                    day
                );

            if (
                date.getFullYear() === year &&
                date.getMonth() === month - 1 &&
                date.getDate() === day
            ) {

                return date.toLocaleDateString(
                    undefined,
                    {
                        month: "short",
                        day: "numeric",
                        year: "numeric"
                    }
                );

            }

        }

        return trimmed;
    }


    document
        .querySelectorAll(".formatted-date")
        .forEach(function (element) {

            const rawDate =
                element.dataset.date;

            const formatted =
                formatDate(rawDate);

            if (formatted) {
                element.textContent = formatted;
            }

        });


    /* =====================================================
       CUSTOMER INITIALS
    ====================================================== */

    function getInitials(name) {

        if (!name) {
            return "?";
        }

        const cleaned =
            String(name)
                .trim()
                .replace(/\s+/g, " ");

        if (!cleaned) {
            return "?";
        }

        const parts =
            cleaned.split(" ");

        if (parts.length === 1) {

            return parts[0]
                .substring(0, 2)
                .toUpperCase();

        }

        return (
            parts[0].charAt(0) +
            parts[parts.length - 1].charAt(0)
        ).toUpperCase();
    }


    deliveryRows.forEach(function (row) {

        const customer =
            row.dataset.customer || "";

        const initialsElement =
            row.querySelector("[data-initials]");

        if (initialsElement) {

            initialsElement.textContent =
                getInitials(customer);

        }

    });


    /* =====================================================
       COMMAND CENTER DATE STATISTICS
    ====================================================== */

    function getLocalDateKey(date) {

        const year =
            date.getFullYear();

        const month =
            String(
                date.getMonth() + 1
            ).padStart(2, "0");

        const day =
            String(
                date.getDate()
            ).padStart(2, "0");

        return (
            year +
            "-" +
            month +
            "-" +
            day
        );
    }


    function getValidISODate(value) {

        if (!value) {
            return null;
        }

        const match =
            String(value)
                .trim()
                .match(
                    /^(\d{4})-(\d{2})-(\d{2})$/
                );

        if (!match) {
            return null;
        }

        const year =
            Number(match[1]);

        const month =
            Number(match[2]);

        const day =
            Number(match[3]);

        const date =
            new Date(
                year,
                month - 1,
                day
            );

        if (
            date.getFullYear() !== year ||
            date.getMonth() !== month - 1 ||
            date.getDate() !== day
        ) {
            return null;
        }

        return date;
    }


    function updateDeliveryStatistics() {

        const todayElement =
            document.getElementById(
                "todayDeliveries"
            );

        const upcomingElement =
            document.getElementById(
                "upcomingDeliveries"
            );

        if (
            !todayElement ||
            !upcomingElement
        ) {
            return;
        }

        const today =
            new Date();

        const todayKey =
            getLocalDateKey(today);

        let todayCount = 0;
        let upcomingCount = 0;

        deliveryRows.forEach(function (row) {

            const rawDate =
                row.dataset.date;

            const date =
                getValidISODate(rawDate);

            if (!date) {
                return;
            }

            const dateKey =
                getLocalDateKey(date);

            if (dateKey === todayKey) {

                todayCount += 1;

            } else if (date > today) {

                /*
                 * Date-only comparison.
                 * No time/status is fabricated.
                 */

                upcomingCount += 1;

            }

        });


        todayElement.textContent =
            todayCount;

        upcomingElement.textContent =
            upcomingCount;
    }


    updateDeliveryStatistics();


    /* =====================================================
       SEARCH
    ====================================================== */

    function filterDeliveryRecords() {

        if (!deliverySearch) {
            return;
        }

        const query =
            deliverySearch.value
                .trim()
                .toLowerCase();

        let visibleCount = 0;


        deliveryRows.forEach(function (row) {

            const id =
                row.dataset.id || "";

            const customer =
                row.dataset.customer || "";

            const date =
                row.dataset.date || "";

            const formattedDateElement =
                row.querySelector(
                    ".formatted-date"
                );

            const formattedDate =
                formattedDateElement
                    ? formattedDateElement.textContent
                    : "";

            const searchableText =
                (
                    id +
                    " " +
                    customer +
                    " " +
                    date +
                    " " +
                    formattedDate
                ).toLowerCase();


            const matches =
                searchableText.includes(query);


            row.style.display =
                matches
                    ? ""
                    : "none";


            if (matches) {
                visibleCount += 1;
            }

        });


        if (clearSearch) {

            clearSearch.hidden =
                query.length === 0;

        }


        if (searchEmpty) {

            searchEmpty.hidden =
                visibleCount !== 0;

        }

    }


    if (deliverySearch) {

        deliverySearch.addEventListener(
            "input",
            filterDeliveryRecords
        );

    }


    if (clearSearch) {

        clearSearch.addEventListener(
            "click",
            function () {

                if (!deliverySearch) {
                    return;
                }

                deliverySearch.value = "";

                filterDeliveryRecords();

                deliverySearch.focus();

            }
        );

    }


    /* =====================================================
       FORM VALIDATION
    ====================================================== */

    function clearFieldError(
        field,
        errorElement
    ) {

        if (field) {
            field.closest(".form-field")
                ?.classList.remove("invalid");
        }

        if (errorElement) {
            errorElement.textContent = "";
        }

    }


    function showFieldError(
        field,
        errorElement,
        message
    ) {

        if (field) {
            field.closest(".form-field")
                ?.classList.add("invalid");
        }

        if (errorElement) {
            errorElement.textContent =
                message;
        }

    }


    function validateCustomer() {

        if (!customerInput) {
            return true;
        }

        const value =
            customerInput.value.trim();


        if (!value) {

            showFieldError(
                customerInput,
                customerError,
                "Customer name is required."
            );

            return false;
        }


        clearFieldError(
            customerInput,
            customerError
        );

        return true;
    }


    function validateDeliveryDate() {

        if (!deliveryDateInput) {
            return true;
        }

        const value =
            deliveryDateInput.value.trim();


        if (!value) {

            showFieldError(
                deliveryDateInput,
                deliveryDateError,
                "Delivery date is required."
            );

            return false;
        }


        const date =
            getValidISODate(value);


        if (!date) {

            showFieldError(
                deliveryDateInput,
                deliveryDateError,
                "Please select a valid delivery date."
            );

            return false;
        }


        clearFieldError(
            deliveryDateInput,
            deliveryDateError
        );

        return true;
    }


    if (customerInput) {

        customerInput.addEventListener(
            "blur",
            validateCustomer
        );

        customerInput.addEventListener(
            "input",
            function () {

                if (
                    customerInput.value.trim()
                ) {
                    clearFieldError(
                        customerInput,
                        customerError
                    );
                }

            }
        );

    }


    if (deliveryDateInput) {

        deliveryDateInput.addEventListener(
            "blur",
            validateDeliveryDate
        );

        deliveryDateInput.addEventListener(
            "change",
            validateDeliveryDate
        );

    }


    /* =====================================================
       NORMAL FLASK FORM SUBMISSION
    ====================================================== */

    if (deliveryForm) {

        deliveryForm.addEventListener(
            "submit",
            function (event) {

                const customerValid =
                    validateCustomer();

                const dateValid =
                    validateDeliveryDate();


                if (
                    !customerValid ||
                    !dateValid
                ) {

                    event.preventDefault();

                    if (!customerValid) {

                        customerInput?.focus();

                    } else {

                        deliveryDateInput?.focus();

                    }

                    return;
                }


                /*
                 * IMPORTANT:
                 * We do NOT use AJAX.
                 * We do NOT replace Flask submission.
                 * We only change the button appearance.
                 */

                if (submitDeliveryButton) {

                    submitDeliveryButton.disabled =
                        true;

                    submitDeliveryButton.classList.add(
                        "loading"
                    );

                    const buttonText =
                        submitDeliveryButton.querySelector(
                            ".button-text"
                        );

                    if (buttonText) {

                        buttonText.textContent =
                            "Adding Delivery...";

                    }

                }

            }
        );

    }


    /* =====================================================
       DELETE MODAL
    ====================================================== */

    function openDeleteModal(button) {

        if (!deleteModal || !button) {
            return;
        }

        previousFocusedElement =
            document.activeElement;

        deleteTargetForm =
            button.closest("form");


        const id =
            button.dataset.id || "";

        const customer =
            button.dataset.customer || "";

        const date =
            button.dataset.date || "";


        if (deleteDeliveryId) {

            deleteDeliveryId.textContent =
                "#" +
                String(id).padStart(3, "0");

        }


        if (deleteCustomer) {

            deleteCustomer.textContent =
                customer || "—";

        }


        if (deleteDate) {

            deleteDate.textContent =
                formatDate(date) || "—";

        }


        deleteModal.hidden = false;

        document.body.style.overflow =
            "hidden";


        window.setTimeout(
            function () {

                closeDeleteModal?.focus();

            },
            50
        );

    }


    function closeDeleteConfirmation() {

        if (!deleteModal) {
            return;
        }

        deleteModal.hidden = true;

        document.body.style.overflow =
            "";

        deleteTargetForm = null;


        if (
            previousFocusedElement &&
            typeof previousFocusedElement.focus === "function"
        ) {

            previousFocusedElement.focus();

        }

        previousFocusedElement = null;
    }


    document
        .querySelectorAll("[data-delete-button]")
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    openDeleteModal(button);

                }
            );

        });


    if (closeDeleteModal) {

        closeDeleteModal.addEventListener(
            "click",
            closeDeleteConfirmation
        );

    }


    if (cancelDelete) {

        cancelDelete.addEventListener(
            "click",
            closeDeleteConfirmation
        );

    }


    if (confirmDelete) {

        confirmDelete.addEventListener(
            "click",
            function () {

                if (!deleteTargetForm) {
                    return;
                }

                /*
                 * IMPORTANT:
                 * The real POST still goes to:
                 *
                 * /delivery-records-page/delete/<id>
                 *
                 * JavaScript only confirms intent.
                 */

                deleteTargetForm.submit();

            }
        );

    }


    if (deleteModal) {

        deleteModal.addEventListener(
            "click",
            function (event) {

                if (
                    event.target === deleteModal
                ) {

                    closeDeleteConfirmation();

                }

            }
        );

    }


    /* =====================================================
       KEYBOARD MODAL CONTROL
    ====================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {

                if (
                    deleteModal &&
                    !deleteModal.hidden
                ) {

                    closeDeleteConfirmation();

                }

                if (
                    sidebar &&
                    sidebar.classList.contains("open")
                ) {

                    closeSidebar();

                }

            }

        }
    );


    /* =====================================================
       SIMPLE MODAL FOCUS PROTECTION
    ====================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key !== "Tab" ||
                !deleteModal ||
                deleteModal.hidden
            ) {
                return;
            }


            const focusable =
                deleteModal.querySelectorAll(
                    "button:not([disabled])"
                );


            if (!focusable.length) {
                return;
            }


            const first =
                focusable[0];

            const last =
                focusable[
                    focusable.length - 1
                ];


            if (
                event.shiftKey &&
                document.activeElement === first
            ) {

                event.preventDefault();

                last.focus();

            } else if (
                !event.shiftKey &&
                document.activeElement === last
            ) {

                event.preventDefault();

                first.focus();

            }

        }
    );


    /* =====================================================
       INITIAL SEARCH STATE
    ====================================================== */

    filterDeliveryRecords();

});