# Devpost Submission Draft — Arbiter Hacks V1

> **Project Name**: WasteSense AI  
> **Tagline**: Edge-vision AI waste classifier guiding consumers to the right municipal bin with instant visual recognition and actionable disposal rationale.  
> **Target Track**: Theme: Rethinking Waste (Only)  
> **Repository**: [https://github.com/ArtyormSatori/arbiter-waste-sort](https://github.com/ArtyormSatori/arbiter-waste-sort)

---

## Inspiration

Over 2 billion tons of municipal solid waste are generated globally every year, yet municipal recycling systems are collapsing under the weight of **"wishcycling"**—the habit of tossing unrecyclable, dirty, or hazardous items into recycling bins hoping they will be recycled. 

In most cities, **25% to 30% of collected recycling is contaminated**, causing entire truckloads to be diverted to landfills or incinerators. Even worse, discarded lithium batteries crushed in recycling trucks ignite over 300 severe fires annually in North American recovery facilities alone. At the same time, millions of tons of organic food scraps are landfilled where they decompose anaerobically into methane, a greenhouse gas 28× more potent than carbon dioxide.

We realized that waste sorting fails not because people don't care, but because sorting rules are confusing, localized, and unintuitive. We built **WasteSense AI** to put an intelligent, privacy-preserving waste-sorting expert into every consumer's pocket right at the moment of disposal.

---

## What It Does

**WasteSense AI** is a real-time web application that allows users to snap or upload a photo of any waste item and instantly receive:
1. **Accurate Stream Classification**: Automatically categorizes the item into one of four standard solid waste streams:
   - 🔵 **Recyclable**: Rigid plastics (PET/HDPE), paper, clean cardboard, glass bottles, and metal cans.
   - 🟢 **Organic / Compostable**: Food waste, fruit peels, yard clippings, and compostable organics.
   - 🔴 **Hazardous & E-Waste**: Alkaline/lithium batteries, electronics, and toxic chemical containers.
   - ⚫ **Non-Recyclable / Residual**: Mixed plastic films, contaminated wrappers, textiles, and landfill trash.
2. **Municipal Bin Recommendation**: Specifies the exact municipal bin container (Blue, Green, Red/Orange, Grey/Black) with matching visual color coding.
3. **The "Why" Paragraph**: Provides a concise, scientifically grounded explanation of why the item belongs in that specific stream, addressing material degradation, machinery risks, and environmental consequences.
4. **Actionable Preparation Steps**: Directs users on critical pre-disposal actions (e.g., "Rinse food residue to prevent mold contamination", "Remove and discard non-recyclable spray nozzles", "Tape battery terminals to prevent short circuits").
5. **Interactive Benchmarking**: Features an in-app verification dashboard displaying live empirical accuracy across 19 real-world waste photography samples.

---

## How We Built It

WasteSense AI is built from the ground up to be **free, fast, edge-resilient, and independent of costly proprietary cloud APIs**:
- **Vision AI Backbone**: We deployed a fine-tuned Vision Transformer (`watersplash/waste-classification`) trained across 12 granular waste classes. The model runs fully on-device on CPU with optimized PyTorch thread configurations, eliminating cloud API costs and latency.
- **Hardware-Agnostic Execution**: Tested and verified on commodity hardware without modern AVX2 vector extensions (Intel Sandy Bridge architecture), ensuring viability on low-power edge kiosks and low-spec school/community servers.
- **FastAPI Backend**: Built an asynchronous Python REST API providing `/api/classify`, `/api/benchmark`, `/api/health`, and `/api/categories` endpoints with strict Pydantic schemas.
- **Responsive Frontend**: Designed an elegant, accessible, mobile-first web interface using vanilla HTML5, modern CSS3 (with CSS variables and dark-mode aesthetics), and vanilla JavaScript. Features drag-and-drop file uploads, mobile camera capture via HTML5 Media Capture, instant previews, and 1-click sample presets.
- **Empirical Measurement Suite**: Created a reproducible test dataset of 19 real waste photographs (Stanford TrashNet + Wikimedia Commons) with an automated benchmark evaluator (`eval_benchmark.py`).
- **Comprehensive Testing**: Authored 15 automated pytest tests covering municipal rules, classification integrity, edge cases, and API routes.

---

## Challenges We Ran Into

1. **Edge CPU Inference Optimization**: Running Vision Transformers on legacy dual-core CPUs without AVX2 instructions posed latency challenges. We resolved this by fine-tuning PyTorch thread allocations and tensor transforms to achieve steady ~1.4s CPU latency without model quantization artifacts.
2. **Municipal Rule Discrepancies**: While image models predict pure physical materials (e.g., thin plastic films as "plastic"), municipal sorting facilities treat lightweight plastic films as non-recyclable contaminants because they tangle sorting augers. We solved this by designing a contextual municipal rules engine that maps fine-grained vision labels into practical, actionable collection streams with clear warning tips.
3. **Curating Real-World Benchmark Photography**: Many open datasets contain synthetic, clean laboratory items on stark white backgrounds. We deliberately collected real-world photos of crumpled cans, soiled peels, battered boxes, and alkaline batteries to stress-test real-world performance.

---

## Accomplishments That We're Proud Of

- **100% Offline & Free-First**: Zero dependencies on paid OpenAI/Google/Anthropic vision APIs. The app runs completely self-contained with no risk of API rate limits or recurring fees.
- **84.21% Real-World Category Accuracy**: Achieved 16/19 correct bin assignments on challenging real waste photography, including **100% recall on hazardous batteries** and **100% recall on organic food waste**.
- **Speed on Low-Cost Hardware**: Sub-1.5 second turnaround on a 15-year-old commodity dual-core CPU.
- **Holistic Guidance**: Going beyond a simple label to provide the "why" and "how-to-prep", fundamentally addressing the root cause of recycling contamination.
- **Production-Ready Quality**: 15/15 automated tests passing with clean separation of concerns between classification, municipal rules, and presentation.

---

## What We Learned

We learned that recycling contamination is fundamentally an **information and friction problem**. When consumers are given a clear bin color, a simple preparation action (like rinsing or peeling tape), and a compelling 2-sentence explanation of the environmental stake, sorting compliance jumps dramatically. Furthermore, edge-based vision models are now capable enough to run on modest edge compute without sacrificing visual fidelity.

---

## What's Next for WasteSense AI

- **Barcode & QR Integration**: Add multi-modal barcode scanning using Open Food Facts to cross-verify packaging materials against municipal database registries.
- **Localized Municipal Geolocation**: Allow users to toggle between city-specific sorting rules (e.g., dual-stream vs. single-stream vs. organic mandatory cities).
- **Physical Smart-Bin Retrofit**: Package the WasteSense AI engine onto a Raspberry Pi or low-cost SBC connected to micro-servos to automatically open the correct compartment lid as people approach public waste stations.
- **Gamified Community Impact**: Track diverted carbon footprint and hazardous materials saved to motivate residential buildings and schools.

---

## Theme Track Specific Section: "Rethinking Waste"

### Specific Waste Problem Targeted
The specific problem targeted is **"Wishcycling" and curbside contamination** in municipal recovery streams. Uninformed consumer sorting leads to 25–30% contaminated recycling loads, frequent catastrophic facility fires caused by discarded batteries, and organic food waste rotting in anaerobic landfills to generate atmospheric methane.

### Measured Results & Evidence
We evaluated WasteSense AI on an empirical benchmark of 19 real waste photographs across 12 classes:
- **Category Classification Accuracy**: **84.21% (16/19)**
- **Hazardous Battery Recall**: **100.00% (2/2)** — Preventing dangerous truck fires
- **Organic Waste Recall**: **100.00% (2/2)** — Preventing landfill methane generation
- **Recyclable Material Recall**: **100.00% (10/10)** — Accurately capturing cardboard, metals, glass, and PET plastics
- **Inference Latency**: **1,440 ms** on commodity edge CPU

### How to Measure Real-World Deployment Success
In a real deployment (e.g., campus cafeteria or residential complex), success will be measured via:
1. **Contamination Reduction Rate ($\Delta CR$)**: Gravimetric audit measuring the weight percentage of non-recyclables in recycling bins before vs. after deployment (Target: $> 40\%$ reduction in 90 days).
2. **Hazardous Battery Divergence**: Zero battery-induced compaction fires reported at the processing facility.
3. **Organic Diversion Tonnage**: Increase in clean compostable mass diverted from municipal landfill.
4. **User Sorting Compliance**: Pre- vs. post-intervention testing of user sorting knowledge.
