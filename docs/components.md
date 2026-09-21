# Component Architecture Specification

**Project:** Laundry Pickup and Delivery Management System  
**Phase:** Phase 3 — Interface Binding  
**Document:** `/docs/components.md`  
**Week:** Week 6 Lab Deliverable  

---

## 1. Executive Summary

This document specifies the component architecture for the **LaundryCare Management System**. It breaks down the system's Week 2 wireframes into reusable, self-contained UI components and maps them across all screens in accordance with the **Week 6 Lab Requirements**.

### Core Architecture Principles:
- **Reuse:** Build shared components (list rows, stat cards, badges, navbars) once and reuse across modules.
- **State-Driven UI:** UI is a pure function of state (`data -> component -> rendered HTML`).
- **Required State Coverage:** Every screen supports **Empty State**, **Loading State**, and **Error State** as reachable conditionals.
- **Semantic Structure:** Accessibility and semantic HTML (`<nav>`, `<header>`, `<main>`, `<section>`, `<table>`, `<form>`) prioritized over superficial styling.

---

## 2. Reusable Shared Components Catalog

The system is decomposed into 12 core reusable components:

| Component ID | Component Name | Description | Reusability Scope |
|---|---|---|---|
| `COMP-01` | **SidebarNav** | Fixed vertical navigation bar with brand icon, 8 module route links, active tab highlighting, and logged-in user footer. | All 19 Desktop Operations Views |
| `COMP-02` | **TopHeader** | Page title, subtitle, search bar, notification bell, and primary action buttons. | All Management Views |
| `COMP-03` | **StatCard** | KPI metric card displaying numeric aggregates, trends, icon badge, and hover elevation. | Dashboard, Orders, Deliveries, Pickups, Customers, Staff, Payments |
| `COMP-04` | **FilterToolbar** | Real-time search input and interactive pill filter buttons (status, role, barangay zone). | Orders, Deliveries, Pickups, Customers, Staff, Payments, Rider App |
| `COMP-05` | **DataTable** | Responsive data table with column headers, zebra row hover lifts, item actions, and pagination/counter. | Orders, Deliveries, Pickups, Customers, Staff, Payments |
| `COMP-06` | **StatusBadge** | High-contrast pill badge with color tokens and live breathing radar pulse indicators (Pending, In Transit, Delivered, Paid). | All Views |
| `COMP-07` | **EmptyState** | Centered icon illustration, descriptive text, and primary call-to-action button rendered when records list is empty. | Orders, Deliveries, Pickups, Customers, Staff, Payments, Track |
| `COMP-08` | **LoadingSkeleton** | Animated shimmer placeholders (`skeleton-shimmer`) shown while asynchronous data fetches occur. | Orders, Deliveries, Pickups, Customers, Payments, Dashboard |
| `COMP-09` | **ErrorAlert** | Dismissible notification banner rendering validation and server failure messages. | All Forms & Table Views |
| `COMP-10` | **ModalDialog** | Accessible pop-up dialog with overlay backdrop blur, header, form body, and submit/cancel actions. | Orders, Deliveries, Pickups, Customers, Staff, Payments |
| `COMP-11` | **ReceiptCard** | Printable customer invoice slip detailing order weight, service rates, barangay zone, and payment status. | Orders, Deliveries, Payments |
| `COMP-12` | **ProgressStepper** | Animated multi-step progress line (`progress-bar-flow`) with pulsing status beacon circles. | Customer Tracker, Delivery Details |

---

## 3. Screen-to-Component Mapping

Below is the exhaustive mapping connecting every screen to its constituent components:

### A. Customer Module (`Owner: John Michael D. Bretaña`)
| Screen | Route | Composed Components | Reachable States |
|---|---|---|---|
| Customer List | `/customers-page` | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ModalDialog` | Empty, Loading, Error, Populated |
| Customer Details | `/customers-page/details/:id` | `SidebarNav`, `TopHeader`, `StatCard`, `DataTable`, `StatusBadge`, `ReceiptCard` | Loading, Error, Populated |
| Add Customer Modal | In-page Modal / `/customers` | `ModalDialog`, `ErrorAlert` | Validation Error, Success |
| Edit Customer | `/customers-page/edit/:id` | `SidebarNav`, `TopHeader`, `ModalDialog`, `ErrorAlert` | Error, Populated |
| Public Welcome Home | `/welcome` | `TopHeader`, `StatusBadge`, `ProgressStepper`, Action Cards | Public Landing |
| Customer Booking | `/book-pickup` | `TopHeader`, Form Component, `StatusBadge`, `ErrorAlert` | Validation Error, Success |
| Customer Live Tracker | `/track` | `TopHeader`, Search Bar, `ProgressStepper`, `StatusBadge`, `EmptyState` | Empty, Loading, Found |

### B. Orders Module (`Owner: Tristan Dave M. Plaza`)
| Screen | Route | Composed Components | Reachable States |
|---|---|---|---|
| Orders List | `/laundry-orders-page` | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ModalDialog` | Empty, Loading, Error, Populated |
| Order Details | `/laundry-orders-page/details/:id` | `SidebarNav`, `TopHeader`, `ReceiptCard`, `StatusBadge`, `ProgressStepper` | Loading, Error, Populated |
| Create Order Modal | In-page Modal / `/laundry-orders` | `ModalDialog`, `ErrorAlert` | Validation Error, Success |
| Edit Order | `/laundry-orders-page/edit/:id` | `SidebarNav`, `TopHeader`, `ModalDialog`, `ErrorAlert` | Error, Populated |

