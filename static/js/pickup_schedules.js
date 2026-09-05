document.addEventListener("DOMContentLoaded", function () {

    "use strict";


    /* =========================================
       ELEMENTS
    ========================================= */

    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const mobileMenuButton = document.getElementById("mobileMenuButton");

    const newPickupButton = document.getElementById("newPickupButton");
    const emptyCreateButton = document.getElementById("emptyCreateButton");

    const pickupFormSection = document.getElementById("pickupFormSection");
    const pickupForm = document.getElementById("pickupForm");

    const customerInput = document.getElementById("customer");
    const pickupDateInput = document.getElementById("pickup_date");

    const customerError = document.getElementById("customerError");
    const pickupDateError = document.getElementById("pickupDateError");

    const submitPickupButton =
        document.getElementById("submitPickupButton");

    const pickupSearch =
        document.getElementById("pickupSearch");

    const searchClear =
        document.getElementById("searchClear");

    const pickupRows =
        Array.from(document.querySelectorAll(".pickup-row"));

    const searchEmpty =
        document.getElementById("searchEmpty");

    const totalPickups =
        document.getElementById("totalPickups");

    const upcomingPickups =
        document.getElementById("upcomingPickups");

    const todayPickups =
        document.getElementById("todayPickups");


    /* =========================================
       SIDEBAR
    ========================================= */

    function openSidebar() {

        if (!sidebar) {
            return;
        }

        sidebar.classList.add("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.add("visible");
        }

        if (mobileMenuButton) {
            mobileMenuButton.setAttribute("aria-expanded", "true");
        }
    }


    function closeSidebar() {

        if (!sidebar) {
            return;
        }

        sidebar.classList.remove("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("visible");
        }

        if (mobileMenuButton) {
            mobileMenuButton.setAttribute("aria-expanded", "false");
        }
    }


    if (mobileMenuButton) {

        mobileMenuButton.addEventListener("click", function () {

            if (sidebar.classList.contains("open")) {
                closeSidebar();
            } else {
                openSidebar();
            }

        });

    }


    if (sidebarOverlay) {

        sidebarOverlay.addEventListener("click", closeSidebar);

    }


    document.querySelectorAll(".nav-item, .logout-link").forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 760) {
                closeSidebar();
            }

        });

    });


    window.addEventListener("resize", function () {

        if (window.innerWidth > 760) {
            closeSidebar();
        }

    });


    /* =========================================
       SCROLL TO FORM
    ========================================= */

    function focusPickupForm() {

        if (!pickupFormSection) {
            return;
        }

        pickupFormSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


        window.setTimeout(function () {

            if (customerInput && !customerInput.readOnly) {
                customerInput.focus();
            } else if (pickupDateInput) {
                pickupDateInput.focus();
            }

        }, 450);

    }


    if (newPickupButton) {
        newPickupButton.addEventListener("click", focusPickupForm);
    }


    if (emptyCreateButton) {
        emptyCreateButton.addEventListener("click", focusPickupForm);
    }


    /* =========================================
       CUSTOMER INITIALS
    ========================================= */

    function generateInitials(name) {

        if (!name) {
            return "CU";
        }

        const cleaned = name
            .trim()
            .replace(/\s+/g, " ");

        if (!cleaned) {
            return "CU";
        }

        const parts = cleaned.split(" ");

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


    document.querySelectorAll(".customer-avatar").forEach(function (avatar) {

        const customerName =
            avatar.getAttribute("data-initials") || "";

        avatar.textContent =
            generateInitials(customerName);

    });


    /* =========================================
       DATE HELPERS
    ========================================= */

    function parseLocalDate(dateString) {

        if (!dateString) {
            return null;
        }

        const match =
            /^(\d{4})-(\d{2})-(\d{2})$/.exec(
                dateString.trim()
            );

        if (!match) {
            return null;
        }

        const year = Number(match[1]);
        const month = Number(match[2]);
        const day = Number(match[3]);

        const date =
            new Date(year, month - 1, day);

        if (
            date.getFullYear() !== year ||
            date.getMonth() !== month - 1 ||
            date.getDate() !== day
        ) {
            return null;
        }

        return date;

    }


    function startOfToday() {

        const now = new Date();

        return new Date(
            now.getFullYear(),
            now.getMonth(),
            now.getDate()
        );

    }


    function formatDate(dateString) {

        const date =
            parseLocalDate(dateString);

        if (!date) {
            return dateString || "";
        }

        return new Intl.DateTimeFormat(
            undefined,
            {
                month: "short",
                day: "numeric",
                year: "numeric"
            }
        ).format(date);

    }


    /* =========================================
       DATE PRESENTATION
    ========================================= */

    document.querySelectorAll(".formatted-date").forEach(function (element) {

        const dateString =
            element.getAttribute("data-date");

        const formatted =
            formatDate(dateString);

        if (formatted) {
            element.textContent = formatted;
        }

    });


    /* =========================================
       DATE STATUS
    ========================================= */

    function updateDateStatuses() {

        const today =
            startOfToday();

        let upcoming = 0;
        let todayCount = 0;

        document
            .querySelectorAll(".date-status")
            .forEach(function (statusElement) {

                const dateString =
                    statusElement.getAttribute(
                        "data-status-date"
                    );

                const date =
                    parseLocalDate(dateString);

                statusElement.classList.remove(
                    "status-today",
                    "status-upcoming",
                    "status-past"
                );


                if (!date) {

                    statusElement.textContent =
                        "Scheduled pickup";

                    return;

                }


                if (date.getTime() === today.getTime()) {

                    todayCount++;

                    statusElement.textContent =
                        "Today";

                    statusElement.classList.add(
                        "status-today"
                    );

                } else if (date > today) {

                    upcoming++;

                    statusElement.textContent =
                        "Upcoming";

                    statusElement.classList.add(
                        "status-upcoming"
                    );

                } else {

                    statusElement.textContent =
                        "Scheduled pickup";

                    statusElement.classList.add(
                        "status-past"
                    );

                }

            });


        if (totalPickups) {
            totalPickups.textContent =
                pickupRows.length;
        }


        if (upcomingPickups) {
            upcomingPickups.textContent =
                upcoming;
        }


        if (todayPickups) {
            todayPickups.textContent =
                todayCount;
        }

    }


    updateDateStatuses();


    /* =========================================
       FORM VALIDATION
    ========================================= */

    function clearFieldError(input, errorElement) {

        if (input) {
            input.closest(".form-group")
                ?.classList.remove("has-error");
        }

        if (errorElement) {
            errorElement.textContent = "";
        }

    }


    function showFieldError(
        input,
        errorElement,
        message
    ) {

        if (input) {
            input.closest(".form-group")
                ?.classList.add("has-error");
        }

        if (errorElement) {
            errorElement.textContent = message;
        }

    }


    function validateCustomer() {

        if (!customerInput) {
            return true;
        }

        if (customerInput.readOnly) {
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


    function validatePickupDate() {

        if (!pickupDateInput) {
            return true;
        }

        const value =
            pickupDateInput.value.trim();

        if (!value) {

            showFieldError(
                pickupDateInput,
                pickupDateError,
                "Pickup date is required."
            );

            return false;

        }


        const date =
            parseLocalDate(value);

        if (!date) {

            showFieldError(
                pickupDateInput,
                pickupDateError,
                "Please select a valid pickup date."
            );

            return false;

        }


        clearFieldError(
            pickupDateInput,
            pickupDateError
        );

        return true;

    }


    if (customerInput) {

        customerInput.addEventListener(
            "input",
            validateCustomer
        );

        customerInput.addEventListener(
            "blur",
            validateCustomer
        );

    }


    if (pickupDateInput) {

        pickupDateInput.addEventListener(
            "change",
            validatePickupDate
        );

        pickupDateInput.addEventListener(
            "blur",
            validatePickupDate
        );

    }


    if (pickupForm) {

        pickupForm.addEventListener(
            "submit",
            function (event) {

                const customerValid =
                    validateCustomer();

                const dateValid =
                    validatePickupDate();

                if (!customerValid || !dateValid) {

                    event.preventDefault();

                    if (!customerValid && customerInput) {
                        customerInput.focus();
                    } else if (!dateValid && pickupDateInput) {
                        pickupDateInput.focus();
                    }

                    return;
                }


                if (submitPickupButton) {

                    submitPickupButton.classList.add(
                        "loading"
                    );

                    submitPickupButton
                        .querySelector(".button-text")
                        .textContent =
                        "Scheduling Pickup...";

                }

            }
        );

    }


    /* =========================================
       SEARCH
    ========================================= */

    function performSearch() {

        if (!pickupSearch) {
            return;
        }

        const query =
            pickupSearch.value
                .trim()
                .toLowerCase();


        let visibleCount = 0;


        pickupRows.forEach(function (row) {

            const id =
                row.getAttribute("data-id") || "";

            const customer =
                row.getAttribute("data-customer") || "";

            const date =
                row.getAttribute("data-date") || "";


            const searchableText = (
                id + " " +
                customer + " " +
                date
            ).toLowerCase();


            const matches =
                !query ||
                searchableText.includes(query);


            row.style.display =
                matches ? "" : "none";


            if (matches) {
                visibleCount++;
            }

        });


        if (searchEmpty) {

            searchEmpty.hidden =
                visibleCount !== 0;

        }


        if (searchClear) {

            searchClear.classList.toggle(
                "visible",
                query.length > 0
            );

        }

    }


    if (pickupSearch) {

        pickupSearch.addEventListener(
            "input",
            performSearch
        );

    }


    if (searchClear) {

        searchClear.addEventListener(
            "click",
            function () {

                if (!pickupSearch) {
                    return;
                }

                pickupSearch.value = "";

                performSearch();

                pickupSearch.focus();

            }
        );

    }


    /* =========================================
       FLASH ALERT CLOSE
    ========================================= */

    document.querySelectorAll(".flash-close").forEach(function (button) {

        button.addEventListener("click", function () {

            const alert =
                button.closest(".flash-alert");

            if (!alert) {
                return;
            }

            alert.style.opacity = "0";
            alert.style.transform = "translateY(-5px)";

            window.setTimeout(function () {
                alert.remove();
            }, 180);

        });

    });


    /* =========================================
       DELETE MODAL
    ========================================= */

    const deleteModal =
        document.getElementById("deleteModal");

    const deleteModalClose =
        document.getElementById("deleteModalClose");

    const cancelDeleteButton =
        document.getElementById("cancelDeleteButton");

    const deleteModalForm =
        document.getElementById("deleteModalForm");

    const deletePickupId =
        document.getElementById("deletePickupId");

    const deleteCustomer =
        document.getElementById("deleteCustomer");

    const deletePickupDate =
        document.getElementById("deletePickupDate");


    let lastFocusedDeleteButton = null;


    function openDeleteModal(button) {

        if (!deleteModal || !button) {
            return;
        }


        lastFocusedDeleteButton =
            button;


        const id =
            button.getAttribute("data-id") || "";

        const customer =
            button.getAttribute("data-customer") || "";

        const date =
            button.getAttribute("data-date") || "";

        const deleteUrl =
            button.getAttribute("data-delete-url") || "";


        if (deletePickupId) {
            deletePickupId.textContent =
                "#" +
                String(id).padStart(3, "0");
        }


        if (deleteCustomer) {
            deleteCustomer.textContent =
                customer;
        }


        if (deletePickupDate) {
            deletePickupDate.textContent =
                formatDate(date);
        }


        if (deleteModalForm) {
            deleteModalForm.action =
                deleteUrl;
        }


        deleteModal.hidden = false;

        document.body.style.overflow = "hidden";


        window.setTimeout(function () {

            if (deleteModalClose) {
                deleteModalClose.focus();
            }

        }, 50);

    }


    function closeDeleteModal() {

        if (!deleteModal) {
            return;
        }

        deleteModal.hidden = true;

        document.body.style.overflow = "";


        if (lastFocusedDeleteButton) {

            lastFocusedDeleteButton.focus();

            lastFocusedDeleteButton = null;

        }

    }


    document.querySelectorAll(".delete-trigger").forEach(function (button) {

        button.addEventListener(
            "click",
            function () {
                openDeleteModal(button);
            }
        );

    });


    if (deleteModalClose) {
        deleteModalClose.addEventListener(
            "click",
            closeDeleteModal
        );
    }


    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener(
            "click",
            closeDeleteModal
        );
    }


    if (deleteModal) {

        deleteModal.addEventListener(
            "click",
            function (event) {

                if (event.target === deleteModal) {
                    closeDeleteModal();
                }

            }
        );

    }


    /* =========================================
       DELIVERY MODAL
    ========================================= */

    const deliveryModal =
        document.getElementById("deliveryModal");

    const deliveryModalClose =
        document.getElementById("deliveryModalClose");

    const cancelDeliveryButton =
        document.getElementById("cancelDeliveryButton");

    const continueDeliveryButton =
        document.getElementById("continueDeliveryButton");

    const deliveryCustomer =
        document.getElementById("deliveryCustomer");

    const deliveryAvatar =
        document.getElementById("deliveryAvatar");

    let selectedDeliveryCustomer = "";


    function openDeliveryModal(button) {

        if (!deliveryModal || !button) {
            return;
        }


        selectedDeliveryCustomer =
            button.getAttribute(
                "data-customer"
            ) || "";


        if (deliveryCustomer) {
            deliveryCustomer.textContent =
                selectedDeliveryCustomer;
        }


        if (deliveryAvatar) {
            deliveryAvatar.textContent =
                generateInitials(
                    selectedDeliveryCustomer
                );
        }


        deliveryModal.hidden = false;

        document.body.style.overflow = "hidden";


        window.setTimeout(function () {

            if (continueDeliveryButton) {
                continueDeliveryButton.focus();
            }

        }, 50);

    }


    function closeDeliveryModal() {

        if (!deliveryModal) {
            return;
        }

        deliveryModal.hidden = true;

        document.body.style.overflow = "";

        selectedDeliveryCustomer = "";

    }


    document.querySelectorAll(".delivery-trigger").forEach(function (button) {

        button.addEventListener(
            "click",
            function () {
                openDeliveryModal(button);
            }
        );

    });


    if (deliveryModalClose) {
        deliveryModalClose.addEventListener(
            "click",
            closeDeliveryModal
        );
    }


    if (cancelDeliveryButton) {
        cancelDeliveryButton.addEventListener(
            "click",
            closeDeliveryModal
        );
    }


    if (deliveryModal) {

        deliveryModal.addEventListener(
            "click",
            function (event) {

                if (event.target === deliveryModal) {
                    closeDeliveryModal();
                }

            }
        );

    }


    /* =========================================
       EXISTING DELIVERY FUNCTIONALITY
       PRESERVED FROM ORIGINAL TEMPLATE
    ========================================= */

    if (continueDeliveryButton) {

        continueDeliveryButton.addEventListener(
            "click",
            function () {

                if (!selectedDeliveryCustomer) {
                    return;
                }


                window.location.href =
                    "/delivery-records-page?customer=" +
                    encodeURIComponent(
                        selectedDeliveryCustomer
                    );

            }
        );

    }


    /* =========================================
       ESCAPE KEY
    ========================================= */

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key !== "Escape") {
                return;
            }


            if (
                deleteModal &&
                !deleteModal.hidden
            ) {
                closeDeleteModal();
                return;
            }


            if (
                deliveryModal &&
                !deliveryModal.hidden
            ) {
                closeDeliveryModal();
                return;
            }


            if (
                sidebar &&
                sidebar.classList.contains("open")
            ) {
                closeSidebar();
            }

        }
    );


    /* =========================================
       PREVENT MODAL FORM DOUBLE SUBMISSION
    ========================================= */

    if (deleteModalForm) {

        deleteModalForm.addEventListener(
            "submit",
            function () {

                const button =
                    deleteModalForm.querySelector(
                        "button[type='submit']"
                    );

                if (!button) {
                    return;
                }

                button.disabled = true;

                button.style.opacity = "0.7";

            }
        );

    }


});