#!/usr/bin/env python3
"""KISAN-EDGE — SIH 2026 idea-submission deck (6 slides, official template)."""
import os
from sih_deck import *          # noqa: F403
from sih_deck import _p, _r     # underscore names are not re-exported by *
import sih_deck as D

PS_ID    = "26180"
PS_TITLE = ("A field-deployable AI-powered Smart Farming Assistant for early "
            "detection of crop disease, pests, nutrient deficiency and "
            "irrigation need, with resilience to drought, flood and heat waves")
THEME    = "Agriculture, FoodTech & Rural Development"
CATEGORY = "Hardware"
TEAM_ID  = "<Team ID>"
TEAM_NM  = "<Team Name>"

M   = IN(0.30)                  # side margin
CW  = SW - 2 * M                # content width
CY  = IN(1.12)                  # content top (below title rule)
CH  = D.FOOT_Y - CY - IN(0.10)  # content height


# ================================================================ slide 1 ====
def s1():
    o = []
    o.append(shape(0, 0, SW, SH, fill=WHITE))
    # soft green field band across the lower half
    o.append(shape(0, IN(4.55), SW, IN(1.80), fill=T_GREEN))
    o.append(shape(0, IN(4.55), SW, IN(0.05), fill=GREEN))
    o += chrome(1, 6)
    o.append(shape(M, IN(1.30), IN(0.10), IN(1.30), fill=GREEN))
    o.append(tb(IN(0.55), IN(1.22), IN(9.0), IN(0.46),
                _p(_r("SMART INDIA HACKATHON 2026", 1500, BLUE, b=True,
                      font=HEAD_FONT), bullet=None)))
    o.append(tb(IN(0.55), IN(1.66), IN(10.2), IN(1.05),
                _p(_r("KISAN-EDGE", 5400, TITLE, b=True, font=HEAD_FONT),
                   bullet=None)))
    o.append(tb(IN(0.60), IN(2.74), IN(10.6), IN(0.44),
                _p(_r("Offline Edge-AI Farming Assistant  —  it looks at "
                      "the leaf, reads the soil, and answers in the farmer's "
                      "language", 1350, GREEN, b=True), bullet=None)))
    # mandated identity strip
    rows = [
        ("Problem Statement ID", PS_ID),
        ("Theme", THEME),
        ("PS Category", CATEGORY),
        ("Team ID", TEAM_ID),
        ("Team Name (Registered on portal)", TEAM_NM),
    ]
    y = IN(4.78)
    o.append(tb(M + IN(0.06), IN(3.34), IN(12.4), IN(1.30),
                _p(_r("Problem Statement Title  ", 1000, NAVY, b=True) +
                   _r(PS_TITLE, 1000, INK), bullet=None, lnspc=98000)))
    bw = CW / 5.0
    for k, (lab, val) in enumerate(rows):
        x = M + k * bw
        o.append(shape(x + IN(0.05), y, bw - IN(0.14), IN(1.02),
                       prst="roundRect", adj=8000, fill=WHITE, line=GREEN,
                       lnw=9525, shadow=True))
        o.append(tb(x + IN(0.16), y + IN(0.08), bw - IN(0.36), IN(0.36),
                    _p(_r(lab.upper(), 750, GREY, b=True), align="ctr",
                       bullet=None, lnspc=88000), anchor="ctr"))
        o.append(tb(x + IN(0.14), y + IN(0.44), bw - IN(0.32), IN(0.50),
                    _p(_r(val, 1000, TITLE, b=True), align="ctr", bullet=None,
                       lnspc=90000), anchor="ctr"))
    return wrap(o)


