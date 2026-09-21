# Week 06 AI Disclosure & Technical Defense Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 06 — The View Layer & Component Architecture / Building Your Views  
**Date:** September 2026  
**Repository Branch:** `main`

---

## 1. Purpose of AI Use

During Week 06, our 5-member engineering team utilized AI tooling (Claude / ChatGPT / Antigravity) to assist with:
1. **Component Architectural Design:** Decomposing monolithic templates into a formal 12-component catalog (`docs/components.md`), establishing component hierarchy trees, and mapping screen-to-component dependencies.
2. **Reachable Wireframe State Engineering:** Implementing accessible, live wireframe states (`?state=empty`, `?state=loading`, `?state=error`, and populated default) across all 5 core operational views (`orders.html`, `deliveries.html`, `pickups.html`, `customers.html`, `payments.html`) via query string dispatch and Jinja2 conditionals.
3. **Skeleton Shimmer & Feedback States:** Scaffolding CSS shimmer animations and lightweight SVG empty/error illustrations in `static/css/animations.css`.

---

## 2. Prompts Used & Interaction Log

### Task 1: Component Catalog & Architecture (`docs/components.md`)
- **Prompt:**
  > *"Analyze our 24 views in LaundryCare (Orders, Deliveries, Pickups, Customers, Payments, Auth, Tracking) and propose a formal component catalog with 10-15 reusable UI components, defining their inputs, outputs, HTML/CSS structure, and parent/child hierarchy."*
- **AI Output:**
  Suggested 12 atomic/molecular components (`SidebarNav`, `TopHeader`, `StatCard`, `FilterToolbar`, `DataTable`, `StatusBadge`, `EmptyState`, `LoadingSkeleton`, `ErrorAlert`, `ModalDialog`, `ReceiptCard`, `ProgressStepper`).
- **Human Verification & Refinement:**
  Accepted the 12 components. Team mapped them explicitly across all 24 views and assigned direct ownership to the 5 team members to ensure balanced contribution.

---

### Task 2: Live Reachable Wireframe States (Empty, Loading, Error)
- **Prompt:**
  > *"How can we make wireframe states (Empty, Loading skeleton, and Error retry alert) directly reachable on live routes for grading and usability testing without clearing the production database?"*
- **AI Output:**
  Suggested inspecting `request.args.get('state')` in Jinja2 templates, rendering conditional `<tr><td colspan="...">` table state containers, and injecting an interactive `<div class="state-preview-bar">` with filter pills.
- **Human Verification & Refinement:**
  Implemented in `orders.html`, `deliveries.html`, `pickups.html`, `customers.html`, and `payments.html`. Ensured fallback to natural database state when no query parameter is provided, and retained real empty-state behavior when 0 database records exist.

---

### Task 3: Shimmer Animation & Feedback Polish
- **Prompt:**
  > *"Provide lightweight CSS keyframe animations for a loading skeleton shimmer and empty state SVG illustration that works with pure CSS without external UI frameworks."*
- **AI Output:**
  Provided `@keyframes shimmer` using `linear-gradient` and `.pulse-beacon` animation classes.
- **Human Verification & Refinement:**
  Merged into `static/css/animations.css` and verified cross-browser compatibility.

---

## 3. Component & Code Attribution Matrix

| Component / Artifact | File Location | Attribution Tag | Author / Maintainer | Description & Human Refinement |
|---|---|---|---|---|
| **Component Catalog** | `docs/components.md` | `AI-modified` | John Michael D. Bretaña | AI generated initial structure; Bretaña added screen mapping, hierarchy trees, and 5-member ownership matrix. |
| **Animation Engine** | `static/css/animations.css` | `AI-modified` | Tristan Dave Plaza | AI scaffolded `@keyframes shimmer`; Plaza added `.state-preview-bar`, `.state-pill`, and mobile media queries. |
| **Orders State Switcher** | `templates/orders.html` | `AI-modified` | John Michael D. Bretaña | AI suggested Jinja2 query inspection; Bretaña removed hardcoded demo rows and wired dynamic empty/loading/error states. |
| **Deliveries State Switcher** | `templates/deliveries.html` | `AI-modified` | Tristan Dave Plaza | Plaza integrated state switcher with active driver route timeline and zone badges. |
| **Pickups State Switcher** | `templates/pickups.html` | `AI-modified` | Mark Ephraim Nicor | Nicor wired state pills with collection batches and vehicle status cards. |
| **Customers State Switcher** | `templates/customers.html` | `AI-modified` | Hazil Enoc | Enoc upgraded plain text empty message to rich SVG card with VIP tier hooks. |
| **Payments State Switcher** | `templates/payments.html` | `AI-modified` | Marvin Oclarino | Oclarino connected transaction journal states and retry error fallbacks. |
| **Test Suite Verification** | `tests/test_*.py` | `Hand-written` | Team (Bretaña, Plaza, Nicor, Enoc, Oclarino) | 24 automated unit and integration tests verifying routing, authentication, RBAC, and CRUD operations. |

