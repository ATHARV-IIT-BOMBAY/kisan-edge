#!/usr/bin/env python3
"""Deck content for SIH PS 26180 - Smart Farming Assistant."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_pptx import build

slides = []

slides.append({"kind": "title",
    "title": "KISAN-EDGE: Smart Farming Assistant",
    "bullets": [
        "An offline-first, edge-AI device that sees crop stress and senses the field — giving farmers instant, actionable advice.",
        "Smart India Hackathon 2026  •  PS 26180  •  Qualcomm Inc.",
        "Theme: Agriculture, FoodTech & Rural Development   |   Category: Hardware",
    ]})

slides.append({"kind": "content",
    "title": "The Problem",
    "bullets": [
        "Indian farmers lose 15–25% of yield yearly to diseases, pests and poor water timing — mostly caught too late. ::",
        "Small & marginal farmers (86% of holdings) lack timely access to agri-experts.",
        "Rural fields have weak / intermittent internet — cloud-only AI apps fail exactly where they are needed.",
        "Climate shocks (drought, floods, heat waves) are getting more frequent and less predictable.",
        "Existing apps: ::",
        "-> Need constant connectivity and send photos to the cloud.",
        "-> Give generic advice, ignore live field sensor data.",
        "-> Are hard to use for low-literacy, non-English farmers.",
    ]})

slides.append({"kind": "content",
    "title": "Our Solution — in one line",
    "bullets": [
        "A low-cost, portable handheld sensor kit paired with an Android app that runs AI on-device (no internet needed) — the farmer walks the plot, photographs leaves and pulls live soil readings, and gets one clear spoken instruction. ::",
        "Phone camera + on-device vision AI ::",
        "-> Classifies crop disease from leaf images with a confidence score (MVP); pest object-detection is Phase 2.",
        "Handheld sensor kit (ESP32 over Bluetooth) ::",
        "-> Soil moisture, temperature, humidity, soil EC, infrared leaf temperature.",
        "Advisory engine (the decision brain) ::",
        "-> Fuses image verdict + sensor data + crop stage + cached weather → one clear action.",
        "Farmer interface ::",
        "-> Voice (offline TTS) + icons in the Android app + SMS fallback, in the local language.",
    ]})

slides.append({"kind": "content",
    "title": "How It Works — Data Flow",
    "bullets": [
        "1. SAMPLE  —  App suggests 3–5 points across the plot; farmer visits each one. ::",
        "2. CAPTURE  —  At each point: leaf photo + live Bluetooth sensor reading, auto GPS-tagged. ::",
        "3. INFER (on-device)  —  Vision model returns disease class + confidence; low confidence → recapture prompt. ::",
        "4. DECIDE (advisory engine)  —  Agronomy rules fuse image verdict + sensors + crop stage + cached weather. ::",
        "5. ADVISE  —  Per-point action, then a colour-coded field zone view: “Irrigate now”, “Likely blight in zone 3”. ::",
        "6. LOG & SYNC  —  Stored locally first; syncs opportunistically when connectivity returns. ::",
        "-> Everything critical runs offline; the cloud is optional, not required.",
    ]})

slides.append({"kind": "section",
    "title": "The AI & Advisory Core",
    "bullets": ["Pretrained models + the rule-based decision engine (our team's focus area)"]})

# more slides appended below


slides.append({"kind": "content",
    "title": "Vision Models — Sourcing Pretrained AI",
    "bullets": [
        "Strategy: reuse proven pretrained backbones, fine-tune on Indian crop data, quantise for the edge. ::",
        "MVP — disease classification ::",
        "-> MobileNetV3 / EfficientNet-Lite fine-tuned on PlantVillage + PlantDoc (real field images) + own field photos.",
        "-> Returns class + confidence; confidence gating prompts a recapture instead of guessing.",
        "Phase 2 — pest object detection ::",
        "-> YOLOv8-n / YOLOv11-n on the IP102 benchmark (75k+ images, 102 classes). Deliberately deferred: detection is a materially harder task than classification.",
        "Deployment on Qualcomm ::",
        "-> Export & quantise (INT8) via Qualcomm AI Hub → Snapdragon NPU now, QCS6490 later, same artefact.",
        "Key insight: lab-trained models drop sharply in real fields — we fine-tune on in-field images to close that gap. ::",
    ]})

slides.append({"kind": "content",
    "title": "The Advisory Logic (Decision Brain)",
    "bullets": [
        "A transparent rule engine that fuses the image verdict with live sensor readings — explainable, not a black box. ::",
        "Inputs :: image_class, confidence, soil_moisture (VWC), temp, humidity, soil EC, leaf temp (IR), crop stage, cached forecast",
        "Example rules :: ",
        "-> IF soil_moisture < MAD threshold AND no rain forecast → 'Irrigate now'.",
        "-> IF (leaf_temp − air_temp) > stress threshold → 'Early water stress before visible wilting'.",
        "-> IF disease_conf > 0.75 AND humidity > 80% → 'High blight risk – scout & targeted spray'.",
        "-> IF soil_EC low AND image shows yellowing → 'Likely nitrogen deficiency – top-dress'.",
        "-> IF temp > heat threshold for crop stage → 'Heat-stress: irrigate at dusk, avoid midday spray'.",
        "Fail-safe :: if the forecast is stale and unavailable, rain-dependent gates are skipped, never assumed. ::",
    ]})

slides.append({"kind": "content",
    "title": "Irrigation Logic — grounded in agronomy",
    "bullets": [
        "We don't guess thresholds — we use the FAO-56 water-balance framework. ::",
        "-> Trigger irrigation when soil water depletion reaches Management Allowed Depletion (MAD) for that crop.",
        "-> Crop water need = reference ET (ETo) × crop coefficient (Kc) for the current growth stage.",
        "-> ETo source :: full Penman-Monteith needs solar radiation + wind, which the kit has no sensors for — so we use the temperature-based Hargreaves-Samani method (an FAO-56 sanctioned fallback), refined by cached forecast data when available.",
        "-> Skip / delay if rain is forecast — saves water and pumping cost.",
        "Calibration matters :: raw sensor % is meaningless; we calibrate to volumetric water content per soil type, since clay and sandy soils have very different field capacity. ::",
        "All thresholds are per-crop config profiles, so the same kit adapts to wheat, rice, cotton, tomato, etc. ::",
    ]})

slides.append({"kind": "content",
    "title": "Hardware — Tier 1 (portable MVP we build now)",
    "bullets": [
        "Every Snapdragon Android phone IS a Qualcomm edge-AI device — AI Hub compiles our model for its NPU. No devkit needed to start. ::",
        "Handheld sensor kit :: ESP32 + capacitive soil-moisture + DHT22 + soil EC + MLX90614 infrared leaf-temp → BLE to the phone.",
        "Edge AI compute :: Snapdragon Android phone — runs the quantised vision model + advisory rule engine on-device.",
        "Camera :: the phone camera (good optics, autofocus) — not an ESP32-CAM.",
        "-> Leaf-lesion detection needs fine texture/colour detail; a low-res fixed-focus OV2640 destroys exactly that.",
        "Portable, not fixed :: soil moisture and disease pressure vary across one plot, so the farmer samples 3–5 GPS-tagged points per round — the same logic as composite soil sampling. ::",
        "Clean split :: ESP32 senses. Phone sees, thinks and speaks. No overlap between hardware and app tracks. ::",
    ]})

slides.append({"kind": "content",
    "title": "Hardware — Tier 2 (field-permanent scale-up)",
    "bullets": [
        "Qualcomm Dragonwing RB3 Gen 2 (QCS6490) :: Linux-based edge AI board with on-device NPU, for unattended 24x7 field installs.",
        "Sensors wire directly into its GPIO / I2C — the ESP32 and BLE link are no longer needed.",
        "Adds a fixed field camera, so no phone has to be present in the field.",
        "Same model, same rules, zero rewrite :: because we export through Qualcomm AI Hub, the identical INT8 model and rule engine run on both tiers. ::",
        "Power :: solar panel + battery for remote, off-grid fields.",
        "Why edge (both tiers) :: low latency, no data cost, works without network, keeps farm data private.",
    ]})

slides.append({"kind": "content",
    "title": "Farmer Interface & Alerts",
    "bullets": [
        "Designed for low-literacy, low-connectivity users. ::",
        "-> Voice advisory in the farmer's language via offline text-to-speech — no internet call needed.",
        "-> Colour + icon status in the app (green / amber / red), not text-dependent screens.",
        "-> Colour-coded field zone map from the GPS-tagged sampling points.",
        "-> SMS fallback for critical alerts — reaches the farmer without any data connection.",
        "-> Farmer can confirm or correct a diagnosis, building trust and a future training set.",
        "One clear action at a time — not dashboards full of numbers. ::",
    ]})

slides.append({"kind": "content",
    "title": "Analytics Dashboard (Phase 2)",
    "bullets": [
        "On-device now :: per-point and per-field history for moisture, EC, disease incidence and drought signal.",
        "Cloud dashboard is a Phase 2 item, not an MVP claim. ::",
        "-> Multi-field aggregate view for cooperatives, FPOs and agri-officers.",
        "-> Yield-risk forecasting and season decision support.",
        "-> Optional integration with weather services and irrigation controllers.",
        "Data syncs opportunistically whenever connectivity is briefly available. ::",
    ]})

slides.append({"kind": "content",
    "title": "Why We Stand Out",
    "bullets": [
        "Truly offline edge AI :: full diagnosis without internet — most competitors are cloud-dependent.",
        "Sensor + vision fusion :: we combine camera + soil/weather data; photo-only apps miss irrigation & stress.",
        "Explainable rule engine :: farmers & agri-officers can see WHY advice was given — builds trust.",
        "Field-realistic models :: fine-tuned on in-field images, not just clean lab photos.",
        "Farmer-first UX :: voice + icons + SMS in local language, one action at a time. ::",
    ]})

slides.append({"kind": "content",
    "title": "Impact",
    "bullets": [
        "Higher yield :: early detection stops small problems becoming crop failures.",
        "Lower cost :: targeted spraying instead of blanket pesticide; less wasted fertiliser.",
        "Water saved :: irrigate only when needed → cuts water & pump-electricity use.",
        "Resilience :: early warnings for drought, flood, heat and outbreaks.",
        "Inclusive :: works for smallholders in low-connectivity regions — the people who need it most. ::",
    ]})

slides.append({"kind": "content",
    "title": "Feasibility & Roadmap",
    "bullets": [
        "Phase 1 — MVP (hackathon) :: ESP32 sensor node + Snapdragon phone as the edge AI device; fine-tune models, export via AI Hub, build rule engine, demo end-to-end.",
        "Phase 2 — field pilot :: deploy on a test plot, collect in-field images, tune per-crop thresholds, add SMS + solar.",
        "Phase 3 — migrate & scale :: port the identical model + rules to Dragonwing RB3 Gen 2 for permanent installs; more crops; dashboard; pilot with an FPO / cooperative.",
        "Risks & mitigation :: ",
        "-> Domain gap (lab→field) → continuous field-image fine-tuning.",
        "-> Sensor drift → periodic calibration + confidence gating.",
        "-> Cost → shared device per cluster of small farms.",
        "-> Devkit availability → Phase 1 deliberately requires no Dragonwing kit.",
    ]})

slides.append({"kind": "content",
    "title": "Tech Stack",
    "bullets": [
        "AI :: PyTorch / TensorFlow-Lite, MobileNetV3, EfficientNet-Lite, YOLOv8-n; Qualcomm AI Hub for export & INT8 quantisation.",
        "Edge runtime :: Snapdragon NPU (Tier 1) and QCS6490 NPU (Tier 2) — same TFLite/QNN artefact on both.",
        "Sensor node :: ESP32 firmware (Arduino / ESP-IDF), BLE link to the phone.",
        "Advisory engine :: rule-based decision layer, per-crop YAML config, FAO-56 water balance.",
        "App / UI :: Android app, TTS for voice, SMS gateway, local display on Tier 2.",
        "Cloud (optional) :: sync service + analytics dashboard (only when online). ::",
    ]})

slides.append({"kind": "section",
    "title": "My Role in the Team",
    "bullets": ["Sourcing/integrating the pretrained model + building the advisory logic"]})

slides.append({"kind": "content",
    "title": "My Contribution (Atharv)",
    "bullets": [
        "Model sourcing & integration :: ",
        "-> Pick and fine-tune the pretrained backbone (MobileNetV3 / EfficientNet-Lite) on PlantVillage + PlantDoc + our field images.",
        "-> Export & quantise (INT8) via Qualcomm AI Hub; wire on-device inference into the Android app.",
        "Advisory logic (decision brain) :: ",
        "-> Table-driven rule engine fusing image class + confidence with moisture, temp, humidity, EC and leaf-temp ΔT.",
        "-> Encode FAO-56 irrigation thresholds, per-crop/per-soil profiles, confidence gating and forecast fail-safe.",
        "-> Aggregate per-point verdicts into the field-level zone recommendation.",
        "Clean interface :: structured sensor + image result in, one recommendation object out — the app never touches rule internals. ::",
    ]})

slides.append({"kind": "content",
    "title": "References",
    "bullets": [
        "PlantDoc — real field-condition plant disease image dataset; PlantVillage for lab-condition pretraining.",
        "Cross-domain field-shift studies — lab-trained accuracy drops sharply in real fields (Frontiers in Plant Science).",
        "IP102: large-scale insect-pest benchmark, 75k+ images / 102 classes (CVPR 2019) — Phase 2 pest detection.",
        "FAO-56: Crop Evapotranspiration — ETo × Kc, Management Allowed Depletion, Hargreaves-Samani fallback.",
        "Qualcomm AI Hub — on-device model optimisation for Snapdragon phones and Dragonwing RB3 Gen 2 (QCS6490).",
        "IMD Gramin Krishi Mausam Sewa (GKMS) — SMS agromet advisories used as the deep-offline forecast path.",
    ]})

build(slides, "/Users/atharv/sih/KISAN-EDGE_SIH26180.pptx")