# ================================================================ slide 2 ====
def s2():
    o = chrome(2, 6, "IDEA TITLE  —  KISAN-EDGE")
    cw = (CW - IN(0.30)) / 3.0
    ch = IN(3.02)
    y = CY + IN(0.02)
    o.append(card(M, y, cw, ch, "PROPOSED SOLUTION",
        ["Portable kit :: ESP32 node — soil moisture (VWC), air temp & RH, "
         "soil EC, IR leaf-temperature — paired over BLE",
         "Phone as the brain :: farmer photographs the leaf; an INT8 CNN runs "
         "on the Snapdragon NPU. No cloud, no data cost",
         "Fusion engine :: rules combine image class + sensor values + "
         "cached forecast into ONE action",
         "Spoken advisory :: Red / Yellow / Green card, read aloud in the "
         "local language",
         "4-6 sample points per field are aggregated into a single field "
         "verdict"],
        accent=GREEN, tint=T_GREEN, bsz=940, tight=True, icon="1"))
    o.append(card(M + cw + IN(0.15), y, cw, ch, "HOW IT SOLVES THE PROBLEM",
        ["Works with zero internet :: inference is local; cloud sync is "
         "optional and opportunistic",
         "Early, not late :: disease and deficiency caught at leaf stage; "
         "water stress caught at the depletion threshold",
         "Saves water :: irrigation fired on FAO-56 MAD and ETo x Kc, not on "
         "habit or guesswork",
         "Climate risk gates :: heat, frost, waterlogging and flood warnings "
         "from local sensors + IMD forecast",
         "Reaches everyone :: app push, then SMS, then automated voice call — "
         "a feature phone still gets the alert"],
        accent=NAVY, tint=T_BLUE, bsz=940, tight=True, icon="2"))
    o.append(card(M + 2 * (cw + IN(0.15)), y, cw, ch,
        "INNOVATION & UNIQUENESS",
        ["Fusion, not two apps :: vision and soil sensing collapse into a "
         "single recommendation",
         "Explainable :: every alert states What, Where, Action and the rules "
         "that fired",
         "Confidence gate :: a doubtful photo asks for a re-shot instead of "
         "guessing a disease",
         "Honest scope :: no fake N-P-K or pesticide-residue claims — only "
         "what the sensors can prove",
         "Low cost :: approx. Rs 3,000-4,000 kit + the farmer's own phone. "
         "No subscription"],
        accent=AMBER, tint=T_AMBER, bsz=940, tight=True, icon="3"))
    gy = y + ch + IN(0.16)
    rows = [("CAPABILITY", "Plantix", "Fasal", "CropIn", "KISAN-EDGE"),
            ("Leaf-image disease AI", "Yes", "No", "Satellite only", "Yes"),
            ("In-field soil / micro-climate sensors", "No", "Yes", "No", "Yes"),
            ("Full function without internet", "No", "No", "No", "Yes"),
            ("Irrigation decision for the farmer", "No", "Yes", "No", "Yes"),
            ("Cost to a small farmer", "Free, ad-driven", "Paid IoT",
             "Enterprise SaaS", "One-time kit")]
    g, _gh = grid(M, gy, CW, rows, [2.3, 1.0, 1.0, 1.2, 1.3], rh=0.265,
                  hsz=830, bsz=820, hdr_fill=NAVY, accent_col=0)
    o.append(g)
    return wrap(o)


