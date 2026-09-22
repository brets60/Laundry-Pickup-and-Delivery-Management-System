# LaundryCare Store Cashier SOP & CRM Guide
**Author:** Hazil Enoc (Store Cashier)  
**Role:** Customer Relationship Management (CRM) & Front Counter Operations  
**System Module:** `/customers-page` & `/customers-page/details/<id>`  

---

## 1. Overview & Operational Responsibilities
As the primary Store Cashier at LaundryCare Maramag Hub, the cashier is responsible for:
1. **Front-Counter Client Intake:** Registering walk-in and phone-in clients with accurate contact numbers and delivery addresses.
2. **Customer Tier Classification:** Assigning and reviewing membership tiers (Regular, Gold, VIP) to reward returning patrons.
3. **Loyalty Balance Auditing:** Checking customer reward points balance during checkout or drop-off.
4. **Data Exports:** Periodically generating customer contact directory CSVs for CRM SMS updates and offline backups.

---

## 2. Customer Registration Workflow

### Step-by-Step Intake:
1. Navigate to `/customers-page` from the sidebar navigation.
2. Click **"+ Add Customer"** button located at the top-right toolbar.
3. Enter required fields:
   - **Full Name:** Complete client name (e.g., *Juan Dela Cruz*).
   - **Phone Number:** Active 11-digit Philippine mobile number starting with `09` (e.g., `09171234567`).
   - **Email Address (Optional):** Used for automated receipt dispatch.
   - **Delivery Address:** Landmark, Barangay, or Purok in Maramag / CMU area.
   - **Membership Tier:** Defaults to `Regular`; upgrade to `Gold` (10+ visits) or `VIP` (corporate/frequent accounts).
4. Click **Save Customer**. Form submissions are protected by double-submit safeguards and provide instant inline feedback.

---

## 3. Loyalty & Rewards Program Structure

The LaundryCare CRM calculates loyalty points automatically based on lifetime order volume and membership tier:

| Membership Tier | Discount Benefit | Points Accrual Rate | Qualifying Criteria |
|:---|:---|:---|:---|
| **Regular** | Standard Rates | 1 pt per ₱50 spent + 10 pts/order | New accounts & occasional clients |
| **Gold** | 10% Off Services | 1.2x points multiplier | 10+ completed orders or ₱3,000+ spend |
| **VIP** | 15% Off Services | 1.5x points multiplier | 25+ completed orders or corporate contracts |

### Redeeming Points:
- Points can be redeemed at the front desk for service discounts (e.g., 50 points = ₱50 laundry discount).
- The Cashier can view points balance instantly via the **Cashier Loyalty Hub** on any customer profile (`/customers-page/details/<id>`).

---

## 4. Search, Filtering & Directory Export

- **Debounced Instant Search:** Typing in the search bar filters clients by name, contact number, or address with real-time feedback without page reloads.
- **Tier Quick Filters:** Click `All`, `Regular`, `VIP`, or `Gold` pill tabs to segment the directory instantly.
- **CSV Directory Export:** Click **"Export CSV"** in the top header to download `laundrycare_customers_directory.csv`. This file contains complete contact records formatted for Excel and accounting reconciliation.

---

## 5. Customer Support Quick Actions

When viewing client records from the directory table:
- **WhatsApp Direct:** Click the green WhatsApp icon to launch a pre-addressed chat with the customer for order ready notifications.
- **Direct Phone Dial:** Click the blue phone icon on mobile/tablet to initiate phone contact regarding laundry delivery availability.
