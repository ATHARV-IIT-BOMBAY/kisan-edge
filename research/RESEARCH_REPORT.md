# Research Report — SIH 2026 PS 26180
## Field-deployable AI-powered Smart Farming Assistant (Qualcomm)

**Project name (proposed):** KISAN-EDGE
**Theme:** Agriculture, FoodTech & Rural Development · **Category:** Hardware

---

## 1. Problem understanding
Indian agriculture loses an estimated 15–25% of potential yield every year to crop diseases, pests, nutrient deficiencies and mistimed irrigation — most of it caught too late. Small & marginal farmers (~86% of holdings) rarely have timely access to agronomists, and rural fields have weak/intermittent internet, so cloud-only apps fail exactly where they are needed. Climate shocks (drought, floods, heat waves) are increasing.

**Gap in existing solutions:** most are cloud-dependent, photo-only (ignore live soil/weather data), give generic advice, and assume a literate, English-speaking smartphone user.

## 2. Our solution (one line)
A low-cost, **portable handheld sensor kit** paired with a companion Android app that runs AI **on-device (no internet needed)** — the farmer walks the plot, photographs leaves and pulls live soil readings over Bluetooth, and a transparent rule engine turns both into one clear spoken/iconic instruction.

## 3. The four building blocks
1. **Vision AI** — disease detection from leaf images (MVP); pest object detection is Phase 2.
2. **Environmental sensing** — soil moisture, temperature, humidity, soil EC, infrared leaf temperature.
3. **Advisory engine (decision brain)** — fuses image verdict + sensor data + crop stage + cached weather via agronomy rules.
4. **Farmer interface** — offline voice TTS + icons in the app, field zone map, and SMS fallback, in the local language.

## 4. AI model sourcing (my focus area)
Strategy: **reuse pretrained backbones → fine-tune on Indian field data → quantise for the edge.**

| Task | Model | Dataset | Scope |
|---|---|---|---|
| Disease classification | MobileNetV3 / EfficientNet-Lite | PlantVillage (pretrain) + **PlantDoc** (real field) + own field photos | **MVP** |
| Pest detection (object detection) | YOLOv8-n / YOLOv11-n | IP102 (75k+ images, 102 classes) | **Phase 2** — detection is materially harder than classification |
| Deployment | Export + INT8 quantise via **Qualcomm AI Hub** | — | Snapdragon NPU now, QCS6490 later, same artefact |

**Critical research finding — the lab-to-field gap:** models trained on clean lab datasets like PlantVillage report ~95%+ accuracy but collapse in real fields; one study measured a **67.7-percentage-point accuracy drop** on cross-domain transfer while the model still reported ~80% confidence. **Mitigation:** fine-tune/validate on PlantDoc and our own in-field images, and use confidence gating so the device prompts a recapture rather than surfacing an unreliable result.

### 4.1 Datasets — verified sources and licences

All licences below were checked against the primary source, not assumed. **Tier A is the training spine; Tier B adds Indian crop coverage; Tier C is Phase 2 only.**