---

## 4. Technical Defense Preparation Cheat-Sheet

During lab defense and instructor evaluation, each team member can defend their component architecture and state implementations using the key technical answers below:

### 1. John Michael D. Bretaña (Project Lead — Orders Module & Overview)
- **Question:** *"How does the system dynamically switch between populated, empty, loading, and error states without reloading code?"*
- **Defense:**
  > *"We implemented query-driven state dispatch using Jinja2 `request.args.get('state')`. When a user or evaluator appends `?state=loading`, the template skips row rendering and displays our shimmer skeleton (`.loading-table-state`). Appending `?state=error` renders our `.error-table-state` with an HTTP 500 alert and retry link. When `?state=empty` is passed or when `orders` length is 0, the `.empty-table-state` SVG illustration renders with a CTA button to create the first order. In the absence of query params, real database records render seamlessly."*

---

### 2. Tristan Dave M. Plaza (Delivery Logistics & Courier Routes)
- **Question:** *"How is the Delivery module composed into reusable components?"*
- **Defense:**
  > *"The Delivery view decomposes into 6 core components: `TopHeader`, `StatCard` (tracking total, in-transit, delivered counts), `FilterToolbar` (combining search, delivery status pills, and Barangay Zone filters), `RouteTimeline` (the 4-stop fulfillment sequence), `DataTable` (`#deliveriesTable`), and `StatusBadge`. Reusable styles are isolated in `deliveries.css` and `animations.css`."*

---

### 3. Mark Ephraim Nicor (Pickup Scheduling & Logistics Clusters)
- **Question:** *"What prevents UI layout shifts when the Pickup table transitions between loading and populated states?"*
- **Defense:**
  > *"Our `.loading-table-state` uses a `<tr><td colspan='8'>` spanning container with matching height dimensions for 4 skeleton placeholder rows. Each skeleton row has a fixed height of `38px` and varied widths (100%, 94%, 97%) simulating realistic schedule entries, preventing layout reflow when real records load from SQLite."*

---

### 4. Hazil Enoc (Customer CRM & Client Directory)
- **Question:** *"How does the empty state improve usability over a blank table or generic 404?"*
- **Defense:**
  > *"According to Nielsen Norman UI guidelines, an empty state must inform, provide context, and prompt immediate user action. Instead of a blank table, our customer empty state displays a high-contrast user icon SVG, an informative headline ('No customer records found'), clarifying copy, and an interactive '+ Register First Customer' CTA button that immediately triggers the customer intake modal."*

---

### 5. Marvin Oclarino (Payments, COD Journal, & Receipts)
- **Question:** *"What is the fallback mechanism if the financial database fails or times out?"*
- **Defense:**
  > *"If a ledger timeout or database lock occurs, the error state renders a styled alert container (`.error-table-state`) with a 500 status indicator and an immediate '↺ Retry Payment Query' recovery action pointing back to `/payments-page`. This prevents uncaught server crashes from displaying raw stack traces to end-users."*

---

## 5. Summary of Compliance with Week 06 Rubric

- [x] **Task 1: Component Catalog** — Fully documented in `docs/components.md` with 12 reusable components, hierarchical relationships, screen mapping, and 5-member ownership.
- [x] **Task 2: Screen Composition** — All 5 core operational views refactored into modular components.
- [x] **Task 3: Reachable Wireframe States** — All 5 list views support `?state=empty`, `?state=loading`, `?state=error`, and default populated view with interactive pill switchers.
- [x] **Task 4: AI Disclosure & Prompt Log** — Complete transparency with prompts, tag matrix, and member technical defense notes documented herein.
- [x] **Task 5: Test Integrity** — 24/24 unit tests passing without regression.
