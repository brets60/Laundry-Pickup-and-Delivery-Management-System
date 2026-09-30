# Deliverable 4 AI Disclosure & Final Defense Dossier
**Coursework:** CS 106 / Software Engineering 1  
**Project:** Laundry Pickup and Delivery Management System (`LaundryCare`)  
**Sprint / Milestone:** Deliverable 4 — QA, Deployment & Final Presentation (Phase 4 Closeout)  
**Weight:** 30% · Due: End of Week 12  
**Date:** October 2026  
**Repository Branch:** `main`  
**Live Public Deployment:** [`https://laundrycare-management.onrender.com`](https://laundrycare-management.onrender.com)  

---

## 1. Executive Summary & Deliverable 4 Scope
Deliverable 4 marks the final capstone milestone of the course (*"Ship it and prove it"*). Spanning Weeks 9 through 12, this deliverable synthesizes:
1. **Cloud Deployment:** Live, public cloud web application running on Render with Gunicorn WSGI and self-initializing SQLite migrations.
2. **Quality Engineering:** Comprehensive 15-feature test matrix, 78 automated tests (100% green), and complete resolution of all triaged bugs (BUG-001–BUG-004).
3. **Professional Presentation:** Complete 10-slide deck outline, rehearsed speaker script, and live demo runbook in [`docs/presentation.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/presentation.md).
4. **Engineering Retrospective:** Candid, blameless reflection across all 12 weeks documented in [`docs/retrospective.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/retrospective.md).
5. **Unassisted Oral Defense Preparation:** Individual defense guides for all 5 team members in [`docs/oral-defense-guide.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/oral-defense-guide.md).

---

## 2. AI Disclosure & Prompt Interaction Log

In Deliverable 4, AI was utilized as an engineering pair-programmer for documentation synthesis, adversarial scenario validation, and presentation structure:

### Prompt Log 1: Retrospective Structuring & Technical Debt Review
- **Prompt:**
  > *"How should our software engineering team structure a professional, blameless retrospective in Markdown covering our 12-week build of a Flask/SQLite laundry delivery system, detailing wins, bottlenecks (like SQLite locking and manual QA), technical debt paid down, and deferred roadmap items?"*
- **AI Output:**
  Suggested an Agile post-mortem layout with Phase-by-Phase reviews, categorized wins, technical debt audits, and core engineering lessons.
- **Human Review & Refinement:**
  Infused the document with LaundryCare-specific operational context (e.g., Maramag geography, CMU student dorms, mobile touch signature challenges). Authored in [`docs/retrospective.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/retrospective.md).

---

### Prompt Log 2: Presentation Deck & Live Demo Runbook
- **Prompt:**
  > *"Create a 12-minute presentation plan following the exact sequence: Problem -> Solution -> Architecture -> Live Demo (Happy Path + Graceful 422 Failure) -> Lessons, with timed speaker notes for our 5 team members and an offline backup protocol to prevent demo crashes."*
- **AI Output:**
  Provided slide outline, speaker time allocations, and demo sequence.
- **Human Review & Refinement:**
  Added exact copy-paste test payloads for the live demo, and established a local hot-standby runbook (`python app.py`) with pre-rendered wireframe fallback slides to satisfy the rubric's backup requirement. Authored in [`docs/presentation.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/presentation.md).

---

### Prompt Log 3: Oral Defense Technical Probe Preparation
- **Prompt:**
  > *"Generate technical defense questions and structured answers for each of our 5 team members (John Michael Bretaña, Hazil Enoc, Marvin Oclarino, Tristan Dave M. Plaza, Mark Ephraim Nicor) focusing on code authorship, design rationale, and edge-case failure handling for our unassisted oral defense."*
- **AI Output:**
  Drafted sample examiner questions on error handling, weight validation, regex tag stripping, slot density algorithms, and SVG barcode generation.
- **Human Review & Refinement:**
  Verified that all code citations match exact line numbers and functions in the repository. Assembled individual cheat-sheets in [`docs/oral-defense-guide.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/oral-defense-guide.md).

---

## 3. Definition of Done Checklist (Deliverable 4 Rubric)

| Checklist Item | Status | Verification Evidence / Repository File Link |
|---|:---:|---|
| **App deployed and working at a live public URL; CRUD complete in production** | **PASS ✅** | Live at [`https://laundrycare-management.onrender.com`](https://laundrycare-management.onrender.com). Full CRUD verified in [`docs/deployment.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/deployment.md). |
| **Failures handled gracefully in production (bad data $\rightarrow$ visible error, not a crash)** | **PASS ✅** | Bad weights, missing fields, and XSS inputs return structured HTTP 422 or human alerts. Zero 500 crashes; documented in [`docs/deployment.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/deployment.md). |
| **Test matrix complete; automated suite passes; P0/P1 bugs resolved** | **PASS ✅** | 15-feature test matrix in [`docs/test-matrix.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/test-matrix.md); **78/78 tests passing (100% green)** in pytest; BUG-001–BUG-004 marked **RESOLVED ✅**. |
| **Professional deck + rehearsed live demo of deployed app (with backup)** | **PASS ✅** | Deck outline, speaker scripts, live demo runbook, and offline backup plan documented in [`docs/presentation.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/presentation.md). |
| **Retrospective documented** | **PASS ✅** | Candid, blameless 12-week retrospective documented in [`docs/retrospective.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/retrospective.md). |
| **Every member completed unassisted oral defense preparation** | **PASS ✅** | Individual defense cheat-sheets and Q&A guides compiled in [`docs/oral-defense-guide.md`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/docs/oral-defense-guide.md). |
| **Contributions visible on the board and in commits across whole term** | **PASS ✅** | All 5 team members have substantial commit history corroborated across all 4 deliverables. |

---

## 4. Final Contributor Attribution & Commit Summary

All team members have verifiable, auditable Git authorship across the repository:

| Contributor | Operational Role | Key Modules Owned | Commits Count |
|---|---|---|:---:|
| **John Michael Bretaña** | Lead Architect & Project Manager | Core App, Auth/RBAC, Cloud Hosting, Error Boundaries | 95+ |
| **Tristan Dave M. Plaza** | Delivery Driver & Mobile UX Lead | Signature Canvas, Route Zoning, XSS Sanitization | 28+ |
| **Mark Ephraim Nicor** | Laundry Operator & Hub Lead | Pickup Conflict Density, Machine Telemetry, Dates | 27+ |
| **Marvin Oclarino** | Delivery Driver & Finance Lead | Cash Change Helper, Revenue Breakdown, Thermal POS | 21+ |
| **Hazil Enoc** | Store Cashier & CRM Lead | Customer CRM, Loyalty Multiplier, Weight Bounds | 21+ |

---

## 5. Course Completion Statement
LaundryCare has successfully met all engineering requirements, automated test benchmarks, architectural specifications, and deployment milestones set forth in CS 106 / Software Engineering 1. The team stands fully prepared for the final oral defense and live application presentation.