# ================================================================ slide 3 ====
def s3():
    o = chrome(3, 6, "TECHNICAL APPROACH")
    lw = IN(4.24)
    o.append(card(M, CY, lw, IN(5.02), "TECHNOLOGIES TO BE USED",
        ["#Hardware (field kit)",
         "!ESP32-C3 MCU  |  capacitive soil-moisture probe  |  SHT31 air "
         "temp + RH  |  soil EC probe  |  MLX90614 IR leaf thermometer  |  "
         "18650 Li-ion + small solar panel  |  BLE 5.0 link",
         "#Edge AI",
         "!MobileNetV3 / EfficientNet-Lite classifier, PyTorch to TFLite, "
         "INT8 quantised and compiled with the Qualcomm AI Hub for the "
         "Snapdragon NPU. YOLOv8-n pest detector in Phase 2.",
         "#Application",
         "!Android (Kotlin), on-device SQLite log, Android TTS for Hindi / "
         "Marathi / Tamil, offline-first sync, SMS + IVR fallback",
         "#Decision layer",
         "!Deterministic if-else rule engine over YAML crop profiles — "
         "FAO-56 MAD depletion, ETo x Kc water need (Hargreaves-Samani), "
         "canopy-minus-air delta-T stress index",
         "#Data",
         "!PlantVillage (pre-train), PlantDoc + our own field photographs "
         "(fine-tune and honest field-only test split)"],
        accent=NAVY, tint=T_BLUE, hsz=1200, bsz=880, tight=True))
    rx = M + lw + IN(0.18)
    rw = SW - M - rx
    o.append(flow(rx, CY, rw, IN(0.62), [
        ("SAMPLE", "4-6 points"), ("CAPTURE", "leaf photo"),
        ("INFER", "NPU, offline"), ("FUSE", "image + sensors"),
        ("ADVISE", "voice + colour"), ("LOG", "sync later")],
        fill=GREEN, sz=880, ssz=700))
    ay = CY + IN(0.78)
    ah = IN(2.16)
    o.append(shape(rx, ay, rw, ah, prst="roundRect", adj=5000, fill="FBFDFB",
                   line=GREY, lnw=9525))
    o.append(tb(rx + IN(0.14), ay + IN(0.04), rw - IN(0.28), IN(0.28),
                _p(_r("SYSTEM ARCHITECTURE  —  Tier 1 (MVP, procurement-safe)",
                      880, TITLE, b=True), bullet=None)))
    bw = (rw - IN(1.30)) / 3.0
    by, bh = ay + IN(0.34), IN(1.70)
    o.append(card(rx + IN(0.12), by, bw, bh, "FIELD KIT",
        ["!Soil VWC, air temp + RH", "!Soil EC, IR leaf temp",
         "!ESP32-C3, solar + Li-ion", "!Timestamp + GPS tag"],
        accent=GREEN2, tint=T_GREEN, hsz=830, bsz=770, tight=True))
    o.append(card(rx + IN(0.12) + bw + IN(0.59), by, bw, bh,
        "SNAPDRAGON PHONE",
        ["!Camera capture + AR framing", "!INT8 CNN on the NPU",
         "!Rule engine + confidence gate", "!Vernacular voice UI"],
        accent=NAVY, tint=T_BLUE, hsz=830, bsz=770, tight=True))
    o.append(card(rx + IN(0.12) + 2 * (bw + IN(0.59)), by, bw, bh,
        "CO-OP DASHBOARD",
        ["!Optional, only when online", "!Farm heat-map of stress",
         "!Season trends, yield view", "!Device health + battery"],
        accent=GREY, tint=T_GREY, hsz=830, bsz=770, tight=True))
    for k, lab in enumerate(("BLE", "SYNC")):
        ax = rx + IN(0.16) + (k + 1) * bw + k * IN(0.59)
        o.append(shape(ax + IN(0.04), by + IN(0.66), IN(0.46), IN(0.30),
                       prst="rightArrow", fill=AMBER if k == 0 else GREY))
        o.append(tb(ax - IN(0.06), by + IN(0.36), IN(0.68), IN(0.26),
                    _p(_r(lab, 700, GREY, b=True), align="ctr", bullet=None)))
    my = ay + ah + IN(0.14)
    o.append(card(rx, my, rw, D.FOOT_Y - my - IN(0.12),
        "METHODOLOGY & PROCESS",
        ["Pre-train on PlantVillage, then fine-tune on PlantDoc plus our own "
         "field images; test only on unseen field photos",
         "Quantise to INT8, benchmark on the AI Hub, keep an NNAPI/CPU "
         "fallback so non-Snapdragon phones still run",
         "Freeze the Observation to Recommendation contract, then encode "
         "agronomy thresholds as versioned YAML crop profiles",
         "Field trial on 2 crops, compare advisory water use against the "
         "farmer's normal schedule",
         "Tier 2 (Phase 2): the same INT8 artefact runs unchanged on a "
         "Qualcomm Dragonwing RB3 Gen 2 always-on field node"],
        accent=GREEN, tint=T_GREEN, hsz=1100, bsz=870, tight=True))
    return wrap(o)


