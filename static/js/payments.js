/* =========================================================
   LAUNDRYCARE PAYMENTS JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ELEMENTS
    ====================================================== */

    const sidebar =
        document.getElementById("sidebar");

    const mobileOverlay =
        document.getElementById("mobileOverlay");

    const mobileMenuButton =
        document.getElementById("mobileMenuButton");

    const jumpToPaymentForm =
        document.getElementById("jumpToPaymentForm");

    const emptyRecordButton =
        document.getElementById("emptyRecordButton");

    const paymentFormSection =
        document.getElementById("paymentFormSection");

    const paymentForm =
        document.getElementById("paymentForm");

    const customerInput =
        document.getElementById("customer");

    const amountInput =
        document.getElementById("payment_amount");

    const methodInput =
        document.getElementById("payment_method");

    const receiptCustomer =
        document.getElementById("receiptCustomer");

    const receiptAmount =
        document.getElementById("receiptAmount");

    const receiptMethod =
        document.getElementById("receiptMethod");

    const receiptStatusText =
        document.getElementById("receiptStatusText");

    const recordPaymentButton =
        document.getElementById("recordPaymentButton");

    const transactionSearch =
        document.getElementById("transactionSearch");

    const clearSearch =
        document.getElementById("clearSearch");

    const searchEmpty =
        document.getElementById("searchEmpty");

    const paymentRows =
        document.querySelectorAll(".payment-row");

    const deleteForms =
        document.querySelectorAll(".delete-form");

    const deleteModal =
        document.getElementById("deleteModal");

    const modalClose =
        document.getElementById("modalClose");

    const cancelDelete =
        document.getElementById("cancelDelete");

    const confirmDelete =
        document.getElementById("confirmDelete");

    const modalPaymentId =
        document.getElementById("modalPaymentId");

    const modalCustomer =
        document.getElementById("modalCustomer");

    const modalAmount =
        document.getElementById("modalAmount");

    const paymentSuccessPopup =
        document.getElementById("paymentSuccessPopup");

    const successDoneButton =
        document.getElementById("successDoneButton");


    let pendingDeleteForm = null;


    /* =====================================================
       MOBILE SIDEBAR
    ====================================================== */

    function openSidebar() {

        if (!sidebar) return;

        sidebar.classList.add("open");

        if (mobileOverlay) {
            mobileOverlay.classList.add("show");
        }

        document.body.style.overflow = "hidden";
    }


    function closeSidebar() {

        if (!sidebar) return;

        sidebar.classList.remove("open");

        if (mobileOverlay) {
            mobileOverlay.classList.remove("show");
        }

        document.body.style.overflow = "";
    }


    if (mobileMenuButton) {

        mobileMenuButton.addEventListener(
            "click",
            openSidebar
        );

    }


    if (mobileOverlay) {

        mobileOverlay.addEventListener(
            "click",
            closeSidebar
        );

    }


    document.querySelectorAll(".sidebar a").forEach(
        function (link) {

            link.addEventListener(
                "click",
                function () {

                    if (
                        window.innerWidth <= 800
                    ) {
                        closeSidebar();
                    }

                }
            );

        }
    );


    /* =====================================================
       SCROLL TO PAYMENT FORM
    ====================================================== */

    function focusPaymentForm() {

        if (!paymentFormSection) return;

        paymentFormSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


        setTimeout(
            function () {

                if (
                    customerInput &&
                    !customerInput.readOnly
                ) {
                    customerInput.focus();
                }
                else if (amountInput) {
                    amountInput.focus();
                }

            },
            500
        );

    }


    if (jumpToPaymentForm) {

        jumpToPaymentForm.addEventListener(
            "click",
            focusPaymentForm
        );

    }


    if (emptyRecordButton) {

        emptyRecordButton.addEventListener(
            "click",
            focusPaymentForm
        );

    }


    /* =====================================================
       RECEIPT PREVIEW
    ====================================================== */

    function updateReceiptPreview() {

        if (!customerInput ||
            !amountInput ||
            !methodInput) {
            return;
        }


        const customer =
            customerInput.value.trim();

        const amount =
            parseFloat(amountInput.value);

        const method =
            methodInput.value;


        /* CUSTOMER */

        if (receiptCustomer) {

            receiptCustomer.textContent =
                customer || "Not entered";

        }


        /* PAYMENT METHOD */

        if (receiptMethod) {

            receiptMethod.textContent =
                method || "Not selected";

        }


        /* AMOUNT */

        if (
            !isNaN(amount) &&
            amount > 0
        ) {

            if (receiptAmount) {

                receiptAmount.textContent =
                    "₱" +
                    amount.toLocaleString(
                        "en-PH",
                        {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        }
                    );

            }

        }
        else {

            if (receiptAmount) {
                receiptAmount.textContent =
                    "₱0.00";
            }

        }


        /* STATUS */

        if (receiptStatusText) {

            if (
                customer &&
                !isNaN(amount) &&
                amount > 0 &&
                method
            ) {

                receiptStatusText.textContent =
                    "Information is ready for submission.";

            }
            else if (
                !isNaN(amount) &&
                amount <= 0 &&
                amountInput.value !== ""
            ) {

                receiptStatusText.textContent =
                    "Enter a valid amount to preview.";

            }
            else {

                receiptStatusText.textContent =
                    "Complete the payment form to preview the receipt.";

            }

        }

    }


    if (customerInput) {

        customerInput.addEventListener(
            "input",
            updateReceiptPreview
        );

    }


    if (amountInput) {

        amountInput.addEventListener(
            "input",
            updateReceiptPreview
        );

    }


    if (methodInput) {

        methodInput.addEventListener(
            "change",
            updateReceiptPreview
        );

    }


    updateReceiptPreview();


    /* =====================================================
       FORM VALIDATION
    ====================================================== */

    function showError(
        input,
        errorElement,
        message
    ) {

        if (!input || !errorElement) {
            return;
        }


        const group =
            input.closest(".form-group");


        if (group) {
            group.classList.add("input-error");
        }


        errorElement.textContent =
            message;

    }


    function clearError(
        input,
        errorElement
    ) {

        if (!input || !errorElement) {
            return;
        }


        const group =
            input.closest(".form-group");


        if (group) {
            group.classList.remove("input-error");
        }


        errorElement.textContent =
            "";

    }


    function validatePaymentForm() {

        let valid = true;


        const customerError =
            document.getElementById("customerError");

        const amountError =
            document.getElementById("amountError");

        const methodError =
            document.getElementById("methodError");


        /* CUSTOMER */

        if (
            customerInput &&
            !customerInput.value.trim()
        ) {

            showError(
                customerInput,
                customerError,
                "Customer name is required."
            );

            valid = false;

        }
        else {

            clearError(
                customerInput,
                customerError
            );

        }


        /* AMOUNT */

        const amount =
            amountInput
                ? parseFloat(amountInput.value)
                : NaN;


        if (
            !amountInput ||
            amountInput.value.trim() === ""
        ) {

            showError(
                amountInput,
                amountError,
                "Payment amount is required."
            );

            valid = false;

        }
        else if (
            isNaN(amount) ||
            amount <= 0
        ) {

            showError(
                amountInput,
                amountError,
                "Enter a valid payment amount."
            );

            valid = false;

        }
        else {

            clearError(
                amountInput,
                amountError
            );

        }


        /* METHOD */

        if (
            !methodInput ||
            !methodInput.value
        ) {

            showError(
                methodInput,
                methodError,
                "Please select a payment method."
            );

            valid = false;

        }
        else {

            clearError(
                methodInput,
                methodError
            );

        }


        return valid;

    }


    if (paymentForm) {

        paymentForm.addEventListener(
            "submit",
            function (event) {

                if (!validatePaymentForm()) {

                    event.preventDefault();

                    const firstError =
                        paymentForm.querySelector(
                            ".input-error input, .input-error select"
                        );

                    if (firstError) {
                        firstError.focus();
                    }

                    return;
                }


                /*
                    IMPORTANT:

                    The form continues to submit
                    normally to Flask.

                    JavaScript does NOT replace
                    the backend submission.
                */

                if (recordPaymentButton) {

                    recordPaymentButton.disabled =
                        true;

                    recordPaymentButton.classList.add(
                        "loading"
                    );

                    const buttonText =
                        recordPaymentButton.querySelector(
                            ".button-text"
                        );

                    if (buttonText) {

                        buttonText.textContent =
                            "Recording Payment...";

                    }

                }

            }
        );

    }


    /* =====================================================
       LIVE SEARCH
    ====================================================== */

    function performSearch() {

        if (!transactionSearch) {
            return;
        }


        const query =
            transactionSearch.value
                .trim()
                .toLowerCase();


        let visibleCount = 0;


        paymentRows.forEach(
            function (row) {

                const searchableText =
                    (
                        row.dataset.search ||
                        row.textContent ||
                        ""
                    )
                    .toLowerCase();


                const matches =
                    !query ||
                    searchableText.includes(query);


                row.style.display =
                    matches
                        ? ""
                        : "none";


                if (matches) {
                    visibleCount++;
                }

            }
        );


        if (clearSearch) {

            clearSearch.classList.toggle(
                "visible",
                query.length > 0
            );

        }


        if (searchEmpty) {

            searchEmpty.hidden =
                paymentRows.length === 0 ||
                visibleCount !== 0;

        }

    }


    if (transactionSearch) {

        transactionSearch.addEventListener(
            "input",
            performSearch
        );

    }


    if (clearSearch) {

        clearSearch.addEventListener(
            "click",
            function () {

                if (!transactionSearch) {
                    return;
                }

                transactionSearch.value = "";

                performSearch();

                transactionSearch.focus();

            }
        );

    }


    /* =====================================================
       DELETE MODAL
    ====================================================== */

    function openDeleteModal(form) {

        if (!deleteModal || !form) {
            return;
        }


        pendingDeleteForm =
            form;


        const paymentId =
            form.dataset.paymentId || "—";

        const customer =
            form.dataset.customer || "—";

        const amount =
            form.dataset.amount || "—";


        if (modalPaymentId) {

            modalPaymentId.textContent =
                "#" +
                String(paymentId).padStart(3, "0");

        }


        if (modalCustomer) {

            modalCustomer.textContent =
                customer;

        }


        if (modalAmount) {

            modalAmount.textContent =
                amount;

        }


        deleteModal.classList.add("show");

        deleteModal.setAttribute(
            "aria-hidden",
            "false"
        );


        document.body.style.overflow =
            "hidden";


        if (cancelDelete) {
            cancelDelete.focus();
        }

    }


    function closeDeleteModal() {

        if (!deleteModal) {
            return;
        }


        deleteModal.classList.remove(
            "show"
        );

        deleteModal.setAttribute(
            "aria-hidden",
            "true"
        );


        document.body.style.overflow =
            "";


        pendingDeleteForm =
            null;

    }


    deleteForms.forEach(
        function (form) {

            form.addEventListener(
                "submit",
                function (event) {

                    /*
                        Stop the immediate submission.

                        Flask remains responsible
                        for the actual deletion.
                    */

                    event.preventDefault();

                    openDeleteModal(form);

                }
            );

        }
    );


    if (modalClose) {

        modalClose.addEventListener(
            "click",
            closeDeleteModal
        );

    }


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

                if (!pendingDeleteForm) {
                    return;
                }


                /*
                    Submit the ORIGINAL FORM.

                    This keeps the existing Flask
                    POST delete route untouched.
                */

                const form =
                    pendingDeleteForm;


                pendingDeleteForm =
                    null;


                form.submit();

            }
        );

    }


    if (deleteModal) {

        deleteModal.addEventListener(
            "click",
            function (event) {

                if (
                    event.target ===
                    deleteModal
                ) {

                    closeDeleteModal();

                }

            }
        );

    }


    /* =====================================================
       ESCAPE KEY
    ====================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape"
            ) {

                if (
                    deleteModal &&
                    deleteModal.classList.contains("show")
                ) {

                    closeDeleteModal();

                }


                if (
                    paymentSuccessPopup &&
                    paymentSuccessPopup.classList.contains("show")
                ) {

                    closeSuccessPopup();

                }


                if (
                    window.innerWidth <= 800 &&
                    sidebar &&
                    sidebar.classList.contains("open")
                ) {

                    closeSidebar();

                }

            }

        }
    );


    /* =====================================================
       SUCCESS POPUP
    ====================================================== */

    function closeSuccessPopup() {

        if (!paymentSuccessPopup) {
            return;
        }


        paymentSuccessPopup.classList.remove(
            "show"
        );

        paymentSuccessPopup.setAttribute(
            "aria-hidden",
            "true"
        );


        document.body.style.overflow =
            "";

    }


    function showSuccessPopup() {

        if (!paymentSuccessPopup) {
            return;
        }


        paymentSuccessPopup.classList.add(
            "show"
        );

        paymentSuccessPopup.setAttribute(
            "aria-hidden",
            "false"
        );


        document.body.style.overflow =
            "hidden";


        if (successDoneButton) {
            successDoneButton.focus();
        }

    }


    if (successDoneButton) {

        successDoneButton.addEventListener(
            "click",
            closeSuccessPopup
        );

    }


    if (paymentSuccessPopup) {

        paymentSuccessPopup.addEventListener(
            "click",
            function (event) {

                if (
                    event.target ===
                    paymentSuccessPopup
                ) {

                    closeSuccessPopup();

                }

            }
        );

    }


    /*
        Preserve the existing behavior:

        Flask redirects with:

        ?success=1

        ONLY then is the success popup shown.
    */

    const urlParams =
        new URLSearchParams(
            window.location.search
        );


    const success =
        urlParams.get("success");


    if (success === "1") {

        showSuccessPopup();

    }


    /* =====================================================
       INITIAL SEARCH STATE
    ====================================================== */

    performSearch();

});