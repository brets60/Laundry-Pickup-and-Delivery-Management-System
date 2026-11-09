# Component Architecture Specification (`docs/components.md`)

**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Phase:** Deliverable 3 — Interface & View Binding (Weeks 6–8 · Phase 3: AI ON)  
**Document:** `/docs/components.md`  

---

## 1. Executive Summary

This document specifies the component architecture for the **LaundryCare Management System**. It decomposes the system's Week 2 wireframes into 12 reusable, self-contained UI components and maps them across every screen (`index/list`, `detail`, `create`, `edit`) and every required UI state (`empty`, `loading`, `error`, `populated`) in accordance with the **Deliverable 3 Rubric**.

### Core Architecture Principles:
- **Reuse:** Build shared components (list rows, stat cards, badges, navbars, modals) once and reuse across all 5 modules.
- **State-Driven UI:** UI is a pure function of state (`data -> component -> rendered HTML`).
- **Required State Coverage:** Every list/index screen supports **Empty State** (`?state=empty` or 0 database rows), **Loading State** (`?state=loading` or pending async action), and **Error State** (`?state=error` or HTTP `422`/`404`/`500`/network failure) as reachable conditionals.
- **Semantic Structure:** Accessibility and semantic HTML (`<nav>`, `<header>`, `<main>`, `<section>`, `<table>`, `<form>`, `role="alert"`, `aria-busy="true"`) prioritized across all views.

---

## 2. Reusable Shared Components Catalog (with AI Attribution)

The system is decomposed into 12 core reusable components, each tagged as `AI-generated`, `AI-modified`, or `Hand-written`:

| Component ID | Component Name | AI Attribution | Owner | Description | Reusability Scope |
|---|---|:---:|---|---|---|
| `COMP-01` | **SidebarNav** | `AI-modified` | John Michael D. Bretaña | Fixed vertical navigation bar with brand icon, 8 module route links, RBAC visibility, active tab highlighting, and logged-in user footer. | All 19 Desktop Operations Views |
| `COMP-02` | **TopHeader** | `AI-modified` | John Michael D. Bretaña | Page title, breadcrumb, notification bell, account switcher, and primary action buttons. | All Management Views |
| `COMP-03` | **StatCard** | `AI-modified` | Tristan Dave M. Plaza | KPI metric card displaying numeric aggregates, trends, icon badge, and hover elevation. | Dashboard, Orders, Deliveries, Pickups, Customers, Staff, Payments |
| `COMP-04` | **FilterToolbar** | `Hand-written` | Tristan Dave M. Plaza | Real-time search input and interactive pill filter buttons (status, role, barangay zone, plus `?state=` preview pills). | Orders, Deliveries, Pickups, Customers, Staff, Payments, Rider App |
| `COMP-05` | **DataTable** | `AI-modified` | Mark Ephraim Nicor | Responsive data table with column headers, zebra row hover lifts, item actions (`View`, `Edit`, `Delete`), and row fade-out animation (`.row-fade-out`). | Orders, Deliveries, Pickups, Customers, Staff, Payments |
| `COMP-06` | **StatusBadge** | `Hand-written` | Mark Ephraim Nicor | High-contrast pill badge with color tokens and live breathing radar pulse indicators (`Received`, `In Wash`, `Out for Delivery`, `Delivered`, `Paid`). | All Views |
| `COMP-07` | **EmptyState** | `AI-generated` | Hazil Enoc | Centered SVG illustration, descriptive copy, and primary call-to-action button rendered when a module table has 0 records or `?state=empty`. | Orders, Deliveries, Pickups, Customers, Staff, Payments, Track |
| `COMP-08` | **LoadingSkeleton** | `AI-generated` | Hazil Enoc | Animated shimmer placeholder rows (`.skeleton-shimmer`) and button spinners (`.btn-spinner`) shown during data fetches and async form submissions (`?state=loading`). | Orders, Deliveries, Pickups, Customers, Payments, Dashboard |
| `COMP-09` | **ErrorAlert** | `AI-modified` | Hazil Enoc | Inline field error badges (`.field-error-text`), form banners (`.form-error-banner`), and table retry cards (`.error-table-state` via `?state=error`). | All Forms & Table Views |
| `COMP-10` | **ModalDialog** | `AI-modified` | Mark Ephraim Nicor | Accessible pop-up dialog for Create forms and Destructive Delete Confirmations (`#lcConfirmModal`) with backdrop blur and focus management. | Orders, Deliveries, Pickups, Customers, Staff, Payments |
| `COMP-11` | **ReceiptCard** | `Hand-written` | Marvin Oclarino | Printable customer invoice slip detailing order weight, service rates, barangay zone, and payment status. | Orders, Deliveries, Payments |
| `COMP-12` | **ProgressStepper** | `Hand-written` | Marvin Oclarino | Animated multi-step fulfillment progress line (`progress-bar-flow`) with pulsing status beacon circles. | Customer Tracker, Order Details, Delivery Details |

---

## 3. Screen-to-Component & State Mapping

