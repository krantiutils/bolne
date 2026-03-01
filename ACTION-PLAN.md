# NepTTS-Bench Action Plan

Full project roadmap from MOS data collection through paper submission to Nepali TTS training and deployment.

---

## Current State (March 1, 2026)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| Benchmark runner (generate, ASR, ABX, FSD, DNSMOS) | Done | `benchmark/runner/run_benchmark.py` |
| Edge TTS baseline (Hemkala, 477 items) | Done | `benchmark/results/edge-tts-ne-np-hemkalaneural/` |
| Reference data (482 test items, 8 categories) | Done | `data/` |
| FSD reference stats (2,000 OpenSLR-54 files) | Done | `benchmark/runner/ref_stats_clsril23.npz` |
| MOS predictor architecture (XLS-R + phoneme branch) | Done | `benchmark/mos/model/mos_predictor.py` |
| MOS training pipeline (BVCC pretrain + Nepali fine-tune) | Done | `benchmark/mos/model/train.py` |
| Recording app (FastAPI + SQLite + Docker) | Done | `benchmark/mos/recording_app/` |
| Paper draft (Introduction through Benchmark Design) | Done | `paper/neptts-bench.tex` |
| G2P pipeline (eSpeak-NG + Epitran fallback) | Done | `benchmark/mos/g2p.py` |
| Multi-system audio generation script | Done | `benchmark/mos/generate_multisystem.py` |

### Known Limitations

- **ASR metrics unreliable**: Whisper (small) CER = 0.46 on Nepali — too weak for round-trip evaluation
- **ABX at chance level**: 48.5% accuracy with Whisper embeddings — doesn't capture Nepali phonological contrasts
- **FSD corpus-level only**: No per-utterance naturalness score
- **DNSMOS language-agnostic**: Signals audio quality but not linguistic naturalness

---

## Phase 1: MOS Data Collection (Weeks 1–3)

**Goal**: Collect human MOS ratings from 15–20 native Nepali speakers across 3+ TTS systems.

### Tasks

- [ ] Deploy recording app to cloud with HTTPS (Fly.io or Railway)
- [ ] Generate multi-system stimuli: Edge TTS, ground truth (OpenSLR-54), at least one more system
- [ ] Recruit 15–20 native Nepali speakers (target: university students, remote workers)
- [ ] Each listener rates ~60 stimuli (20 per system × 3 systems, randomized)
- [ ] Monitor inter-rater reliability: Krippendorff's alpha ≥ 0.6

### Quality Gate

At **10 completed listeners**, check:
- Krippendorff's alpha ≥ 0.6 → continue to 15–20
- Alpha < 0.5 → investigate: bad stimuli? unclear instructions? recruit more carefully

### Deliverables

- Raw ratings in SQLite (`benchmark/mos/recording_app/data/`)
- Exported ratings JSON via admin API
- Inter-rater reliability report

---

## Phase 2: Run Full Baselines (Weeks 2–4, overlaps Phase 1)

**Goal**: Benchmark all available TTS systems on the full NepTTS-Bench suite.

### Systems to Benchmark

| System | Method | Priority |
|--------|--------|----------|
| Edge TTS (Hemkala) | Already done | — |
| OpenSLR-54 ground truth | Select matching sentences, extract audio | High |
| Google Cloud TTS (ne-NP) | API call, WaveNet voice | High |
| Gemini Flash 2.5 TTS | API call via Google AI Studio | High |
| MMS-TTS Nepali | `facebook/mms-tts-npi` from HuggingFace | Medium |

### Tasks

- [ ] Write ground truth extraction script (match test sentences → OpenSLR-54 utterances)
- [ ] Add Google Cloud TTS generator to `generate_audio.py`
- [ ] Add Gemini Flash 2.5 TTS generator
- [ ] Add MMS-TTS generator (local inference)
- [ ] Run full benchmark pipeline on each system
- [ ] Build cross-system comparison tables

### Deliverables

- `benchmark/results/<system>/` for each system (manifest, quality, ASR, ABX, FSD)
- Comparison CSV/JSON with all systems side-by-side

---

## Phase 3: MOS Predictor Training (Weeks 4–5)

**Goal**: Train a Nepali-aware MOS predictor that correlates with human ratings.

### Tasks

- [ ] Aggregate final ratings using `benchmark/mos/aggregate_ratings.py`
- [ ] Train/val/test split (stratified by system, 70/15/15)
- [ ] Optional: Pretrain on BVCC (English MOS data) for representation learning
- [ ] Fine-tune on collected Nepali ratings
- [ ] Evaluate: LCC ≥ 0.8 with human MOS, correct system ranking order
- [ ] If LCC < 0.7: try simpler model (linear probe on XLS-R), more data, or data augmentation

### Architecture Recap

```
Audio → XLS-R 300M (frozen initially) → frame features
                                              ↓
Text → G2P → phoneme embeddings → cross-attention with frame features
                                              ↓
                                        MOS prediction head → scalar MOS
```

### Deliverables

- Trained model checkpoint at `benchmark/mos/model/checkpoints/`
- Validation metrics (LCC, SRCC, MSE) logged
- Per-system predicted MOS vs. human MOS correlation plot

---

## Phase 4: Paper Finalization & Submission (Weeks 5–7)

**Goal**: Complete and submit the NepTTS-Bench paper to Interspeech 2026.

### Tasks