# ================================================================ slide 4 ====
def s4():
    o = chrome(4, 6, "FEASIBILITY AND VIABILITY")
    cw = (CW - IN(0.30)) / 3.0
    ch = IN(3.06)
    o.append(card(M, CY, cw, ch, "FEASIBILITY",
        ["Every part is off-the-shelf :: ESP32 boards and the four sensors "
         "are sold in India today; nothing needs fabrication",
         "No new phone needed :: the compute is the farmer's own Android "
         "handset, so hardware cost stays near Rs 3,000-4,000",
         "Datasets already exist and are licensed :: PlantVillage "
         "(CC BY-SA 3.0) and PlantDoc (CC BY 4.0)",
         "Toolchain is free :: PyTorch, TFLite and the Qualcomm AI Hub all "
         "have no-cost tiers",
         "MVP is a 6-8 week build for a 6-person team; the rule engine is "
         "deterministic, not research-grade"],
        accent=GREEN, tint=T_GREEN, bsz=920, tight=True, icon="1"))
    o.append(card(M + cw + IN(0.15), CY, cw, ch, "CHALLENGES & RISKS",
        ["Lab-to-field accuracy collapse :: models trained on clean lab "
         "leaves lose most of their accuracy outdoors while still reporting "
         "high confidence",
         "Sensor calibration :: raw capacitive readings are meaningless "
         "until converted to volumetric water content",
         "Not every budget phone is Snapdragon :: many are MediaTek, so the "
         "NPU path cannot be assumed",
         "No solar-radiation or wind sensor, so full Penman-Monteith ETo is "
         "not computable",
         "Trust and adoption :: one wrong spray advisory can end a farmer's "
         "confidence in the app"],
        accent=RED, tint=T_RED, bsz=920, tight=True, icon="2"))
    o.append(card(M + 2 * (cw + IN(0.15)), CY, cw, ch,
        "STRATEGY FOR OVERCOMING",
        ["Fine-tune on PlantDoc plus our own field photographs and report "
         "accuracy only on an unseen field-only test split",
         "Confidence gate :: below threshold the app asks for a better photo "
         "instead of naming a disease",
         "Dual execution path :: AI Hub NPU delegate on Snapdragon, "
         "NNAPI-or-CPU TFLite everywhere else",
         "Use Hargreaves-Samani ETo, an FAO-56 sanctioned temperature-only "
         "fallback",
         "Forecast fail-safe :: rain / no rain / unknown, and an unknown "
         "simply skips the rain-dependent rule",
         "Advisory stays advisory :: the farmer confirms, the app never acts "
         "on its own"],
        accent=NAVY, tint=T_BLUE, bsz=920, tight=True, icon="3"))
    by = CY + ch + IN(0.16)
    bh = D.FOOT_Y - by - IN(0.12)
    o.append(shape(M, by, IN(5.05), bh, prst="roundRect", adj=6000,
                   fill=WHITE, line=GREY, lnw=9525))
    o.append(bars(M + IN(0.25), by + IN(0.10), IN(4.55), bh - IN(0.20),
        [("Reported on clean lab images", 98, GREEN2),
         ("Same model on real field photos", 30, RED),
         ("Our target after field fine-tuning", 85, NAVY)],
        title="Accuracy honesty: why field data is non-negotiable",
        maxv=100, bsz=790))
    sx = M + IN(5.20)
    sw = (SW - M - sx - IN(0.30)) / 3.0
    tiles = [("Rs 3-4k", "One-time kit cost per farmer, phone already owned",
              GREEN, T_GREEN),
             ("< 1 s", "On-device diagnosis, fully offline, zero data charge",
              NAVY, T_BLUE),
             ("20-30%", "Targeted irrigation-water saving vs habit-based "
              "watering", AMBER, T_AMBER)]
    for k, (big, lab, ac, ti) in enumerate(tiles):
        o.append(stat(sx + k * (sw + IN(0.15)), by, sw, bh, big, lab,
                      accent=ac, tint=ti, bsz=1900, lsz=850))
    return wrap(o)


