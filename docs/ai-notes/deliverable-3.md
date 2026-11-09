# Deliverable 3 — AI Disclosure & Interface Binding Summary
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Milestone:** Deliverable 3 — Views, Components & Interface Binding (Weeks 6–8 · Phase 3)  
**Weight:** 30% · Due: End of Week 8  

---

## 1. Overview of AI Use in Phase 3 (Weeks 6–8)

During Deliverable 3, AI tooling was used as a frontend/backend integration assistant to:
1. Decompose the 24 application templates into 12 reusable UI components ([`docs/components.md`](../components.md)) and reachable wireframe states (`?state=empty`, `?state=loading`, `?state=error`).
2. Design dual-mode controllers (`controllers/*_routes.py`) and the client-side form interceptor (`static/js/form_bindings.js`) so forms submit asynchronously with loading states, duplicate-submit protection, and field-level HTTP `422` validation feedback.
3. Implement branded `404` and `500` error pages (`templates/404.html`, `templates/500.html`), accessible destructive-action confirmation modals, and humanized micro-copy ([`docs/feedback-matrix.md`](../feedback-matrix.md)).

---

## 2. Detailed Weekly Prompt & Defense Logs

- **Week 06 (Component Catalog & Reachable Wireframe States):** [`docs/ai-notes/week-06.md`](week-06.md)
- **Week 07 (Asynchronous Form Binding & 422 Field Errors):** [`docs/ai-notes/week-07.md`](week-07.md)
- **Week 08 (Global Error Handling, Destructive Modals & Micro-Copy):** [`docs/ai-notes/week-08.md`](week-08.md)