| # | Dataset | Size | Conditions | Licence | Role |
|---|---|---|---|---|---|
| A1 | **PlantVillage** ([repo](https://github.com/spMohanty/PlantVillage-Dataset), [HF card](https://huggingface.co/datasets/mohanty/PlantVillage)) | 54,306 imgs · 14 crops · 26 diseases | Lab — single detached leaf, uniform background | **CC BY-SA 3.0** | **Pretrain only.** Never report its accuracy as ours |
| A2 | **PlantDoc** ([classification](https://github.com/pratikkayal/PlantDoc-Dataset), [detection](https://github.com/pratikkayal/PlantDoc-Object-Detection-Dataset)) | 2,598 imgs · 13 species · 17 diseases | **Real field** — clutter, mixed light, occlusion | **CC BY 4.0** | **Fine-tune + the honest test split** |
| B1 | [SAR-CLD-2024 cotton](https://data.mendeley.com/datasets/b3jy2p6k8w/2) | 2,137 imgs · 7 classes | Field | CC BY 4.0 (verify on page) | Cotton coverage |
| B2 | [Wheat disease dataset](https://data.mendeley.com/datasets/5gc7hwydwg/1) | 1,603 originals · 5 classes · 1920×1080 | Field | CC BY 4.0 (verify) | Wheat coverage |
| B3 | [Rice leaf disease](https://data.mendeley.com/datasets/zfwkkdj6dk/2) | multi-class | Field | CC BY 4.0 (verify) | Rice coverage |
| B4 | [FC45DHLPD](https://data.mendeley.com/datasets/ph9g2cfxwm/1) | 15 crops · 45 classes incl. cotton, wheat, rice, chilli, sugarcane, groundnut | Mixed | CC BY 4.0 (verify) | Broad Indian crop set |
| B5 | [Rice stem borer, symptom-labelled](https://data.mendeley.com/datasets/hnfjs42d5g/1) | 2,096 imgs | Field, **captured on a 64 MP smartphone** | CC BY 4.0 (verify) | Closest match to our own capture device |
| C1 | **IP102** ([repo](https://github.com/xpwu95/IP102), [CVPR 2019 paper](https://openaccess.thecvf.com/content_CVPR_2019/html/Wu_IP102_A_Large-Scale_Benchmark_Dataset_for_Insect_Pest_Recognition_CVPR_2019_paper.html)) | 75,000+ imgs · 102 pest classes | Field | ⚠️ **Academic use only** — other uses need the author's permission | Phase 2 pest detection |

**Five licence and data-hygiene points that actually matter:**

1. **IP102 is academic-use-only.** Fine for SIH; a blocker the moment this becomes a product. Either email the author (contact is on the repo) or plan a replacement. Flag it now, not later.
2. **PlantVillage is share-alike (CC BY-SA 3.0).** If we redistribute the dataset or a curated derivative of it, the same licence follows. Trained weights are generally treated as a separate artefact, but we should not publish a repackaged subset without matching the licence. Not legal advice — worth a considered decision if we open-source.
3. **PlantDoc's images were internet-scraped.** The *annotations* are cleanly CC BY 4.0; the underlying photographs carry their own upstream copyright. Acceptable for research and a hackathon, another reason our own field photos matter for anything beyond that.
4. **Leakage: PlantVillage contains multiple shots of the same physical leaf.** A random train/test split therefore leaks and inflates accuracy. Use the leaf-grouped 80/20 splits published on the Hugging Face card, or group by leaf ID ourselves.
5. **Label taxonomies don't match across datasets.** PlantVillage, PlantDoc and each Mendeley set name classes differently. Building one unified label map — and deciding which fine-grained classes to merge — is real work on my track, not a formality.

**Attribution:** every dataset above requires credit. I'll keep a `DATASETS.md` with the BibTeX for each (PlantDoc → Singh et al., CoDS-COMAD 2020; PlantVillage → Mohanty, Hughes & Salathé 2016; IP102 → Wu et al., CVPR 2019) so the citation slide writes itself.

**Our own field images — the part no download replaces.** Target a few hundred photos per target disease, shot on the actual demo phone, at the ΔT sampling window, with the label confirmed by someone who knows the crop. These are the only images drawn from the same distribution as deployment, so they belong in the **test** split first and the training split second.

## 5. Advisory logic (my focus area)
A transparent, **table-driven rule engine** — explainable, not a black box. Exposed to the app as one clean interface: structured sensor + image result in, one recommendation object out.

- **Inputs:** `image_class`, `confidence`, `soil_moisture` (calibrated VWC), `temp`, `humidity`, `soil_EC`, `leaf_temp` (IR), `crop_stage`, `forecast` (tri-state: rain / no rain / **unknown**).
- **Example rules:**
  - IF `soil_moisture < MAD threshold` AND no rain forecast → *Irrigate now*.
  - IF `(leaf_temp − air_temp) > stress threshold` → *Early water stress, before visible wilting*.
  - IF `disease_conf > 0.75` AND `humidity > 80%` → *High blight risk – scout & targeted spray*.
  - IF `soil_EC` low AND image shows yellowing → *Likely nitrogen deficiency – top-dress*.
  - IF `temp > heat threshold` for stage → *Heat-stress: irrigate at dusk, avoid midday spray*.
- **Confidence gating:** low-confidence image → ask farmer to re-capture.
- **Forecast fail-safe:** if the cache is stale and no GKMS SMS has arrived, rain-dependent gates are **skipped, never assumed**.
- **Aggregation:** per-point verdicts roll up into the field-level colour-coded zone recommendation.

**Irrigation grounded in agronomy (FAO-56):** trigger irrigation at **Management Allowed Depletion (MAD)**; crop water need = reference ET (ETo) × crop coefficient (Kc) for the growth stage; skip if rain is forecast. All thresholds live in **per-crop / per-soil config profiles**, so one kit adapts to wheat/rice/cotton/tomato.

**ETo source — a real constraint:** full FAO-56 Penman-Monteith needs solar radiation and wind speed, and the kit has no sensors for either. We therefore use the **Hargreaves-Samani** temperature-based method, which FAO-56 sanctions as the fallback when radiation and wind data are unavailable, refined by cached forecast data when it exists. This is a deliberate, documented approximation rather than an oversight.

**Calibration dependency:** raw capacitive-sensor percentage is meaningless to these rules — clay and sandy soils have very different field capacity and wilting points. The hardware track owns raw-ADC-to-physical-unit conversion (calibration curve in ESP32 firmware); this track owns the agronomic thresholds and consumes **volumetric water content**. The interface between the two is a fixed BLE packet schema with explicit units.

### 5.1 Engine interface contract
The advisory engine is a pure function: one observation in, one recommendation out. The app never reads rule internals, and the rules never touch the UI or the sensors. This is the single integration point between my track and the app track.

```
Observation  →  { crop_id, crop_stage, soil_profile,
                  point_id, gps, timestamp,
                  image_class, image_confidence,
                  soil_vwc, air_temp_c, humidity_pct,
                  soil_ec_dsm, leaf_temp_c,
                  forecast: rain | no_rain | unknown }

Recommendation → { action_code,          // enum, drives icon + TTS string
                   severity,             // green | amber | red
                   message_key,          // localised, not raw English
                   because[],            // the rules that fired — explainability
                   needs_recapture,      // confidence gate tripped
                   confidence_note }
```

Two properties matter for the demo: `because[]` makes every verdict auditable to a farmer or agri-officer, and `message_key` keeps translation out of the rule layer so adding a language never touches agronomy.

**Episodic sampling changes what rules are possible.** The kit is carried to the field per session, not left in it, so the engine sees a sparse series of visits rather than a continuous stream. Any rule requiring consecutive daily readings — sustained waterlogging, multi-day pest population trend — is therefore **not implementable in the MVP** and is deferred to Tier 2, where a fixed installation reads unattended. MVP rules are single-observation or short-history only.

**Measurement protocol for the ΔT signal.** Canopy-minus-air temperature varies strongly with time of day, cloud cover and wind, so readings taken at 9 am and 2 pm are not comparable. The app must therefore timestamp every reading and prompt for sampling within a consistent near-midday window under clear sky; readings outside that window are recorded but excluded from the stress gate. Without this discipline the drought signal is noise, not data.

## 6. Hardware & edge platform — two-tier plan

The edge AI must run on a Qualcomm chip (Qualcomm is the sponsoring org, category is Hardware). But that chip does **not** have to be a devkit we don't own yet: **any Snapdragon Android phone is a Qualcomm edge-AI device**, and Qualcomm AI Hub compiles/quantises models specifically for Snapdragon NPUs. So Tier 1 is buildable today with zero procurement risk, and Tier 2 is a drop-in upgrade.

### Tier 1 — MVP for the hackathon (what we actually build)
A **portable handheld kit**, not a fixed installation.

| Part | Component | Job |
|---|---|---|
| Sensor node | **ESP32** + capacitive soil-moisture + DHT22 + soil **EC** + **MLX90614** IR leaf-temp | Reads the field, sends a structured packet over BLE |
| Edge AI compute | **Snapdragon Android phone** (Qualcomm NPU) | Runs the quantised vision model + advisory rule engine |
| Camera | **The phone camera** | Leaf/canopy images |
| Interface | Android app + offline TTS voice + icons + SMS fallback | Advice to the farmer |
| Power | Battery pack (MVP) / solar (Tier 2) | Portable, handheld operation |

**Why portable, not fixed:** soil moisture varies across a single plot with drainage, elevation and shade, and disease pressure is patchy rather than uniform. One fixed sensor cannot represent a field. The farmer carries the kit to **3–5 GPS-tagged sampling points** per round — the same principle as composite soil sampling in standard agronomy. Point-level results aggregate into a colour-coded field zone view.

**Why the phone camera and not an ESP32-CAM:** the ESP32-CAM's OV2640 is a low-resolution, fixed-focus, noisy sensor. Leaf-lesion classification depends on fine texture and colour detail — exactly what a cheap camera destroys, and it makes the lab-to-field accuracy gap (§4) much worse. A phone camera is far better optics for free, and it is already a Qualcomm ISP + NPU in the farmer's hand.

**Nutrient sensing — what we do and don't claim:** soil **EC** gives a real fertiliser-depletion/salinity signal and is cross-checked against image-based colour and texture cues. We do **not** claim individual N-P-K measurement: cheap "NPK sensors" sold online are EC sensors with a marketing label, and true NPK needs lab chemistry. Similarly, no affordable sensor detects pesticide residue, so the pesticide feature is **spray decision support** (targeted-spray recommendation, spray-event logging, pre-harvest-interval warnings), not residue analysis.

**Division of labour is clean:** ESP32 = sensing and calibration to physical units. Phone = camera + inference + rules + UI. No conflict between the hardware and app tracks.

**Which Android phone — a constraint we should state, not dodge:** the requirement to run on entry-level phones and the requirement to showcase the Snapdragon NPU pull in opposite directions, because many budget Indian handsets ship MediaTek SoCs. We resolve it by shipping **two execution paths from one model**: the AI Hub-exported QNN/NPU delegate on Snapdragon (the demo device, and the sponsor story), with an NNAPI-or-CPU TFLite fallback on everything else. A quantised MobileNetV3 runs acceptably on CPU, so non-Snapdragon users lose latency, not function. The deck should name the demo device explicitly rather than implying every phone is a Qualcomm target.

### Tier 2 — production / field-permanent (Dragonwing)
- **Compute:** Qualcomm Dragonwing RB3 Gen 2 (QCS6490) — Linux-based edge AI board with on-device NPU.
- Sensors wire **directly into its GPIO/I2C** — the ESP32 and BLE link disappear.
- Adds a fixed field camera for unattended 24×7 monitoring (no phone needed in the field).
- **The same AI Hub-exported model and the same rule engine run unchanged on both tiers** — that is the whole point of exporting through AI Hub. Tier 2 is a deployment target, not a rewrite.

### Common to both
- **Connectivity:** works fully offline; opportunistic Wi-Fi/4G sync + SMS gateway.
- **Power:** solar panel + battery for off-grid fields (Tier 2).
- **Why edge:** low latency, no data cost, works without network, keeps farm data private.

> **Honesty note for the jury:** we present Tier 1 as the demo and Tier 2 as the deployment path. We do not claim to have a Dragonwing kit unless we do. Judges reward a working MVP with a credible scale-up far more than an aspirational BOM.

## 7. Differentiators
Truly offline edge AI · sensor+vision fusion (not photo-only) · explainable rule engine · field-realistic models · farmer-first voice/icon/SMS UX.

## 8. Impact
Higher yield (early detection) · lower cost (targeted spray, less wasted fertiliser) · water & electricity saved · climate resilience · inclusive for low-connectivity smallholders.

## 9. Feasibility & roadmap
- **Phase 1 — MVP (hackathon):** ESP32 sensor node + Snapdragon Android phone as the edge AI device. Fine-tune the vision models, export via Qualcomm AI Hub, build the rule engine, demo end-to-end on one plot.
- **Phase 2 — field pilot:** deploy on a test plot, collect in-field images, tune per-crop thresholds, add SMS + solar.
- **Phase 3 — migrate & scale:** port the identical model + rule engine to the **Dragonwing RB3 Gen 2** for permanent, unattended field installation with a fixed camera; more crops; dashboard; pilot with an FPO/cooperative.
- **Risks:** domain gap → field fine-tuning; sensor drift → calibration + gating; cost → one shared device per cluster; **devkit availability → Phase 1 deliberately needs no Dragonwing.**

## 10. Tech stack
PyTorch/TFLite · MobileNetV3 / EfficientNet-Lite / YOLOv8-n · Qualcomm AI Hub (INT8 export for Snapdragon **and** QCS6490) · rule engine + per-crop YAML (Kotlin/Python) · ESP32 firmware (Arduino/ESP-IDF) over BLE · Android app + TTS + SMS gateway · optional cloud sync/dashboard.

---

## 11. Open questions & known limits
Stated deliberately — a jury trusts a team that names its own boundaries more than one that claims none.

| Item | Status | Effect if unresolved |
|---|---|---|
| Snapdragon vs budget (MediaTek) phones | Resolved by dual execution path; demo device must be named | Sponsor-alignment claim looks overstated |
| ETo without solar radiation / wind | Resolved as Hargreaves-Samani, documented as an approximation | Irrigation depth less precise; trigger timing unaffected |
| No rain gauge | Open — water balance is **open-loop** | Actual rainfall can't be verified against forecast; depletion estimate drifts over a season |
| GKMS SMS parsing | Works for a hackathon build; Play Store restricts SMS-read permission | Blocks public distribution, not the demo |
| Multi-day / trend rules | Not implementable on episodic sampling; deferred to Tier 2 | Waterlogging and pest-trend rules absent from MVP |
| Dragonwing devkit access | Unconfirmed | None for Phase 1 by design; would promote Tier 2 from Phase 3 to Phase 2 if obtained |
| Field-image collection | Not started | Largest single risk to real-world accuracy (§4) |

## 12. My deliverables (this track)
1. Fine-tuned disease classifier — MobileNetV3/EfficientNet-Lite, PlantVillage pretrain → PlantDoc + own field images, with a held-out **field-only** test split so the reported number is honest.
2. INT8 export via Qualcomm AI Hub, plus the NNAPI/CPU fallback artefact.
3. The table-driven rule engine, per-crop/per-soil YAML profiles, confidence gate, forecast fail-safe, per-point → field aggregation.
4. The frozen `Observation` / `Recommendation` contract in §5.1, handed to the app track early so both sides can build against it in parallel.

---

## Sources
- Reliability gap, controlled-to-field shift (67.7pt drop): https://www.frontiersin.org/articles/10.3389/fpls.2026.1826962
- PlantVillage degrades under field conditions (review): https://link.springer.com/article/10.1007/s42452-026-08684-0
- Tomato disease/pest with real field datasets (PlantVillage over-optimism): https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2024.1493322/full
- IP102 pest benchmark (CVPR 2019): http://openaccess.thecvf.com/content_CVPR_2019/papers/Wu_IP102_A_Large-Scale_Benchmark_Dataset_for_Insect_Pest_Recognition_CVPR_2019_paper.pdf
- PlantVillage dataset repo (CC BY-SA 3.0): https://github.com/spMohanty/PlantVillage-Dataset
- PlantVillage licence + leaf-grouped splits: https://huggingface.co/datasets/mohanty/PlantVillage
- PlantDoc classification dataset (CC BY 4.0): https://github.com/pratikkayal/PlantDoc-Dataset
- PlantDoc object-detection annotations: https://github.com/pratikkayal/PlantDoc-Object-Detection-Dataset
- IP102 repo — academic-use-only notice: https://github.com/xpwu95/IP102
- Mendeley Data — Indian/regional crop disease sets (cotton, wheat, rice, 15-crop): https://data.mendeley.com/datasets/b3jy2p6k8w/2 · https://data.mendeley.com/datasets/5gc7hwydwg/1 · https://data.mendeley.com/datasets/zfwkkdj6dk/2 · https://data.mendeley.com/datasets/ph9g2cfxwm/1
- FAO-56 Crop Evapotranspiration (ETo × Kc, MAD): https://www.fao.org/4/X0490E/x0490e00.htm
- Qualcomm AI Hub — YOLOv8 detection model: https://aihub.qualcomm.com/models/yolov8_det
- Qualcomm Dragonwing RB3 Gen 2 docs: https://dragonwingdocs-staging.qualcomm.com/Tools/Qualcomm-Device-Cloud/run-sample-applications