Below is the exhaustive mapping connecting every screen (`index/list`, `detail`, `create`, `edit`) across all 5 modules to its constituent components, async bindings, and reachable states:

### A. Customer Module (`Owner: Hazil Enoc`)
| Screen | Route / Template | Composed Components | Async Binding | Reachable States |
|---|---|---|---|---|
| **Customer List** | `/customers-page` (`customers.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog` | `data-delete-url` on rows | Populated, Empty (`?state=empty`), Loading (`?state=loading`), Error (`?state=error`) |
| **Customer Details** | `/customers-page/details/:id` (`customer_details.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `DataTable`, `StatusBadge`, `ReceiptCard` | — | Populated, 404 Error (`404.html`) |
| **Create Customer** | In-page Modal on `/customers-page` & `POST /customers` | `ModalDialog`, `ErrorAlert`, `LoadingSkeleton` (`.btn-spinner`) | `data-async-form="customer-create"` | Idle, Pending/Loading (`Saving...`), 422 Inline Errors, 201 Success Toast |
| **Edit Customer** | `/customers-page/edit/:id` (`edit_customer.html`) & `PUT /customers/:id` | `SidebarNav`, `TopHeader`, `ErrorAlert`, `ModalDialog` (Delete confirm) | `data-async-form="customer-edit"` & `data-delete-url` | Pre-filled, Pending/Loading, 422 Inline Errors, 404 Not Found, 200 Success Toast |

### B. Laundry Orders Module (`Owner: John Michael D. Bretaña`)
| Screen | Route / Template | Composed Components | Async Binding | Reachable States |
|---|---|---|---|---|
| **Orders List** | `/laundry-orders-page` (`orders.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog` | `data-delete-url` on rows | Populated, Empty (`?state=empty`), Loading (`?state=loading`), Error (`?state=error`) |
| **Order Details** | `/laundry-orders-page/details/:id` (`order_details.html`) | `SidebarNav`, `TopHeader`, `ReceiptCard`, `StatusBadge`, `ProgressStepper` | — | Populated, Print Mode, 404 Error (`404.html`) |
| **Create Order** | In-page Modal on `/laundry-orders-page` & `POST /laundry-orders` | `ModalDialog`, `ErrorAlert`, `LoadingSkeleton` (`.btn-spinner`) | `data-async-form="order-create"` | Idle, Pending/Loading (`Saving...`), 422 Inline Errors, 201 Success Toast |
| **Edit Order** | `/laundry-orders-page/edit/:id` (`edit_order.html`) & `PUT /laundry-orders/:id` | `SidebarNav`, `TopHeader`, `ErrorAlert`, `ModalDialog` (Delete confirm) | `data-async-form="order-edit"` & `data-delete-url` | Pre-filled, Pending/Loading, 422 Inline Errors, 404 Not Found, 200 Success Toast |

### C. Pickup Schedules Module (`Owner: Mark Ephraim Nicor`)
| Screen | Route / Template | Composed Components | Async Binding | Reachable States |
|---|---|---|---|---|
| **Pickup Schedules List** | `/pickup-schedules-page` (`pickups.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog` | `data-delete-url` on rows | Populated, Empty (`?state=empty`), Loading (`?state=loading`), Error (`?state=error`) |
| **Pickup Details** | `/pickup-schedules-page/details/:id` (`pickup_details.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `StatusBadge` | — | Populated, 404 Error (`404.html`) |
| **Create Pickup** | In-page Modal on `/pickup-schedules-page` & `POST /pickup-schedules` | `ModalDialog`, `ErrorAlert`, `LoadingSkeleton` (`.btn-spinner`) | `data-async-form="pickup-create"` | Idle, Pending/Loading (`Saving...`), 422 Inline Errors, 201 Success Toast |
| **Edit Pickup** | `/pickup-schedules-page/edit/:id` (`edit_pickup.html`) & `PUT /pickup-schedules/:id` | `SidebarNav`, `TopHeader`, `ErrorAlert`, `ModalDialog` (Delete confirm) | `data-async-form="pickup-edit"` & `data-delete-url` | Pre-filled, Pending/Loading, 422 Inline Errors, 404 Not Found, 200 Success Toast |

### D. Delivery Records Module (`Owner: Tristan Dave M. Plaza`)
| Screen | Route / Template | Composed Components | Async Binding | Reachable States |
|---|---|---|---|---|
| **Delivery Records List** | `/delivery-records-page` (`deliveries.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar` (Zone filter), `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog` | `data-delete-url` on rows | Populated, Empty (`?state=empty`), Loading (`?state=loading`), Error (`?state=error`) |
| **Delivery Details** | `/delivery-records-page/details/:id` (`delivery_details.html`) | `SidebarNav`, `TopHeader`, `ProgressStepper`, `StatusBadge`, `ReceiptCard` | — | Populated, 404 Error (`404.html`) |
| **Create Delivery** | In-page Modal on `/delivery-records-page` & `POST /delivery-records` | `ModalDialog`, `ErrorAlert`, `LoadingSkeleton` (`.btn-spinner`) | `data-async-form="delivery-create"` | Idle, Pending/Loading (`Saving...`), 422 Inline Errors, 201 Success Toast |
| **Edit Delivery** | `/delivery-records-page/edit/:id` (`edit_delivery.html`) & `PUT /delivery-records/:id` | `SidebarNav`, `TopHeader`, `ErrorAlert`, `ModalDialog` (Delete confirm) | `data-async-form="delivery-edit"` & `data-delete-url` | Pre-filled, Pending/Loading, 422 Inline Errors, 404 Not Found, 200 Success Toast |

### E. Payment Module (`Owner: Marvin Oclarino`)
| Screen | Route / Template | Composed Components | Async Binding | Reachable States |
|---|---|---|---|---|
| **Payments List** | `/payments-page` (`payments.html`) | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog` | `data-delete-url` on rows | Populated, Empty (`?state=empty`), Loading (`?state=loading`), Error (`?state=error`) |
| **Payment Details / Receipt** | `/payments-page/details/:id` (`payment_details.html`) | `SidebarNav`, `TopHeader`, `ReceiptCard`, `StatusBadge` | — | Populated, Thermal Receipt Print, 404 Error (`404.html`) |
| **Create Payment** | In-page Modal on `/payments-page` & `POST /payments` | `ModalDialog`, `ErrorAlert`, `LoadingSkeleton` (`.btn-spinner`) | `data-async-form="payment-create"` | Idle, Pending/Loading (`Saving...`), 422 Inline Errors, 201 Success Toast |
| **Edit Payment** | `/payments-page/edit/:id` (`edit_payment.html`) & `PUT /payments/:id` | `SidebarNav`, `TopHeader`, `ErrorAlert`, `ModalDialog` (Delete confirm) | `data-async-form="payment-edit"` & `data-delete-url` | Pre-filled, Pending/Loading, 422 Inline Errors, 404 Not Found, 200 Success Toast |

---

## 4. Component Tree Hierarchy

```text
App Root
├── SidebarNav (COMP-01)
│   ├── BrandLogo
│   ├── NavLinks [8 items]
│   └── UserSessionFooter
└── MainContentArea
    ├── TopHeader (COMP-02)
    │   ├── Breadcrumb / Title
    │   ├── NotificationBell & AccountSwitcher
    │   └── ActionButtons
    ├── StatCardsGrid [4 items] (COMP-03)
    │   └── CounterValue [animated]
    ├── FilterToolbar (COMP-04)
    │   ├── SearchBox
    │   ├── PillToggles (Status / Barangay Zone)
    │   └── StatePreviewBar (?state=empty | ?state=loading | ?state=error)
    ├── StateConditionals
    │   ├── Case: Loading  --> LoadingSkeleton (COMP-08)
    │   ├── Case: Error    --> ErrorAlert (COMP-09)
    │   ├── Case: Empty    --> EmptyState (COMP-07)
    │   └── Case: Data     --> DataTable (COMP-05)
    │                           └── DataRow (repeating)
    │                               ├── CellData
    │                               ├── StatusBadge (COMP-06)
    │                               └── ActionButtons (View / Edit / Async Delete)
    └── Modals / Dialogs (COMP-10)
        ├── CreateRecordModal (data-async-form)
        ├── DestructiveConfirmModal (#lcConfirmModal)
        └── ReceiptSlipModal (COMP-11)
```

---

## 5. Team Member Component & Binding Ownership

| Team Member | Primary Module | Core Components & Bindings Owned |
|---|---|---|
| **John Michael D. Bretaña** | Laundry Orders & Core UI | `SidebarNav` (`COMP-01`), `TopHeader` (`COMP-02`), Orders Views (`orders.html`, `edit_order.html`, `order_details.html`), Global 404/500 Error Handlers |
| **Tristan Dave M. Plaza** | Delivery Records & Dispatch | `StatCard` (`COMP-03`), `FilterToolbar` (`COMP-04`), Delivery Views (`deliveries.html`, `edit_delivery.html`, `delivery_details.html`), `404.html`, `500.html` |
| **Mark Ephraim Nicor** | Pickup Schedules & UI Engine | `DataTable` (`COMP-05`), `StatusBadge` (`COMP-06`), `ModalDialog` (`COMP-10`), Pickup Views (`pickups.html`, `edit_pickup.html`, `pickup_details.html`), `form_bindings.js` |
| **Hazil Enoc** | Customers & State Conditionals | `EmptyState` (`COMP-07`), `LoadingSkeleton` (`COMP-08`), `ErrorAlert` (`COMP-09`), Customer Views (`customers.html`, `edit_customer.html`, `customer_details.html`), `animations.css` |
| **Marvin Oclarino** | Payments & Receipts | `ReceiptCard` (`COMP-11`), `ProgressStepper` (`COMP-12`), Payment Views (`payments.html`, `edit_payment.html`, `payment_details.html`), Failure-Path Tests (`test_error_handling.py`) |