# ================================================================ slide 5 ====
def s5():
    o = chrome(5, 6, "IMPACT AND BENEFITS")
    o.append(card(M, CY, CW, IN(2.00), "POTENTIAL IMPACT ON THE TARGET AUDIENCE",
        ["Small and marginal farmers :: expert-level crop diagnosis in the "
         "field, in their own language, without internet, without paying an "
         "agronomist and without waiting for one to arrive",
         "Low-literacy and feature-phone users :: advice is spoken, "
         "colour-coded and escalates to SMS and a voice call, so the alert "
         "does not depend on reading a screen",
         "Cooperatives and FPOs :: one kit can serve several member farms; "
         "the optional dashboard shows a stress heat-map across all plots",
         "Extension officers :: field visits become data-led instead of "
         "complaint-led, since every observation is logged with GPS and time"],
        accent=GREEN, tint=T_GREEN, hsz=1200, bsz=940, tight=True))
    y2 = CY + IN(2.14)
    h2 = IN(2.52)
    cw = (CW - IN(0.30)) / 3.0
    o.append(card(M, y2, cw, h2, "SOCIAL",
        ["Breaks the literacy and language barrier through voice-first, "
         "icon-anchored vernacular advice",
         "Reduces dependence on informal shopkeeper advice that often "
         "over-prescribes chemicals",
         "Every alert follows What, Where, Action — no warning is ever given "
         "without a remedy",
         "Farmer-owned data stays on the phone; nothing is uploaded unless "
         "the farmer syncs"],
        accent=NAVY, tint=T_BLUE, bsz=910, tight=True, icon="S"))
    o.append(card(M + cw + IN(0.15), y2, cw, h2, "ECONOMIC",
        ["Early detection protects yield instead of paying for damage after "
         "it is visible from a distance",
         "Lower input cost :: spray and fertiliser only where and when a rule "
         "actually fires",
         "One-time kit cost, no subscription, no per-report fee — the phone "
         "is already owned",
         "Spray-event logging supports pre-harvest-interval compliance, which "
         "protects market price"],
        accent=GREEN, tint=T_GREEN, bsz=910, tight=True, icon="E"))
    o.append(card(M + 2 * (cw + IN(0.15)), y2, cw, h2, "ENVIRONMENTAL",
        ["Water drawn on measured depletion (FAO-56 MAD) rather than on a "
         "fixed habit, cutting groundwater use",
         "Targeted spraying reduces pesticide load on soil and water",
         "Less over-fertilising means less nutrient runoff",
         "Solar-assisted node and a phone already in the farmer's pocket keep "
         "the deployment footprint tiny"],
        accent=GREEN2, tint=T_GREEN, bsz=910, tight=True, icon="V"))
    fy = y2 + h2 + IN(0.16)
    o.append(tb(M + IN(0.02), fy, IN(12.0), IN(0.24),
                _p(_r("ALERT REACHES THE FARMER EVEN WITH NO SMARTPHONE AND "
                      "NO INTERNET  —  four-step escalation", 830, TITLE,
                      b=True), bullet=None)))
    o.append(flow(M, fy + IN(0.26), CW, IN(0.56), [
        ("FIELD BEACON", "red LED on the pole"),
        ("APP PUSH", "offline, on-device"),
        ("SMS", "if unread in 15 min"),
        ("VOICE CALL", "critical only, local accent")],
        fill=NAVY, sz=860, ssz=700))
    return wrap(o)


