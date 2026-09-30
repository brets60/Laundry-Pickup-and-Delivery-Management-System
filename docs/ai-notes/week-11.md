# Week 11 AI Disclosure & Production Deployment Log
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Week:** Week 11 — Fix, Clean Up & Ship  
**Target Milestone:** Deliverable 4 (QA, Deployment & Final Defense Readiness, 30%)  
**Date:** October 2026  
**Repository Branch:** `main`  
**Team (5 Members):**  
- John Michael Bretaña (Manager / Lead Architect)  
- Hazil Enoc (Store Cashier)  
- Marvin Oclarino (Delivery Driver — Van 1)  
- Tristan Dave M. Plaza (Delivery Driver — Motorcycle 1)  
- Mark Ephraim Nicor (Laundry Operator)  

---

## 1. Executive Summary
Week 11 marks the transition from local development to production readiness (*"Today your app leaves your laptop"*). Building upon the comprehensive feature freeze and bug hunting conducted in Week 10, the team executed five critical deployment objectives:
1. **Squashed All Triaged Bugs:** Resolved BUG-001 (Stored XSS tag stripping), BUG-002 (uncapped weight ceiling), BUG-003 (historical pickup dates), and BUG-004 (Escape key modal closer).
2. **Paid Down Technical Debt:** Centralized duplicated `is_async_request()` and input sanitization routines across all 6 controllers into `controllers/utils.py`.
3. **Environment & Security Decoupling:** Migrated application configurations to environment variables, authored `.env.example`, protected `.gitignore` against accidental secret commits, and enforced `APP_DEBUG=False` in production.
4. **Cloud Host Provisioning:** Packaged the application for production WSGI concurrency with `gunicorn`, authored `Procfile` and `render.yaml`, and verified automated cold-boot database schema initialization.
5. **Live Production Smoke Testing:** Verified both happy path CRUD workflows and HTTP 422 adversarial failure paths on the live production instance at [`https://laundrycare-management.onrender.com`](https://laundrycare-management.onrender.com).
6. **Automated Regression Suite:** All **78 automated tests are passing (100% green)**.

---

## 2. Prompts Used & Interaction Log (AI Disclosure)

In Week 11, AI was utilized as an engineering pair-programmer under strict human code review to assist in bug reproduction, refactoring, and deployment configuration:

### Task 1: Bug Squash & Input Sanitization
- **Prompt:**
  > *"How do we implement high-performance, robust HTML/XSS tag stripping in Python that completely eliminates `<script>` and `<style>` blocks (including interior executable JavaScript) from customer inputs before saving to SQLite?"*
- **AI Output:**
  Suggested regex replacement using `re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text, flags=re.IGNORECASE | re.DOTALL)`.
- **Human Review & Refinement:**
  Integrated the function into `controllers/utils.py` as `strip_html_tags()`. Applied it across `controllers/customer_portal_routes.py` for `name`, `address_details`, and `notes`. Authored regression test in `tests/test_adversarial_qa.py` verifying that payload `<script>alert('pwned')</script>Please handle with care` strips cleanly to `"Please handle with care"`.
- **Author:** Tristan Dave M. Plaza (`tristandaveplaza422@gmail.com`)

---

### Task 2: Weight Ceiling & Technical Debt Refactoring
- **Prompt:**
  > *"We noticed `is_async_request()` is duplicated across 6 controllers. What is the cleanest way to centralize this in Flask while adding an upper bound weight ceiling of 150 kg on orders with a descriptive 422 error?"*
- **AI Output:**
  Recommended creating `controllers/utils.py` and updating domain controllers to import `is_async_request`. Provided validation snippet for `0 < weight <= 150.0`.
- **Human Review & Refinement:**
  Implemented `0 < weight <= 150.0 kg` in both `manage_orders` and `edit_order` inside `controllers/order_routes.py`. Refactored all 6 controllers (`customer_routes.py`, `order_routes.py`, `pickup_routes.py`, `delivery_routes.py`, `payment_routes.py`, and `app.py`) to import from `controllers.utils`. Verified that 78/78 tests remain green.
- **Authors:** Hazil Enoc (`hazilenoc1@gmail.com`) & John Michael Bretaña (`bretanajohnmichael@gmail.com`)

---

### Task 3: Environment Configuration & Debug Hardening
- **Prompt:**
  > *"Generate a comprehensive `.env.example` file and show how `app.py` should safely read `SECRET_KEY`, `DATABASE`, `FLASK_ENV`, and `APP_DEBUG` so that debug mode is strictly forced to False in production."*
- **AI Output:**
  Provided `.env.example` structure and Flask environment loading logic.
- **Human Review & Refinement:**
  Configured `app.py` to evaluate `FLASK_ENV == 'production'`, enforcing `app.debug = False`. Updated `.gitignore` to block `.env`, `.env.*`, and temporary test databases. Verified via CLI that `os.environ['FLASK_ENV']='production'` guarantees `app.debug is False`.
- **Author:** Mark Ephraim Nicor (`markephraimnicor418@gmail.com`)

---

### Task 4 & 5: Live Cloud Deployment & Smoke Test Matrix
- **Prompt:**
  > *"Create a production `Procfile` and `render.yaml` for a Flask application using Gunicorn with 2 workers, 4 threads, and an auto-migrating SQLite database, plus a structured smoke test plan for deployment.md."*
- **AI Output:**
  Provided `Procfile` syntax, Render blueprint specification, and smoke test format.
- **Human Review & Refinement:**
  Authored `Procfile` and `render.yaml`. Updated `requirements.txt` with `gunicorn>=21.2.0`. Created [`docs/deployment.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/deployment.md) documenting live URL (`https://laundrycare-management.onrender.com`), cloud architecture diagram, and executed happy path + HTTP 422 failure path smoke tests.
- **Authors:** Marvin Oclarino (`marvinoclarino09@gmail.com`) & John Michael Bretaña (`bretanajohnmichael@gmail.com`)

---

## 3. End-of-Lab Checklist (All Requirements Satisfied)

| Checklist Item | Status | Verification Evidence / Repository Reference |
|:---|:---:|:---|
| **1. P0/P1 bugs fixed via reviewed PRs; suite green** | **PASS ✅** | BUG-001 (XSS strip), BUG-002 (weight ceiling), BUG-003 (date min), BUG-004 (Escape key) squashed. **78/78 tests passing (100% green)** in [`tests/test_adversarial_qa.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_adversarial_qa.py). |
| **2. One or two debt items paid down** | **PASS ✅** | Centralized `is_async_request()` and `strip_html_tags()` into [`controllers/utils.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/utils.py), eliminating duplicated boilerplate across 6 controllers. |
| **3. Config in env vars; no secrets in repo; debug off in prod** | **PASS ✅** | Documented in [`.env.example`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/.env.example). [`.gitignore`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/.gitignore) protects secrets. [`app.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/app.py) forces `app.debug = False` when `FLASK_ENV=production`. |
| **4. App deployed; migrations run; live URL recorded** | **PASS ✅** | Deployed with [`Procfile`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/Procfile) & [`render.yaml`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/render.yaml). Database auto-initializes on startup via `init_database()`. Live URL recorded: [`https://laundrycare-management.onrender.com`](https://laundrycare-management.onrender.com). |
| **5. Live smoke test passed (happy + one failure path)** | **PASS ✅** | Full logs documented in [`docs/deployment.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/deployment.md) covering HP-01–HP-07 (Happy Path) and FP-01–FP-06 (Adversarial HTTP 422 failure path). |
| **6. Prompt logs current in /docs/ai-notes/week-11.md** | **PASS ✅** | Fully documented in Section 2 of this dossier with AI disclosures, prompts, and human code review records. |

---

## 4. Looking Ahead to Week 12 (Defense Readiness)
With Deliverable 4 preparation complete:
- The team is scheduled for **Week 12 Final Presentation & Live Demo** of the deployed application.
- Each member is prepared for an **unassisted oral defense** of their respective functional domains:
  - **John Michael Bretaña:** Lead architecture, role-based access control, session isolation, cloud hosting pipeline.
  - **Hazil Enoc:** Customer directory CRM, customer loyalty rewards engine, order intake validation.
  - **Marvin Oclarino:** Revenue channels, financial settlement split, cash change helper, 80mm thermal receipt generator.
  - **Tristan Dave M. Plaza:** Dispatch logistics, mobile touch signature pad, public tracking portal, XSS sanitization.
  - **Mark Ephraim Nicor:** Pickup conflict density detector, wash hub machine telemetry monitor, route time-slotting.
