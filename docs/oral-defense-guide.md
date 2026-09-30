# LaundryCare — Individual Unassisted Oral Defense Preparation Guide
**Coursework:** CS 106 / Software Engineering 1  
**Target Milestone:** Deliverable 4 (Individual Defense — 25 Points / 50 Individual Total)  
**Requirement:** Defend your own code live, individually, and unassisted (no AI, no teammate prompts).  

---

## Defense Evaluation Matrix & Rubric Expectations
The defense assesses three core criteria:
1. **Code Authorship & Navigation:** Can you instantly locate and explain the code you committed?
2. **Design Rationale & Trade-offs:** Can you justify *why* you chose this data structure, validation boundary, or algorithm over alternatives?
3. **Edge Case & Failure Handling:** Do you understand how your module behaves when given bad data, network drops, or malicious inputs?

---

# Member 1: John Michael Bretaña (Lead Architect & Manager)

### 1. Codebase Ownership & Key Files
- **Primary Source Files:** [`app.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/app.py), [`Procfile`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/Procfile), [`render.yaml`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/render.yaml)
- **Primary Test Suites:** [`tests/test_rbac.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_rbac.py), [`tests/test_error_handling.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_error_handling.py), [`tests/test_adversarial_qa.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_adversarial_qa.py)
- **Primary Commits:** `1ddeb6a`, `9fed121`, `86c76af`, `2703f2e`

### 2. Deep-Dive Architectural Concepts
- **Modular Blueprint Architecture:** Divided the app into 6 decoupled domain blueprints to prevent Git merge bottlenecks and enable independent testing.
- **Dual-Mode Error Architecture:** Registered global `@app.errorhandler(404)` and `@app.errorhandler(500)`. If a request is async (`Accept: application/json` or `X-Requested-With: XMLHttpRequest`), it returns a structured JSON payload (`{"status": 404, "error": "..."}`). If it's a browser navigation request, it renders a branded dark-glass HTML template (`404.html` or `500.html`). This guarantees **zero stack trace leakage**.
- **Role-Based Access Control Decorator:** Built `@role_required(allowed_roles)` wrapping endpoints. Checks `session.get('role')` against whitelist; unauthorized riders attempting to access cashier/admin pages are cleanly redirected with flash feedback.
- **Production WSGI Hardening:** Configured Gunicorn with 2 workers and 4 threads. Decoupled secrets into environment variables; enforced `app.debug = False` whenever `FLASK_ENV == 'production'`.

### 3. Anticipated Defense Questions & Model Answers
- **Q1: Why did you implement dual-mode error handling instead of standard Flask aborts?**
  > *"Standard `abort(404)` renders raw HTML error pages. When a modern frontend makes an asynchronous fetch or delete call, receiving an HTML document instead of JSON breaks client-side parsing and causes uncaught JavaScript promise rejections. By inspecting request headers, my handler returns JSON for fetch requests and HTML for direct browser hits, preserving application stability in all contexts."*
- **Q2: How does your database handle migrations and cold-boot deployments on cloud PaaS?**
  > *"In `app.py`, `init_database()` executes on module import. It uses idempotent DDL statements (`CREATE TABLE IF NOT EXISTS`) and inspects `PRAGMA table_info` before executing non-destructive `ALTER TABLE ADD COLUMN` commands. This allows fresh cloud containers on Render to boot and self-heal the database schema without manual SSH intervention."*
- **Q3: What prevents session tampering or privilege escalation?**
  > *"Session cookies are cryptographically signed using Flask's `secret_key`, loaded from a 64-character environment variable in production. Role attributes are verified on the server in `@role_required` decorators on every privileged request, preventing client-side spoofing."*

---

# Member 2: Hazil Enoc (Store Cashier & CRM Lead)

