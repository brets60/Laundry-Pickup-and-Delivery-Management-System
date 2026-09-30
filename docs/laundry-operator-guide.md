# LaundryCare Wash Hub Operations & Sanitization SOP
**Author:** Mark Ephraim Nicor (Laundry Operator)  
**Role:** Wash Hub Plant Management, Machine Load Balancing & Quality Control  
**System Module:** `/pickup-schedules-page` & `/laundry-orders-page`  

---

## 1. Overview & Plant Responsibilities
At LaundryCare Maramag Hub, the Laundry Operator is the vital bridge between courier intake and clean delivery dispatch. Primary duties include:
1. **Intake Weigh-in & Inspection:** Verifying gross weight (kg) from incoming pickup sacks against order records.
2. **Fabric Sorting & Pre-Treatment:** Classifying items into Whites, Coloreds, Heavy Linens (bedsheets/blankets), and Delicates.
3. **Machine Capacity Balancing:** Maintaining optimal drum load (75–80% volume capacity) to ensure thorough agitation and spin hygiene.
4. **Dryer Cycle Supervision:** Preventing fabric shrinkage and managing static neutralization.
5. **Bagging & Handoff Staging:** Sealing clean laundry in tagged bags for delivery couriers (Marvin Oclarino & Tristan Dave Plaza).

---

## 2. Washing Machine Operational Matrix

| Cycle Type | Drum Load Target | Water Temp | Detergent Dosage | Spin Speed |
|:---|:---|:---|:---|:---|
| **Regular Wash & Fold** | 6.0 – 8.0 kg | Cold / 30°C | 60 ml Eco-Detergent | 1000 RPM |
| **Whites & Institutional** | 5.0 – 7.0 kg | Warm / 50°C | 80 ml Oxygen Bleach | 1200 RPM |
| **Heavy Beddings & Comforters** | Single large item | Warm / 40°C | 90 ml Heavy Formulation | 800 RPM |
| **Delicate / Silk Garments** | Under 4.0 kg | Cold / 20°C | 40 ml Mild pH-neutral | 600 RPM |

---

## 3. High-Density Slot & Courier Coordination

- In `/pickup-schedules-page`, the **Wash Hub Intake Monitor** updates real-time washer and dryer utilization (e.g. 4/6 washers active).
- When more than 4 pickups arrive within a single time slot (`09:00 AM - 12:00 PM` or `01:00 PM - 04:00 PM`), the automated conflict detector flags high volume so the operator can pre-allocate extra washer drums.

---

## 4. Packaging, Tagging & Ready-for-Delivery Handover

1. Once folded and inspected for cleanliness, bundle items according to standard folding dimensions.
2. Affix the thermal **Laundry Bag ID Tag** showing:
   - Order ID (`#ORD-XXXX`)
   - Customer Name & Barangay Zone
   - Verified Total Weight
3. Move sealed sacks to the **Dispatch Shelf** and update order status to `Ready for Delivery` in `/laundry-orders-page`.