# ================================================================ slide 6 ====
def s6():
    o = chrome(6, 6, "RESEARCH AND REFERENCES")
    cw = (CW - IN(0.18)) / 2.0
    ch = IN(2.70)
    y2 = CY + ch + IN(0.16)
    o.append(card(M, CY, cw, ch, "AGRONOMY & DECISION LOGIC",
        ["Allen, Pereira, Raes & Smith :: FAO Irrigation and Drainage Paper "
         "56, Crop Evapotranspiration — ETo, Kc and Management Allowed "
         "Depletion.  fao.org/3/x0490e/x0490e00.htm",
         "Hargreaves & Samani (1985) :: temperature-based reference ETo, the "
         "FAO-56 sanctioned fallback when solar radiation and wind are not "
         "measured",
         "India Meteorological Department :: Gramin Krishi Mausam Sewa "
         "district agro-advisory and forecast bulletins.  mausam.imd.gov.in",
         "ICAR crop-stage and irrigation-scheduling advisories for the "
         "target crops (cotton, tomato, wheat, rice)"],
        accent=GREEN, tint=T_GREEN, hsz=1150, bsz=870, tight=True))
    o.append(card(M + cw + IN(0.18), CY, cw, ch, "DATASETS (LICENCES VERIFIED)",
        ["PlantVillage :: 54,306 images, 14 crops, 26 diseases, CC BY-SA 3.0. "
         "Laboratory conditions, used for pre-training only.  "
         "github.com/spMohanty/PlantVillage-Dataset",
         "PlantDoc :: 2,598 real field images, 13 species, 17 disease "
         "classes, CC BY 4.0 (Singh et al., CoDS-COMAD 2020). Fine-tuning "
         "and the honest test split.  github.com/pratikkayal/PlantDoc-Dataset",
         "IP102 :: 75,000+ images, 102 pest classes (Wu et al., CVPR 2019) — "
         "academic use only, so Phase-2 pest work stays non-commercial",
         "Mendeley Data, Indian field sets :: SAR-CLD-2024 cotton (2,137), "
         "wheat (1,603), rice leaf, rice stem borer (2,096, 64 MP phone)"],
        accent=NAVY, tint=T_BLUE, hsz=1150, bsz=870, tight=True))
    o.append(card(M, y2, cw, ch, "MODELS & EDGE AI TOOLCHAIN",
        ["Howard et al. (2019) :: Searching for MobileNetV3, arXiv:1905.02244 "
         "— the classifier family used for the on-device model",
         "TensorFlow Lite post-training INT8 quantisation and the NNAPI "
         "delegate documentation (non-Snapdragon fallback path)",
         "Qualcomm AI Hub :: model compilation, NPU profiling and on-device "
         "benchmarking for Snapdragon.  aihub.qualcomm.com",
         "Qualcomm Dragonwing RB3 Gen 2 (QCS6490) developer documentation — "
         "the Tier 2 always-on field node",
         "Ultralytics YOLOv8-n / YOLOv11-n documentation — Phase-2 pest "
         "detection"],
        accent=AMBER, tint=T_AMBER, hsz=1150, bsz=870, tight=True))
    o.append(card(M + cw + IN(0.18), y2, cw, ch,
        "PRIOR ART, BENCHMARKS & FIELD UX",
        ["Mohanty, Hughes & Salathe (2016) :: Using Deep Learning for "
         "Image-Based Plant Disease Detection, Frontiers in Plant Science — "
         "the 99% lab benchmark we deliberately do not quote as a field number",
         "Published lab-to-field transfer studies reporting large accuracy "
         "collapse with unchanged high confidence — the basis of our "
         "confidence gate",
         "Existing products reviewed :: Plantix (cloud vision, no sensors), "
         "Fasal (paid IoT, no vision), CropIn (enterprise satellite SaaS)",
         "Field UX practice :: high-contrast sunlight-readable layouts, "
         "traffic-light severity, and the What-Where-Action alert framework "
         "used in Indian agri-extension messaging"],
        accent=GREY, tint=T_GREY, hsz=1150, bsz=870, tight=True))
    return wrap(o)


# ==================================================================== main ===
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    logo = open(os.path.join(here, "sihlogo.png"), "rb").read()
    out = os.path.join(os.path.dirname(here),
                       "making the ppt for submission",
                       "KISAN-EDGE_SIH2026_Idea_Submission.pptx")
    write_pptx([s1(), s2(), s3(), s4(), s5(), s6()], out, {"sihlogo.png": logo})