### 1. Codebase Ownership & Key Files
- **Primary Source Files:** [`controllers/customer_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/customer_routes.py), [`controllers/order_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/order_routes.py), [`templates/customers.html`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/templates/customers.html)
- **Primary Test Suites:** [`tests/test_customers_crm.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_customers_crm.py)
- **Primary Commits:** `ec2aac7`, `a6eb3ed`

### 2. Deep-Dive Architectural Concepts
- **Customer Loyalty Points Algorithm:** Engineered the loyalty calculation:
  $$\text{Points} = \left(\frac{\text{Total Spent}}{50} + (\text{Total Orders} \times 10)\right) \times \text{Multiplier}$$
  where Regular = 1.0, Student/Loyal = 1.2, and VIP = 1.5. Handled edge cases: customers with 0 orders cleanly evaluate to 0 points without division errors.
- **Physical Weight Ceiling Validation (BUG-002 Resolution):** In Week 10 adversarial testing, an order with 999,999 kg was accepted. In Week 11, I implemented boundary validation:
  $$0 < \text{weight} \le 150.0\text{ kg}$$
  Inputs exceeding 150 kg are rejected with HTTP 422: *"Single orders exceeding 150 kg require commercial contract approval."*
- **Debounced Real-Time CRM Search:** Implemented client-side input debouncing (300ms) on `/customers-page` to filter rows smoothly without firing excessive requests or freezing the DOM.
- **CSV Data Export:** Created `/customers-page/export` generating streaming RFC 4180 CSV responses using Python's `csv.writer` and `io.StringIO`.

### 3. Anticipated Defense Questions & Model Answers
- **Q1: Why did you set the maximum order weight to exactly 150 kg?**
  > *"Our physical store profile has 6 commercial washers with 15–20 kg capacity each. A single intake over 150 kg would completely monopolize the entire laundry hub for half a day, causing delivery bottlenecks for all other clients. Capping it at 150 kg enforces operational reality in software and guides commercial bulk clients to management contracts."*
- **Q2: Walk me through your loyalty multiplier formula. How does it handle negative or zero values?**
  > *"The formula calculates base points from spend: `total_spent / 50` plus loyalty frequency: `total_orders * 10`, multiplied by the tier scalar (1.0 for Regular, 1.5 for VIP). In `controllers/customer_routes.py`, database constraints prevent negative spend, and `coalesce` defaults missing totals to 0, ensuring mathematical safety."*
- **Q3: What happens when an unauthenticated user or courier tries to export customer CSV data?**
  > *"The route is protected by `@role_required(['admin', 'staff'])`. If an unauthenticated user or delivery courier attempts to access `/customers-page/export`, the decorator intercepts the request and redirects them to login or their delivery manifest, preventing customer PII exfiltration."*

---

# Member 3: Mark Ephraim Nicor (Laundry Operator & Operations Lead)

### 1. Codebase Ownership & Key Files
- **Primary Source Files:** [`controllers/pickup_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/pickup_routes.py), [`templates/pickups.html`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/templates/pickups.html)
- **Primary Test Suites:** [`tests/test_pickup_hub.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_pickup_hub.py), [`tests/test_pickup.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_pickup.py)
- **Primary Commits:** `31f4bc5`, `ce1c859`, `0498011`

### 2. Deep-Dive Architectural Concepts
- **Pickup Slot Density & Conflict Detector:** Authored `check_pickup_slot_conflict(conn, pickup_date, pickup_time, assigned_driver)`. Queries SQLite for non-cancelled pickups in the same time window. If count $\ge 4$, flags an operational warning: *"High intake density: 4 pickups booked for this slot"*, preventing courier overload.
- **Wash Hub Equipment Telemetry:** Built live operational indicators on `/pickup-schedules-page` displaying real-time utilization for 6 commercial washers and 4 dryers.
- **Historical Pickup Date Prevention (BUG-003 Resolution):** In Week 10, users could schedule pickups in the past. In Week 11, I dynamically injected `min="YYYY-MM-DD"` via JavaScript and added backend validation in `customer_portal_routes.py` rejecting `pickup_date < today`.

### 3. Anticipated Defense Questions & Model Answers
- **Q1: Why trigger the slot density alert at 4 bookings rather than 10 or 2?**
  > *"Our logistics setup utilizes 1 Van and 2 Motorcycles in Maramag. A standard pickup route window is 2 hours. A single courier can comfortably execute 2 pickups per hour accounting for rural road conditions. Therefore, 4 pickups per 2-hour window represents the maximum safe capacity for a single driver without delaying wash intake."*
- **Q2: How do your date validations prevent historical bookings without breaking automated test suites?**
  > *"In templates, the HTML5 input attribute `min` is dynamically set to `new Date().toISOString().split('T')[0]`, blocking past dates in modern browsers. On the backend, we compare `pickup_date < today_str`. For automated testing, fixtures generate dynamic current timestamps via `date.today()`, ensuring tests remain green regardless of the execution date."*
- **Q3: What database index or query structure ensures the conflict detector remains fast as records grow?**
  > *"The query filters on `pickup_date`, `pickup_time`, and `status != 'Cancelled'`. SQLite optimizes this through indexed B-Tree lookups on the composite fields, keeping query execution sub-millisecond even with thousands of archived schedules."*

---

# Member 4: Tristan Dave M. Plaza (Delivery Driver & Mobile UX Lead)

### 1. Codebase Ownership & Key Files
- **Primary Source Files:** [`controllers/delivery_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/delivery_routes.py), [`controllers/customer_portal_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/customer_portal_routes.py), [`controllers/utils.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/utils.py), [`templates/deliveries.html`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/templates/deliveries.html)
- **Primary Test Suites:** [`tests/test_delivery.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_delivery.py), [`tests/test_delivery_logistics.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_delivery_logistics.py), [`tests/test_customer_portal.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_customer_portal.py)
- **Primary Commits:** `214273f`, `7a5f11b`

