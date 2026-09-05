document.addEventListener("DOMContentLoaded", function () {

    /*
     * ==========================================
     * MOBILE SIDEBAR
     * ==========================================
     */

    const sidebar = document.getElementById("sidebar");
    const hamburgerButton = document.getElementById("hamburgerButton");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    function openSidebar() {

        if (!sidebar || !sidebarOverlay) {
            return;
        }

        sidebar.classList.add("open");
        sidebarOverlay.classList.add("show");

        if (hamburgerButton) {
            hamburgerButton.setAttribute("aria-expanded", "true");
        }
    }

    function closeSidebar() {

        if (!sidebar || !sidebarOverlay) {
            return;
        }

        sidebar.classList.remove("open");
        sidebarOverlay.classList.remove("show");

        if (hamburgerButton) {
            hamburgerButton.setAttribute("aria-expanded", "false");
        }
    }

    if (hamburgerButton) {

        hamburgerButton.addEventListener("click", function () {

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


    /*
     * Close mobile sidebar after navigation.
     */

    if (sidebar) {

        const navLinks = sidebar.querySelectorAll("a");

        navLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                if (window.innerWidth <= 760) {
                    closeSidebar();
                }

            });

        });

    }


    /*
     * ==========================================
     * NEW ORDER BUTTON
     * ==========================================
     */

    const newOrderButton = document.getElementById("newOrderButton");
    const emptyCreateButton = document.getElementById("emptyCreateButton");
    const orderFormCard = document.getElementById("orderFormCard");
    const customerInput = document.getElementById("customer");

    function focusOrderForm() {

        if (!orderFormCard) {
            return;
        }

        orderFormCard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

        setTimeout(function () {

            if (customerInput) {
                customerInput.focus();
            }

        }, 450);
    }

    if (newOrderButton) {
        newOrderButton.addEventListener("click", focusOrderForm);
    }

    if (emptyCreateButton) {
        emptyCreateButton.addEventListener("click", focusOrderForm);
    }


    /*
     * ==========================================
     * TOTAL WEIGHT
     * ==========================================
     */

    const totalWeightElement = document.getElementById("totalWeight");

    function calculateTotalWeight() {

        if (!totalWeightElement) {
            return;
        }

        const rows = document.querySelectorAll(".order-row");

        let total = 0;

        rows.forEach(function (row) {

            const weight = parseFloat(
                row.getAttribute("data-weight")
            );

            if (!Number.isNaN(weight)) {
                total += weight;
            }

        });

        totalWeightElement.textContent =
            total.toFixed(1) + " kg";
    }

    calculateTotalWeight();


    /*
     * ==========================================
     * ORDER SEARCH
     * ==========================================
     */

    const searchInput = document.getElementById("orderSearch");
    const clearSearchButton = document.getElementById("clearSearch");
    const clearSearchEmptyButton =
        document.getElementById("clearSearchEmpty");

    const searchEmptyState =
        document.getElementById("searchEmptyState");

    const visibleOrderCount =
        document.getElementById("visibleOrderCount");

    const orderRows =
        document.querySelectorAll(".order-row");


    function filterOrders() {

        if (!searchInput) {
            return;
        }

        const searchTerm =
            searchInput.value.trim().toLowerCase();

        let visibleCount = 0;

        orderRows.forEach(function (row) {

            const id =
                row.getAttribute("data-id") || "";

            const customer =
                row.getAttribute("data-customer") || "";

            const weight =
                row.getAttribute("data-weight") || "";

            const searchableText =
                (
                    id +
                    " " +
                    customer +
                    " " +
                    weight
                ).toLowerCase();

            const matches =
                searchableText.includes(searchTerm);

            if (matches) {

                row.style.display = "";
                visibleCount++;

            } else {

                row.style.display = "none";

            }

        });


        if (visibleOrderCount) {
            visibleOrderCount.textContent = visibleCount;
        }


        if (searchEmptyState) {

            if (searchTerm !== "" && visibleCount === 0) {

                searchEmptyState.hidden = false;

            } else {

                searchEmptyState.hidden = true;

            }

        }


        if (clearSearchButton) {

            clearSearchButton.style.display =
                searchTerm !== "" ? "flex" : "none";

        }

    }


    function clearSearch() {

        if (!searchInput) {
            return;
        }

        searchInput.value = "";

        filterOrders();

        searchInput.focus();
    }


    if (searchInput) {

        searchInput.addEventListener(
            "input",
            filterOrders
        );

    }

    if (clearSearchButton) {

        clearSearchButton.addEventListener(
            "click",
            clearSearch
        );

    }

    if (clearSearchEmptyButton) {

        clearSearchEmptyButton.addEventListener(
            "click",
            clearSearch
        );

    }


    /*
     * ==========================================
     * ADD ORDER VALIDATION
     * ==========================================
     */

    const orderForm =
        document.getElementById("orderForm");

    const weightInput =
        document.getElementById("laundry_weight");

    const customerError =
        document.getElementById("customerError");

    const weightError =
        document.getElementById("weightError");

    const submitOrderButton =
        document.getElementById("submitOrderButton");


    function showFieldError(
        input,
        errorElement,
        message
    ) {

        if (input) {
            input.closest(".form-group")
                .classList.add("has-error");
        }

        if (errorElement) {
            errorElement.textContent = message;
        }

    }


    function clearFieldError(
        input,
        errorElement
    ) {

        if (input) {
            input.closest(".form-group")
                .classList.remove("has-error");
        }

        if (errorElement) {
            errorElement.textContent = "";
        }

    }


    if (customerInput) {

        customerInput.addEventListener(
            "input",
            function () {

                if (customerInput.value.trim() !== "") {

                    clearFieldError(
                        customerInput,
                        customerError
                    );

                }

            }
        );

    }


    if (weightInput) {

        weightInput.addEventListener(
            "input",
            function () {

                const value =
                    parseFloat(weightInput.value);

                if (
                    !Number.isNaN(value) &&
                    value > 0
                ) {

                    clearFieldError(
                        weightInput,
                        weightError
                    );

                }

            }
        );

    }


    if (orderForm) {

        orderForm.addEventListener(
            "submit",
            function (event) {

                let valid = true;


                /*
                 * Customer validation
                 */

                const customer =
                    customerInput
                        ? customerInput.value.trim()
                        : "";

                if (customer === "") {

                    showFieldError(
                        customerInput,
                        customerError,
                        "Customer name is required."
                    );

                    valid = false;

                } else {

                    clearFieldError(
                        customerInput,
                        customerError
                    );

                }


                /*
                 * Weight validation
                 */

                const weight =
                    weightInput
                        ? parseFloat(weightInput.value)
                        : NaN;

                if (
                    Number.isNaN(weight) ||
                    weight <= 0
                ) {

                    showFieldError(
                        weightInput,
                        weightError,
                        "Laundry weight must be greater than 0 kg."
                    );

                    valid = false;

                } else {

                    clearFieldError(
                        weightInput,
                        weightError
                    );

                }


                if (!valid) {

                    event.preventDefault();

                    const firstError =
                        document.querySelector(
                            ".has-error input"
                        );

                    if (firstError) {
                        firstError.focus();
                    }

                    return;
                }


                /*
                 * Loading state.
                 *
                 * The form still submits normally
                 * to Flask.
                 */

                if (submitOrderButton) {

                    submitOrderButton.disabled = true;

                    submitOrderButton.innerHTML = `
                        <span class="spinner"></span>
                        <span class="button-text">
                            Adding Order...
                        </span>
                    `;

                }

            }
        );

    }


    /*
     * ==========================================
     * DELETE CONFIRMATION MODAL
     * ==========================================
     */

    const deleteModal =
        document.getElementById("deleteModal");

    const cancelDelete =
        document.getElementById("cancelDelete");

    const confirmDelete =
        document.getElementById("confirmDelete");

    const modalOrderId =
        document.getElementById("modalOrderId");

    const modalCustomer =
        document.getElementById("modalCustomer");

    const modalWeight =
        document.getElementById("modalWeight");

    let deleteFormToSubmit = null;


    function openDeleteModal(button) {

        if (!deleteModal) {
            return;
        }

        deleteFormToSubmit =
            button.closest(".delete-form");


        const orderId =
            button.getAttribute("data-order-id");

        const customer =
            button.getAttribute("data-customer");

        const weight =
            button.getAttribute("data-weight");


        if (modalOrderId) {
            modalOrderId.textContent =
                "#" + String(orderId).padStart(3, "0");
        }

        if (modalCustomer) {
            modalCustomer.textContent =
                customer || "Customer";
        }

        if (modalWeight) {
            modalWeight.textContent =
                (weight || "0") + " kg";
        }


        deleteModal.hidden = false;

        document.body.style.overflow = "hidden";


        setTimeout(function () {

            if (cancelDelete) {
                cancelDelete.focus();
            }

        }, 50);

    }


    function closeDeleteModal() {

        if (!deleteModal) {
            return;
        }

        deleteModal.hidden = true;

        document.body.style.overflow = "";

        deleteFormToSubmit = null;

    }


    const deleteButtons =
        document.querySelectorAll(".delete-button");

    deleteButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                openDeleteModal(button);

            }
        );

    });


    if (cancelDelete) {

        cancelDelete.addEventListener(
            "click",
            closeDeleteModal
        );

    }


    if (confirmDelete) {

        confirmDelete.addEventListener(
            "click",
            function () {

                if (!deleteFormToSubmit) {
                    return;
                }

                confirmDelete.disabled = true;

                confirmDelete.innerHTML = `
                    <span class="spinner"></span>
                    Deleting...
                `;

                /*
                 * Submit the ORIGINAL Flask form.
                 * No fake JavaScript deletion occurs.
                 */

                deleteFormToSubmit.submit();

            }
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


    /*
     * ESC key closes modal/sidebar.
     */

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

            }

            if (
                sidebar &&
                sidebar.classList.contains("open")
            ) {

                closeSidebar();

            }

        }
    );


    /*
     * ==========================================
     * FLASH ALERT CLOSE
     * ==========================================
     */

    const alertCloseButtons =
        document.querySelectorAll(".alert-close");

    alertCloseButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const alert =
                    button.closest(".flash-alert");

                if (!alert) {
                    return;
                }

                alert.style.opacity = "0";
                alert.style.transform = "translateY(-5px)";

                setTimeout(function () {

                    alert.remove();

                }, 200);

            }
        );

    });


    /*
     * ==========================================
     * RESPONSIVE SIDEBAR CLEANUP
     * ==========================================
     */

    window.addEventListener(
        "resize",
        function () {

            if (window.innerWidth > 760) {
                closeSidebar();
            }

        }
    );

});