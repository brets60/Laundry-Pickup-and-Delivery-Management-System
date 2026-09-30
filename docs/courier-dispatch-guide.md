# LaundryCare Courier Dispatch & Delivery Logistics Guide
**Author:** Tristan Dave M. Plaza (Delivery Driver — Motorcycle 1)  
**Role:** Field Courier Logistics & Express Doorstep Dispatch  
**System Module:** `/delivery-records-page` & `/track`  

---

## 1. Overview & Fleet Assignment
LaundryCare operates a two-tiered fleet to provide rapid turnaround across Maramag, Bukidnon:
- **Delivery Van 1 (Marvin Oclarino):** High-capacity transport for bulk commercial loads, heavy comforters, and wholesale clients.
- **Motorcycle 1 (Tristan Dave Plaza):** Agile courier unit optimized for rapid dormitory deliveries at Central Mindanao University (CMU), town center drop-offs, and express single-bag orders (<10 kg).

---

## 2. Dispatch Zones & Route Sequencing

Maramag service coverage is segmented into three primary logistical sectors:

| Delivery Zone | Target Landmarks | Typical Transit Time | Primary Unit |
|:---|:---|:---|:---|
| **CMU Campus / Musuan** | Men's & Women's Dormitories, Faculty Village, University Market | 8–12 mins | Motorcycle 1 |
| **Poblacion Maramag** | Sayre Highway commercial strip, Municipal Hall, Public Market | 5–8 mins | Motorcycle 1 / Van 1 |
| **Dologon & Base Camp** | Purok 1–5, Highway Junctions, Residential Subdivisions | 12–18 mins | Delivery Van 1 |

### Daily Dispatch Flow:
1. **08:30 AM — Fleet Inspection:** Check tire pressure, fuel, waterproof delivery carrier box, and mobile tablet battery.
2. **09:00 AM — Manifest Sync:** Access `/delivery-records-page` on mobile tablet or phone. Filter by `Scheduled` status and review stop sequencing.
3. **Print / Verify Slips:** Generate thermal delivery slips with Code128 tracking barcodes for all assigned parcels.

---

## 3. Proof of Delivery (POD) & Digital Signature Capture

To eliminate lost package claims:
1. **Physical Handover Checklist:**
   - Verify customer identity against the delivery record.
   - Count sealed garment bags in the client's presence.
   - Verify payment status (`Paid` or collect COD cash / GCash reference).
2. **Interactive Signature Pad:**
   - In `/delivery-records-page`, open the Delivery Slip modal (`#slipModal`).
   - Hand tablet or phone to customer to sign directly onto the HTML5 Canvas signature pad using finger or stylus.
   - Touch listeners automatically prevent screen scrolling during signature strokes.
   - Click **"Clear"** if the client wishes to redraw.
3. **Marking Delivery as Completed:**
   - Set status to `Delivered`. The live customer tracking portal (`/track`) updates instantly via reactive polling.

---

## 4. Inclement Weather & Safety Protocols

- During heavy Bukidnon rains, all folded garments must remain double-bagged inside heavy-gauge waterproof courier bags.
- If a CMU dormitory or Dologon dropoff location is unreachable due to road closures or severe weather, immediately contact the client via the WhatsApp or Phone quick-action button in the dashboard and update dispatch notes.