### C. Pickup Module (`Owner: Mark Ephraim Nicor`)
| Screen | Route | Composed Components | Reachable States |
|---|---|---|---|
| Pickup Schedules | `/pickup-schedules-page` | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ModalDialog` | Empty, Loading, Error, Populated |
| Pickup Details | `/pickup-schedules-page/details/:id` | `SidebarNav`, `TopHeader`, `StatCard`, `StatusBadge` | Loading, Error, Populated |
| Schedule Pickup Modal| In-page Modal | `ModalDialog`, `ErrorAlert` | Validation Error, Success |
| Edit Pickup | `/pickup-schedules-page/edit/:id` | `SidebarNav`, `TopHeader`, `ModalDialog`, `ErrorAlert` | Error, Populated |

### D. Delivery Module (`Owner: Marvin Oclarino`)
| Screen | Route | Composed Components | Reachable States |
|---|---|---|---|
| Delivery Records | `/delivery-records-page` | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar` (Zone filter), `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ModalDialog` | Empty, Loading, Error, Populated |
| Delivery Details | `/delivery-records-page/details/:id` | `SidebarNav`, `TopHeader`, `ProgressStepper`, `StatusBadge`, `ReceiptCard` | Loading, Error, Populated |
| Dispatch Modal | In-page Modal | `ModalDialog`, `ErrorAlert` | Validation Error, Success |
| Edit Delivery | `/delivery-records-page/edit/:id` | `SidebarNav`, `TopHeader`, `ModalDialog`, `ErrorAlert` | Error, Populated |
| Rider Mobile Portal | `/rider-app` | Mobile Header, Shift Status Pulse, Task Cards, `StatusBadge`, `FilterToolbar` | Active Shift, Populated, Empty |

### E. Payment Module (`Owner: Hazil Enoc`)
| Screen | Route | Composed Components | Reachable States |
|---|---|---|---|
| Payments List | `/payments-page` | `SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ModalDialog` | Empty, Loading, Error, Populated |
| Payment Receipt | `/payments-page/details/:id` | `SidebarNav`, `TopHeader`, `ReceiptCard`, `StatusBadge` | Loading, Error, Populated |
| Record Payment Modal | In-page Modal | `ModalDialog`, `ErrorAlert` | Validation Error, Success |
| Edit Payment | `/payments-page/edit/:id` | `SidebarNav`, `TopHeader`, `ModalDialog`, `ErrorAlert` | Error, Populated |

---

## 4. Component Tree Hierarchy

```
App Root
├── SidebarNav (COMP-01)
│   ├── BrandLogo
│   ├── NavLinks [8 items]
│   └── UserSessionFooter
└── MainContentArea
    ├── TopHeader (COMP-02)
    │   ├── Breadcrumb / Title
    │   ├── SearchInput
    │   └── ActionButtons
    ├── StatCardsGrid [4 items] (COMP-03)
    │   └── CounterValue [animated]
    ├── FilterToolbar (COMP-04)
    │   ├── SearchBox
    │   └── PillToggles (Status / Zone)
    ├── StateConditionals
    │   ├── Case: Loading  --> LoadingSkeleton (COMP-08)
    │   ├── Case: Error    --> ErrorAlert (COMP-09)
    │   ├── Case: Empty    --> EmptyState (COMP-07)
    │   └── Case: Data     --> DataTable (COMP-05)
    │                           └── DataRow (repeating)
    │                               ├── CellData
    │                               ├── StatusBadge (COMP-06)
    │                               └── ActionButtons
    └── Modals / Dialogs (COMP-10)
        ├── CreateRecordModal
        ├── EditRecordModal
        └── ReceiptSlipModal (COMP-11)
```

---

## 5. Team Member Component Ownership

| Team Member | Primary Module | Core Components Owned & Defended |
|---|---|---|
| **John Michael D. Bretaña** | Customer & Core UI | `SidebarNav`, `TopHeader`, Customer Views, Master Animations (`animations.css`, `ui_interactions.js`) |
| **Tristan Dave M. Plaza** | Orders Module | Orders List, Order Details, `ReceiptCard`, Intake & Weight Calculation Components |
| **Mark Ephraim Nicor** | Pickup Module | Pickup Schedule List, Calendar Toolbar, Time Slot Selector, Reschedule Modal |
| **Marvin Oclarino** | Delivery & Rider App | Delivery Dispatch Table, Barangay Zone Filter Pills, Mobile Rider Task Card (`rider_mobile.html`) |
| **Hazil Enoc** | Payment Module | Payments Journal, Payment Method Badges (GCash/Cash), Payment Receipt Print Slip |

---

## 6. Verification and Testing

All components and views are covered by automated unit and integration tests:
- **Pytest Suite:** `tests/test_app.py`, `tests/test_customer_portal.py`, `tests/test_delivery.py`, `tests/test_pickup.py`, `tests/test_rbac.py`
- **Pass Rate:** **24/24 tests passing (100%)**
- **Semantic HTML & CSS:** All templates pass strict linting with unified 8-link sidebar navigation and responsive layout.