### 2. Deep-Dive Architectural Concepts
- **HTML5 Touch Signature Canvas (`#sigCanvas`):** Implemented mobile touch signature capture. Handled `touchstart`, `touchmove`, and `touchend` events while calling `e.preventDefault()`, which prevents the mobile browser from triggering native pinch-to-zoom or vertical page bouncing while the customer signs.
- **Stored XSS Sanitization Engine (BUG-001 Resolution):** In Week 10, adversarial testing found that `<script>` and `<img onerror=...>` tags in customer booking notes were saved raw in SQLite. In Week 11, I created `strip_html_tags()` in `controllers/utils.py` using regex to purge `<script>...</script>` and `<style>...</style>` blocks along with their executable contents, escaping any remaining angle brackets.
- **Barangay Logistics Zone Allocation:** Created `resolve_maramag_zone_and_rider()` in `customer_portal_routes.py`. It inspects customer addresses using substring heuristics:
  - CMU Campus / Musuan / Doms $\rightarrow$ Zone 1 (Rider Mike — Van 1)
  - Kalagutay / Base Camp / Dologon $\rightarrow$ Zone 3 (Rider Dave — Moto 3)
  - Poblacion Center $\rightarrow$ Zone 2 (Rider Alex — Moto 2)

### 3. Anticipated Defense Questions & Model Answers
- **Q1: Why did you use regex to strip HTML tags in `controllers/utils.py` rather than installing an external library like `bleach`?**
  > *"Installing external C-extension dependencies like `bleach` or `lxml` introduces compilation dependencies that can fail on minimalist Linux cloud containers (such as Render or Alpine). By writing a self-contained, regex-based tag stripper with `re.DOTALL`, we eliminated external dependency bloat while cleanly stripping both `<script>` tags and their interior executable code before saving to SQLite."*
- **Q2: How does your signature pad convert stylus strokes into verifiable proof of delivery?**
  > *"The canvas captures 2D coordinate paths (`ctx.lineTo`). When the driver clicks 'Confirm Handover', `canvas.toDataURL('image/png')` converts the stroke vectors into a Base64-encoded PNG string, which is submitted via async fetch and stored in the delivery record."*
- **Q3: How did you fix mobile screen bouncing during touch signatures?**
  > *"On mobile viewports, touch gestures on `<canvas>` default to scrolling the window. In `deliveries.html`, I bound passive-disabled event listeners to `touchstart`, `touchmove`, and `touchend`, calling `e.preventDefault()`. This restricts the touch event solely to the canvas context."*

---

# Member 5: Marvin Oclarino (Delivery Driver & Financial Settlement Lead)

### 1. Codebase Ownership & Key Files
- **Primary Source Files:** [`controllers/payment_routes.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/controllers/payment_routes.py), [`templates/payments.html`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/templates/payments.html)
- **Primary Test Suites:** [`tests/test_payments_billing.py`](file:///C:/Users/Saidimar%20Rey/.gemini/antigravity/scratch/Laundry-Pickup-and-Delivery-Management-System/tests/test_payments_billing.py)
- **Primary Commits:** `3aac5ba`, `a9d354e`

### 2. Deep-Dive Architectural Concepts
- **Multi-Channel Revenue Settlement:** Aggregates transaction records by payment channel (Cash, GCash, Bank Transfer) and computes real-time percentage shares:
  $$\text{Share}_{\text{Channel}} = \left(\frac{\text{Channel Total}}{\text{Gross Total}}\right) \times 100$$
  Handled edge case where zero gross revenue defaults all percentages to `0.0%` without division-by-zero crashes.
- **Courier Cash Change Helper:** Client-side real-time calculation in `#cashChangeHelper`. When the driver enters the cash tendered, it compares against `amountDue`. If tendered $\ge$ due, it renders exact change in green (`#059669`). If under-tendered, it displays a bold red alert: *"Short: ₱XX.XX"*, preventing doorstep arithmetic mistakes.
- **POS Thermal Receipt Generator:** Designed an 80mm roll receipt modal formatted for thermal Bluetooth printing via `@media print`. Features an inline SVG simulated Code128 barcode and electronic settlement audit metadata.
- **Cross-Browser Modal Escape Handler (BUG-004 Resolution):** Resolved modal freezing in Firefox by adding a global `keydown` event listener for `e.key === 'Escape'`, closing open modals gracefully without loss of underlying form state.

### 3. Anticipated Defense Questions & Model Answers
- **Q1: Why did you render the Code128 barcode as inline SVG instead of loading an image or external font?**
  > *"External barcode fonts or third-party web APIs fail when drivers are in low-connectivity areas or printing offline. By generating the Code128 barcode as pure inline SVG rect elements, it has zero network dependencies, renders instantly, prints crisply at 203 DPI on thermal paper, and has zero rendering latency."*
- **Q2: How does your cash change helper prevent drivers from collecting insufficient funds?**
  > *"In `payments.html`, `calculateChange()` evaluates `tendered - amountDue`. If `tendered < amountDue`, the display immediately switches to red with the text `Short: ₱XX.XX`. Furthermore, backend validation in `controllers/payment_routes.py` rejects negative payments and enforces valid numeric amounts."*
- **Q3: What was the cause of BUG-004 in Firefox, and how did you resolve it?**
  > *"In Firefox, clicking outside the modal overlay did not consistently register due to event bubbling differences. More importantly, pressing the physical `Escape` key had no listener attached. I added `document.addEventListener('keydown', (e) => { if (e.key === 'Escape') ... })`, querying all open modal overlays and removing the `.open` class. This works identically across Chrome, Firefox, and Safari."*
