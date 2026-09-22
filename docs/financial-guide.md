# LaundryCare Financial Settlement & End-of-Day Balancing Guide
**Author:** Marvin Oclarino (Delivery Driver & Financial Settlement Audit)  
**Role:** Driver Logistics (Van 1) & Cash Collection Reconciliation  
**System Module:** `/payments-page` & `/payments-page/export`  

---

## 1. Overview & Objectives
At LaundryCare Maramag, accurate cash flow tracking between field deliveries and the front desk ensures financial integrity. This Standard Operating Procedure (SOP) governs:
1. **Courier Field Collections (COD):** Collecting cash or verifying GCash payments at customer doorsteps.
2. **Channel Distribution Auditing:** Segregating revenue into Cash on Delivery, GCash/Maya QR, and Bank Transfers.
3. **Receipt Generation:** Issuing thermal receipts featuring electronic barcodes and transaction identifiers.
4. **End-of-Day (EOD) Settlement:** Balancing the delivery pouch against the digital journal before shifting handover.

---

## 2. Doorstep Cash on Delivery (COD) Workflow

When delivering laundry on Driver Van 1:
1. **Invoice Verification:** Review order price on the physical laundry bag tag against `/delivery-records-page`.
2. **Accepting Cash:**
   - Always count notes aloud in the presence of the client.
   - Calculate change accurately before completing handover.
3. **Digital GCash / Maya Payments:**
   - Present the official LaundryCare QR code mounted inside Van 1.
   - Verify the customer's payment screenshot on their smartphone.
   - Note down the **GCash Reference Number** (last 4 digits) for transaction reconciliation.
4. **Thermal Receipt Handover:**
   - Issue physical receipt with Code128 barcode or trigger electronic receipt confirmation via `/payments-page`.

---

## 3. Revenue Settlement Breakdown

The LaundryCare Financial Engine calculates channel distribution automatically:

| Payment Channel | Primary Settlement Channel | Reconciliation Target |
|:---|:---|:---|
| **Cash on Delivery (COD)** | Physical Cash Pouch | Counted daily and handed over to Cashier |
| **GCash / Maya QR** | Merchant Wallet / Mobile POS | Cross-referenced against digital GCash transaction logs |
| **Bank Transfer & Cards** | Landbank / BDO Business Account | Matched against bank statement credit confirmations |

---

## 4. End-of-Day (EOD) Cash Reconciliation Protocol

Every evening at 5:30 PM:
1. **Pull System Totals:** Open `/payments-page` and review the **Revenue Settlement Breakdown** widget.
2. **Physical Count:** Driver counts notes in the courier money pouch:
   - Count ₱1000, ₱500, ₱100, ₱50, and ₱20 bills separately.
3. **Reconcile with Cash Total:** Ensure physical cash matches `stats.cash_total`.
4. **Generate Ledger Export:**
   - Click **"Export CSV"** on the payments dashboard to download `laundrycare_payments_ledger.csv`.
   - Print or save the CSV report for monthly accounting records.
5. **Sign-off:** Cashier (Hazil Enoc) and Driver (Marvin Oclarino) verify the handover total and sign the EOD shift summary envelope.

---

## 5. Discrepancy & Refund Policy

- In the event of an overpayment, issue immediate cash change or record a customer credit note on their profile.
- If a delivery cannot be collected due to customer absence, mark order status as `Pending Collection` on the dispatch sheet; **never** mark as `Paid` without physical or verified electronic funds.
