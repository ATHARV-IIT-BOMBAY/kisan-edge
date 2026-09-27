# 🌾 KISAN-EDGE

**Offline, on-device AI smart-farming assistant for Indian farmers.**
Point a phone at a leaf → get a disease diagnosis and a plain-language action, with **no internet** after first load.

> **Smart India Hackathon 2026** · Problem Statement **26180** · **Qualcomm Inc.**
> Category: **Hardware** · Theme: Agriculture, FoodTech & Rural Development

---

## The problem

Millions of small and marginal Indian farmers face crop disease, pests, and water stress with **no timely diagnostics and poor connectivity**. Cloud-first apps fail exactly where they are needed — in the field, offline.

## Our approach

Perception and advice run **entirely on the device**:

1. **AI perception** — a pretrained convolutional neural net (MobileNet, PlantVillage, 38 classes) runs in the browser via **TensorFlow.js**. The leaf image never leaves the phone.
2. **Deterministic advisory** — a transparent, auditable rule engine turns the model's label + live sensor readings (soil moisture, air temperature, humidity) into one clear action: *irrigate now*, *spray fungicide*, *heat-stress warning*, etc.

Two systems on purpose: the AI *sees*, the rules *decide* — so every recommendation is explainable.

---

## Try the prototype (30 seconds, no build)

The MVP is a **single self-contained HTML file** — no server, no install.

```bash
git clone https://github.com/ATHARV-IIT-BOMBAY/kisan-edge.git
cd kisan-edge
open prototype/index.html          # macOS  (use xdg-open on Linux)
```

Or drag `prototype/index.html` onto any modern browser (Chrome/Edge recommended for camera).

**What to do:** tap a **sample tile** (Tomato · diseased, Potato · diseased, Healthy leaf, Blurry photo) to classify a real PlantVillage leaf image live, or tap **Scan a leaf** to use your camera. Toggle **हिंदी** for the full Hindi UI; tap **🔊 Listen** for spoken advice.

> First load downloads the ~17 MB model from a CDN once, then caches it (IndexedDB) — **every scan after that is fully offline.**

## What you'll see

| Sample | Result |
|---|---|
| Tomato · diseased | **Late blight, 99%** → 🔴 RED · "Spray protectant fungicide" + "Irrigate now" (soil 18% < 20%) |
| Healthy leaf | **Healthy, 98%** → 🟠 AMBER (bumped by low soil, *not* disease) |
| Blurry photo | **54% < 70% confidence gate** → "Retake photo" (never a confident wrong call) |

Inference runs in **~25–60 ms** on-device (shown live on the result card).

---

## How it works

```
 leaf image ──► TF.js MobileNet ──► label + confidence ─┐
 (camera/sample)   (on-device, 38-class)                │
                                                        ├─► rule engine ─► action + severity
 soil / temp / humidity ─────────────────────────────────┘   (FAO-56 MAD irrigation,
                                                              heat gate, confidence gate)
```

- **Preprocessing:** resize 224×224, normalize to [-1, 1], argmax over the 38-way softmax.
- **Confidence gate:** a disease call below 70% confidence is rejected with a "retake" prompt instead of guessing.
- **Irrigation logic:** soil moisture vs. crop threshold (irrigate < 20%, hold > 45%) — deterministic, not AI.
- **Offline:** model cached to IndexedDB, labels to localStorage; graceful fallback if the model can't load.

## Honest limitations

We state these upfront — they matter for real deployment:

- **Lab vs. field gap.** The model is trained on PlantVillage (clean single-leaf lab images). Accuracy on messy real-field photos is lower; the confidence gate is our guardrail against that.
- **Crop coverage.** 14 crops / 38 conditions (tomato, potato, pepper, corn, grape, apple…). **Cotton is not in the dataset** — we don't claim it.
- **Sensors** in this prototype are illustrative field readings; the hardware track wires real sensors on the edge device.

## Repository layout

```
prototype/        The working MVP (open index.html)
  index.html      Single-file SPA: TF.js inference + rule engine + bilingual UI
  rules.js        Advisory rules (reference)
research/         Problem research, UX notes, documentation
build/            Python scripts that generate the pitch deck
problem statement.txt   Official SIH PS 26180
```

## Credits & license

- Code: **MIT** (see [LICENSE](LICENSE)).
- Disease model: [Rishit-dagli/Greenathon-Plant-AI](https://github.com/Rishit-dagli/Greenathon-Plant-AI) (Apache-2.0), loaded at runtime.
- Demo images: [PlantVillage dataset](https://github.com/spMohanty/PlantVillage-Dataset).

*Built for SIH 2026 by the KISAN-EDGE team.*