- [ ] Fill results tables (Tables 5–6 in `paper/neptts-bench.tex`) with baseline + MOS data
- [ ] Write Results section: per-metric analysis, system rankings, metric correlation
- [ ] Write Discussion: what metrics agree/disagree, ASR/ABX limitations, MOS predictor validity
- [ ] Add MOS predictor architecture figure
- [ ] Switch to final Interspeech 2026 template (template files in `paper/`)
- [ ] Proofread, check page limit, verify all references
- [ ] Submit to Interspeech 2026
- [ ] Upload arXiv preprint

### Key Results to Report

| Metric | Edge TTS (current) | Ground Truth | Google Cloud | Gemini | MMS |
|--------|--------------------:|-------------:|-------------:|-------:|----:|
| DNSMOS OVRL | 3.095 | ? | ? | ? | ? |
| FSD | 6.63 | ? | ? | ? | ? |
| CER | 0.461 | ? | ? | ? | ? |
| Human MOS | ? | ? | ? | ? | ? |
| Predicted MOS | ? | ? | ? | ? | ? |

### Deliverables

- Submitted paper (Interspeech 2026)
- arXiv preprint
- Camera-ready materials

---

## Phase 5: Nepali TTS Fine-Tuning (Weeks 8–16)

**Goal**: Build a competitive Nepali TTS system, evaluated with NepTTS-Bench.

### Data Preparation

- [ ] Download full OpenSLR-54 (all 16 shards, ~150 hours Nepali speech)
- [ ] Download OpenSLR-43 (Nepali read speech) and OpenSLR-143 (Nepali conversational)
- [ ] Build text normalization pipeline (numbers, dates, abbreviations, English loanwords)
- [ ] Build G2P pipeline (extend `benchmark/mos/g2p.py` with schwa deletion rules)
- [ ] Create train/val/test splits (speaker-disjoint)
- [ ] Validate alignment quality (discard utterances with poor forced alignment)

### Option A: VITS / MMS Fine-Tuning (recommended first)

- [ ] Start from `facebook/mms-tts-npi` checkpoint
- [ ] Fine-tune on OpenSLR-54 with Nepali phoneme set
- [ ] Evaluate at checkpoints 10k, 25k, 50k, 100k steps
- [ ] Run NepTTS-Bench after each checkpoint

### Option B: Matcha-TTS from Scratch

- [ ] Prepare phoneme-aligned dataset (Montreal Forced Aligner)
- [ ] Train Matcha-TTS with Nepali phoneme vocabulary
- [ ] Pair with HiFi-GAN vocoder (pretrained or Nepali-fine-tuned)
- [ ] Evaluate with NepTTS-Bench

### Deliverables

- Trained TTS model checkpoints
- NepTTS-Bench results for each checkpoint
- Training logs and learning curves

---

## Phase 6: Distillation & Deployment (Weeks 16+)

**Goal**: Create a fast, deployable Nepali TTS model suitable for real-time use.

### Tasks

- [ ] Generate teacher audio via Gemini Flash 2.5 (5,000+ utterances)
- [ ] Train student model on teacher audio (<500M parameters)
- [ ] Optimize for streaming: target TTFA (Time to First Audio) < 500ms
- [ ] Export to ONNX for on-device inference
- [ ] Benchmark latency on target hardware (CPU, mobile)
- [ ] Final NepTTS-Bench evaluation of distilled model

### Deliverables

- Distilled model checkpoint + ONNX export
- Latency benchmarks (TTFA, RTF)
- NepTTS-Bench comparison: teacher vs. student

---

## Dependency Graph

```
Phase 1 (MOS Collection) ──────────────────────┐
                                                ├──→ Phase 3 (MOS Predictor)
Phase 2 (Baselines) ───────────────────────────┘          │
                                                           ↓
                                                 Phase 4 (Paper) ──→ Submit
                                                           │
                                                           ↓
                                                 Phase 5 (Fine-Tuning)
                                                           │
                                                           ↓
                                                 Phase 6 (Distillation)
```

Phases 1 and 2 run in parallel. Phase 3 requires data from both. Phase 4 requires results from Phase 3. Phases 5 and 6 are post-paper.

---

## Timeline Summary

| Phase | Weeks | Key Milestone |
|-------|-------|---------------|
| 1: MOS Data Collection | 1–3 | 15+ listener ratings collected |
| 2: Full Baselines | 2–4 | All systems benchmarked |
| 3: MOS Predictor | 4–5 | Predictor trained, LCC ≥ 0.8 |
| 4: Paper | 5–7 | Interspeech 2026 submission |
| 5: TTS Fine-Tuning | 8–16 | Competitive Nepali TTS model |
| 6: Distillation | 16+ | Deployable streaming TTS |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Too few MOS raters (<10 speakers) | Medium | High | Start recruiting early; offer compensation; have backup pool |
| Low inter-rater agreement (alpha < 0.5) | Medium | High | Improve instructions, add training examples, screen raters |
| Whisper ASR too poor for Nepali CER metric | Confirmed | Medium | Report as limitation; rely on DNSMOS + FSD + MOS; explore NeMo Nepali ASR |
| MOS predictor doesn't generalize (LCC < 0.7) | Medium | Medium | Fall back to BVCC-pretrained UTMOS; report human MOS only |
| Interspeech deadline pressure | Low | High | Prioritize Phases 1–4; Phases 5–6 are post-submission |
| OpenSLR-54 alignment quality issues | Low | Medium | Use Montreal Forced Aligner with Nepali acoustic model; manual spot-check |
