import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    # Color Palette
    COLOR_BG = RGBColor(248, 250, 252)        # Slate 50 (#F8FAFC)
    COLOR_PRIMARY = RGBColor(30, 58, 138)      # Blue 900 (#1E3A8A)
    COLOR_BLUE_ACCENT = RGBColor(37, 99, 235)  # Blue 600 (#2563EB)
    COLOR_TEAL_ACCENT = RGBColor(13, 148, 136) # Teal 600 (#0D9488)
    COLOR_GREEN = RGBColor(5, 150, 105)        # Emerald 600 (#059669)
    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)     # Slate 900 (#0F172A)
    COLOR_TEXT_MUTED = RGBColor(71, 85, 105)   # Slate 600 (#475569)
    COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)# Slate 200 (#E2E8F0)
    COLOR_LIGHT_BLUE = RGBColor(239, 246, 255) # Blue 50 (#EFF6FF)
    COLOR_LIGHT_GREEN = RGBColor(236, 253, 245)# Emerald 50 (#ECFDF5)

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_BG
        bg_shape.line.fill.background()
        return bg_shape

    def add_header(slide, title_text, category_text, presenter_text):
        header_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1)
        )
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
        header_box.line.color.rgb = COLOR_CARD_BORDER
        header_box.line.width = Pt(1)

        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.25)
        tf.margin_bottom = Inches(0.1)

        p_cat = tf.paragraphs[0]
        p_cat.text = f"{category_text.upper()}   •   PRESENTER: {presenter_text.upper()}"
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_BLUE_ACCENT

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN
        p_title.space_before = Pt(3)

    def add_card(slide, left, top, width, height, title, items, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, icon_text=""):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_right = Inches(0.25)
        tf.margin_bottom = Inches(0.2)

        p_title = tf.paragraphs[0]
        full_title = f"{icon_text}  {title}".strip() if icon_text else title
        p_title.text = full_title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_PRIMARY
        p_title.space_after = Pt(8)

        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"•  {item}"
            p_item.font.name = "Calibri"
            p_item.font.size = Pt(12)
            p_item.font.color.rgb = COLOR_TEXT_MUTED
            p_item.space_before = Pt(4)
            p_item.space_after = Pt(4)

        return card

    # =========================================================================
    # SLIDE 1 OF 5: TITLE & TEAM ROSTER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    s1_hero = s1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(2.2)
    )
    s1_hero.fill.solid()
    s1_hero.fill.fore_color.rgb = COLOR_PRIMARY
    s1_hero.line.fill.background()

    tf1 = s1_hero.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.4)
    tf1.margin_top = Inches(0.25)

    p1_sub = tf1.paragraphs[0]
    p1_sub.text = "CS 106 / SOFTWARE ENGINEERING 1  •  FINAL SYSTEM DEFENSE & LIVE DEMO"
    p1_sub.font.name = "Calibri"
    p1_sub.font.size = Pt(11)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = RGBColor(147, 197, 253)

    p1_h1 = tf1.add_paragraph()
    p1_h1.text = "LaundryCare Management System"
    p1_h1.font.name = "Arial"
    p1_h1.font.size = Pt(32)
    p1_h1.font.bold = True
    p1_h1.font.color.rgb = RGBColor(255, 255, 255)
    p1_h1.space_before = Pt(4)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "Automated Doorstep Laundry ERP & Sector-Based Logistics for Barangay Base Camp, Maramag, Bukidnon"
    p1_desc.font.name = "Calibri"
    p1_desc.font.size = Pt(14)
    p1_desc.font.color.rgb = RGBColor(224, 231, 255)
    p1_desc.space_before = Pt(4)

    # Team Roster Table / Card
    roster_box = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.95), Inches(7.5), Inches(4.0)
    )
    roster_box.fill.solid()
    roster_box.fill.fore_color.rgb = COLOR_CARD_BG
    roster_box.line.color.rgb = COLOR_CARD_BORDER
    roster_box.line.width = Pt(1.5)

    rtf = roster_box.text_frame
    rtf.word_wrap = True
    rtf.margin_left = Inches(0.3)
    rtf.margin_top = Inches(0.2)

    rtf_p0 = rtf.paragraphs[0]
    rtf_p0.text = "PROJECT TEAM & CODEBASE OWNERSHIP"
    rtf_p0.font.name = "Arial"
    rtf_p0.font.size = Pt(14)
    rtf_p0.font.bold = True
    rtf_p0.font.color.rgb = COLOR_PRIMARY
    rtf_p0.space_after = Pt(10)

    members = [
        ("John Michael Bretaña", "Lead Architect & Branch Manager", "Core Architecture, RBAC, Cloud Deployment"),
        ("Hazil Enoc", "Store Cashier & CRM Lead", "Customer Loyalty Engine, Digital Weighing & POS"),
        ("Mark Ephraim Nicor", "Laundry Operator & Courier 3", "Wash Hub Telemetry, Machine Densities & Zone 3"),
        ("Tristan Dave M. Plaza", "Mobile UX Lead & Courier 1", "Rider Mobile Web App, Touch Signature & Zone 1"),
        ("Marvin Oclarino", "Financial Lead & Courier 2", "Doorstep Change Calculator, Thermal POS & Zone 2"),
    ]

    for m_name, m_role, m_desc in members:
        p_m = rtf.add_paragraph()
        p_m.text = f"•  {m_name} — {m_role}"
        p_m.font.name = "Calibri"
        p_m.font.size = Pt(12)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_TEXT_MAIN

        p_sub = rtf.add_paragraph()
        p_sub.text = f"    Domain: {m_desc}"
        p_sub.font.name = "Calibri"
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_after = Pt(4)

    # Right Quality Badges Box
    right_box = s1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.55), Inches(2.95), Inches(3.98), Inches(4.0)
    )
    right_box.fill.solid()
    right_box.fill.fore_color.rgb = COLOR_LIGHT_BLUE
    right_box.line.color.rgb = RGBColor(191, 219, 254)
    right_box.line.width = Pt(1.5)

    qtf = right_box.text_frame
    qtf.word_wrap = True
    qtf.margin_left = Inches(0.25)
    qtf.margin_top = Inches(0.25)

    qp0 = qtf.paragraphs[0]
    qp0.text = "KEY PROJECT HIGHLIGHTS"
    qp0.font.name = "Arial"
    qp0.font.size = Pt(14)
    qp0.font.bold = True
    qp0.font.color.rgb = COLOR_PRIMARY
    qp0.space_after = Pt(10)

    highlights = [
        ("✅ 79 / 79 Passing Tests", "100% green automated Pytest test suite covering RBAC, arithmetic, and failure paths."),
        ("🌐 Live Cloud Deployment", "Hosted on Render PaaS (Linux Gunicorn WSGI) with offline local hot standby."),
        ("🛵 100% Bajaj Motorcycle Fleet", "Exclusively customized for Barangay Base Camp sectors with 3 dedicated riders."),
        ("✍️ Paperless Touch Signatures", "HTML5 Canvas touch signatures for verifiable proof of delivery.")
    ]

    for h_title, h_body in highlights:
        p_h = qtf.add_paragraph()
        p_h.text = h_title
        p_h.font.name = "Calibri"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_GREEN if "79" in h_title else COLOR_BLUE_ACCENT

        p_hb = qtf.add_paragraph()
        p_hb.text = h_body
        p_hb.font.name = "Calibri"
        p_hb.font.size = Pt(11)
        p_hb.font.color.rgb = COLOR_TEXT_MUTED
        p_hb.space_after = Pt(6)

    # =========================================================================
    # SLIDE 2 OF 5: THE CHALLENGE (PROBLEM DEFINITION)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Challenge: Operational Gaps in Traditional Laundry Shops", "Phase 1: Problem Definition", "Hazil Enoc (Store Cashier & CRM Lead)")

    w_col = Inches(2.78)
    h_col = Inches(5.1)
    top_col = Inches(1.75)
    gap = Inches(0.2)

    c1_x = Inches(0.8)
    c2_x = c1_x + w_col + gap
    c3_x = c2_x + w_col + gap
    c4_x = c3_x + w_col + gap

    add_card(s2, c1_x, top_col, w_col, h_col, "Lost Paper Slips & Tags", [
        "Physical paper receipts get torn, wet, or lost on the shop floor.",
        "Manual identification tags lead to misplaced garments and bag mix-ups.",
        "Zero permanent digital audit trail for customer service histories."
    ], icon_text="🏷️")

    add_card(s2, c2_x, top_col, w_col, h_col, "Customer Blindspots", [
        "Clients have zero visibility into washing and drying stages.",
        "Students and busy families repeatedly call staff asking if laundry is ready.",
        "No digital notifications when riders are en route for collection."
    ], icon_text="👀")

    add_card(s2, c3_x, top_col, w_col, h_col, "Uncoordinated Couriers", [
        "Riders receive unstructured phone calls with unclear landmarks.",
        "No sector planning leads to overlapping routes and wasted fuel.",
        "Peak intake hours overwhelm couriers without scheduling density checks."
    ], icon_text="🛵")

    add_card(s2, c4_x, top_col, w_col, h_col, "Doorstep Math Errors", [
        "Couriers mentally compute per-kilogram rates and cash change on the road.",
        "Cashier end-of-day reconciliation deficits from arithmetic mistakes.",
        "Lack of digital Proof of Delivery (POD) signatures causes disputes."
    ], icon_text="🧮")

    # =========================================================================
    # SLIDE 3 OF 5: THE SOLUTION & 3 UNIFIED PORTALS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "The LaundryCare Solution: 3 Unified Portals", "Phase 2: Solution Architecture", "Mark Ephraim Nicor (Laundry Operator & Courier 3)")

    w_card3 = Inches(3.77)
    h_card3 = Inches(5.1)
    gap3 = Inches(0.2)

    p1_x = Inches(0.8)
    p2_x = p1_x + w_card3 + gap3
    p3_x = p2_x + w_card3 + gap3

    add_card(s3, p1_x, top_col, w_card3, h_card3, "Public Customer Portal", [
        "Zero Login Required: Frictionless access for dormitory students and residents.",
        "60-Second Online Booking (/book-pickup): Sector-based pickup scheduling.",
        "Live Real-Time Tracker (/track): 5-step progress bar from intake to doorstep drop-off.",
        "Transparent Payments: Electronic GCash/Maya reference modal."
    ], icon_text="📱")

    add_card(s3, p2_x, top_col, w_card3, h_card3, "Cashier & Wash Operations", [
        "Customer CRM Directory (/customers-page): Lifetime spend & loyalty tier tracking.",
        "Digital Scale Intake (/laundry-orders-page): Auto-pricing calculation (Weight x Rate).",
        "Wash Hub Monitor (/pickup-schedules-page): Live capacity telemetry for 6 washers & 4 dryers.",
        "Payments & Settlement (/payments-page): Walk-in settlement & POS payment recording."
    ], icon_text="🧺")

    add_card(s3, p3_x, top_col, w_card3, h_card3, "Rider Mobile Web App", [
        "Field Courier Interface (/rider-app): Optimized for motorcycle smartphone mounts.",
        "1-Tap GPS Navigation: Direct shortcuts into Google Maps & Waze.",
        "Quick Client Calling: 1-tap phone dialer for arrival coordination.",
        "HTML5 Signature Canvas: Paperless touch signature handover."
    ], icon_text="🛵")

    # =========================================================================
    # SLIDE 4 OF 5: ENGINEERING INTEGRITY & TEST COVERAGE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Engineering Integrity: Architecture, RBAC & Test Evidence", "Phase 3: Software Engineering & QA", "Tristan Dave M. Plaza (Mobile UX Lead & Courier 1)")

    # Left: Architecture Card
    add_card(s4, Inches(0.8), top_col, Inches(5.76), Inches(5.1), "Modular System Architecture", [
        "Backend Framework: Python 3 + Flask using 6 decoupled domain Blueprints (Customer, Order, Pickup, Delivery, Payment, Portal).",
        "Merge Conflict Prevention: Team members worked on separate controllers concurrently without Git collisions.",
        "Database Architecture: SQLite 3 with enforced foreign keys (PRAGMA foreign_keys = ON) and automatic cold-start migrations.",
        "Dual-Mode Error Handler: Returns JSON for AJAX fetch calls and branded HTML for browser navigation (zero stack trace leakage).",
        "Role-Based Access Control: Decorator checks session roles (Admin, Staff, Rider) preventing privilege escalation."
    ], icon_text="🏗️")

    # Right: Adversarial Security & QA
    add_card(s4, Inches(6.76), top_col, Inches(5.77), Inches(5.1), "Adversarial Security & Test Evidence", [
        "Stored XSS Sanitization (BUG-001): Regex-based tag stripper (strip_html_tags()) purges <script> and <style> tags before database storage.",
        "Physical Capacity Ceiling (BUG-002): Caps single order weight at 150.0 kg. Oversized loads return HTTP 422 commercial warning.",
        "Historical Date Prevention (BUG-003): Dynamic min date attribute and server-side checks block bookings in the past.",
        "Modal Freezing Resolution (BUG-004): Universal Escape key event handler cleanly dismisses dialogs across all browsers.",
        "79 / 79 Passing Pytest Tests: 100% green suite validating RBAC, arithmetic precision, and adversarial boundary limits."
    ], icon_text="🛡️")

    # =========================================================================
    # SLIDE 5 OF 5: OPERATIONS & SYSTEM DEMONSTRATION WORKFLOW
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Motorcycle Logistics, POS Settlement & Live System Demo", "Phase 4: Operations & Live Demonstration", "Marvin Oclarino (Financial Settlement Lead & Courier 2)")

    # Left: Logistics Card
    add_card(s5, Inches(0.8), top_col, Inches(5.76), Inches(3.6), "Base Camp Bajaj Motorcycle Logistics", [
        "Exclusive Barangay Coverage: Central washing hub located at Base Camp Proper.",
        "Zone 1 (Proper & Commercial Junction): Dispatched to Tristan Dave Plaza (Bajaj Moto 1).",
        "Zone 2 (Sayre Highway Corridor & Strip): Dispatched to Marvin Oclarino (Bajaj Moto 2).",
        "Zone 3 (Puroks 1 to 5 Residential): Dispatched to Mark Ephraim Nicor (Bajaj Moto 3).",
        "Smart Sector Dispatch: Booking engine automatically resolves addresses into courier assignments."
    ], icon_text="🗺️")

    # Right: Financial POS Settlement
    add_card(s5, Inches(6.76), top_col, Inches(5.77), Inches(3.6), "Doorstep Financial POS & Contact Hub", [
        "Courier Cash Change Helper: Real-time calculation displays exact change in green or a bold red alert (Short: ₱XX.XX).",
        "80mm Thermal Bluetooth Print: POS receipt modal formatted for thermal paper with zero-dependency inline SVG Code128 barcode.",
        "Customer Hotline & Socials: Official Hotline 0906-188-8611 • Store Hours: 8:00 AM - 4:30 PM (Mon-Sat).",
        "Official Facebook Page: Direct integration to https://www.facebook.com/LaundryCare."
    ], icon_text="💳")

    # Bottom Demo Transition Banner
    demo_banner = s5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.3)
    )
    demo_banner.fill.solid()
    demo_banner.fill.fore_color.rgb = COLOR_LIGHT_GREEN
    demo_banner.line.color.rgb = RGBColor(167, 243, 208)
    demo_banner.line.width = Pt(1.5)

    dtf = demo_banner.text_frame
    dtf.word_wrap = True
    dtf.margin_left = Inches(0.3)
    dtf.margin_top = Inches(0.18)

    dp0 = dtf.paragraphs[0]
    dp0.text = "LIVE SYSTEM DEMONSTRATION WORKFLOW  •  TRANSITIONING TO APPLICATION"
    dp0.font.name = "Arial"
    dp0.font.size = Pt(13)
    dp0.font.bold = True
    dp0.font.color.rgb = COLOR_GREEN

    dp1 = dtf.add_paragraph()
    dp1.text = "Demo Steps: 1. Public 60s Booking (/book-pickup)  ➔  2. Scale Weighing & Pricing (/laundry-orders-page)  ➔  3. Wash Hub Telemetry (/pickup-schedules-page)  ➔  4. Customer Tracker (/track)  ➔  5. Mobile Courier Touch Signature (/rider-app)  ➔  6. Thermal POS Receipt & Payment Settlement (/payments-page)."
    dp1.font.name = "Calibri"
    dp1.font.size = Pt(11)
    dp1.font.color.rgb = COLOR_TEXT_MAIN
    dp1.space_before = Pt(3)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_dir = r"C:\Users\Saidimar Rey\.gemini\antigravity\scratch\Laundry-Pickup-and-Delivery-Management-System"
    out_file = os.path.join(out_dir, "LaundryCare_Presentation.pptx")
    create_deck(out_file)
