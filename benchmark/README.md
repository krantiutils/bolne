# NepTTS-Bench — Benchmark Suite

Evaluation benchmark for Nepali (and bilingual Nepali-English) text-to-speech systems. Organized by evaluation dimension with defined protocols and pass/fail thresholds.

## Benchmark Categories

### prosody/
Tests whether the TTS system produces correct and distinguishable prosodic patterns.

| File | What it tests |
|------|---------------|
| `nepali_contrastive_stress.json` | Stress/emphasis placement shifts meaning (focus, corrective, contrastive) |
| `nepali_question_intonation.json` | Rising/falling intonation for question types (yes/no, wh-, tag, rhetorical) |
| `nepali_emotion_sentences.json` | Emotional prosody (happy, sad, angry, surprised, neutral) |

### intelligibility/
Tests whether the TTS system correctly disambiguates and pronounces ambiguous text, and measures overall intelligibility via ASR round-trip.

| File | What it tests |
|------|---------------|
| `nepali_homographs.json` | Same spelling, different pronunciation/meaning based on context |
| `nepali_newspaper_ambiguities.json` | Real-world messy text from Nepali news (mixed scripts, abbreviations, numbers) |
| `asr_roundtrip_protocol.json` | ASR round-trip intelligibility: synthesize → transcribe → measure CER/WER |

### stability/
Tests whether the TTS system remains stable and intelligible under challenging conditions, including language boundaries.

| File | What it tests |
|------|---------------|
| `nepali_long_form_sentences.json` | Long utterances — tests for attention collapse, quality degradation over time |
| `nepali_robustness_tests.json` | Edge cases: tongue twisters, repetition, very short inputs, code-switching, rare words |
| `code_switching_protocol.json` | Nepali-English code-switching: voice quality, speaker identity, phonology, and transition smoothness at language boundaries |

### acoustic_quality/
Automated and human evaluation of synthesized audio signal quality.

| File | What it tests |
|------|---------------|
| `acoustic_quality_protocol.json` | DNSMOS P.835 (OVRL/SIG/BAK), UTMOS, SNR, LUFS, clipping, silence trimming, human MOS calibration |

### speaker_consistency/
Evaluation of speaker identity preservation between teacher and student models.

| File | What it tests |
|------|---------------|
| `speaker_consistency_protocol.json` | Speaker embedding similarity (ECAPA-TDNN), F0 consistency, speaking rate, cross-condition identity |

### latency/
On-device streaming performance — critical for the <500M parameter deployment goal.

| File | What it tests |
|------|---------------|
| `latency_protocol.json` | Time to first audio, real-time factor, peak memory, chunk boundary quality across hardware targets |

### phonological_accuracy/
The core differentiator for Nepali TTS — scoring whether phonological contrasts are produced correctly.

| File | What it tests |
|------|---------------|
| `phonological_accuracy_protocol.json` | ABX discrimination, forced alignment, perceptual confusion matrix for Nepali phonological contrasts (aspiration, retroflex, nasalization, gemination, schwa) |

### normalizer/
Tests whether the text normalization pipeline produces correct spoken forms.

| File | What it tests |
|------|---------------|
| `normalizer_accuracy_protocol.json` | Exact match accuracy for number, date, currency, time, phone, abbreviation, and percentage normalization |

## Dual-Purpose Files (in `data/`)

These files serve both the text normalizer / corpus generation pipeline **and** as benchmark evaluation inputs. They remain in `data/` and are referenced here by relative path.

| File | Normalizer use | Benchmark use |
|------|---------------|---------------|
| `../data/nepali_numbers.json` | Number-to-word conversion rules | Number verbalization accuracy |
| `../data/nepali_abbreviations.json` | Abbreviation expansion rules | Abbreviation reading accuracy |
| `../data/nepali_phone_number_patterns.json` | Phone number normalization | Phone number reading accuracy |
| `../data/nepali_time_expressions.json` | Time expression normalization | Time expression reading accuracy |
| `../data/phonological_minimal_pairs.json` | Phonological coverage for corpus | Phonological contrast accuracy |
| `../data/nepali_negation_patterns.json` | Negation pattern rules | Negation pattern reading accuracy |

## Metric Thresholds Summary

### Acoustic Quality

| Metric | Pass | Minimum | Unit |
|--------|------|---------|------|
| DNSMOS OVRL | >= 3.5 | >= 3.0 | MOS (1-5) |
| DNSMOS SIG | >= 3.5 | >= 3.0 | MOS (1-5) |
| DNSMOS BAK | >= 4.0 | >= 3.5 | MOS (1-5) |
| UTMOS | >= 4.0 | >= 3.5 | MOS (1-5) |
| SNR | >= 35 | >= 25 | dB |
| LUFS | -23 +/- 1 | — | LUFS |
| Clipping | < 0.01% | — | % samples |
| Silence (lead/trail) | <= 100ms | — | ms |
| Human MOS | >= 3.8 | >= 3.5 | MOS (1-5) |

### Speaker Consistency

| Metric | Pass | Minimum | Unit |
|--------|------|---------|------|
| Embedding sim (teacher-student) | >= 0.85 | >= 0.75 | cosine similarity |
| Embedding sim (student-student) | >= 0.90 | >= 0.80 | cosine similarity |
| F0 mean deviation | <= 15% | — | % of teacher |
| F0 std deviation | <= 25% | — | % of teacher |
| Speaking rate deviation | <= 15% | — | % of teacher |

### Intelligibility (ASR Round-Trip)

| Metric | Pass | Minimum | Unit |
|--------|------|---------|------|
| CER (overall) | <= 0.10 | <= 0.20 | ratio |
| WER (overall) | <= 0.15 | <= 0.25 | ratio |
| CER (phonological core) | <= 0.15 | <= 0.25 | ratio |
| CER (conversational) | <= 0.08 | <= 0.18 | ratio |

### Latency

| Metric | Pass (A10G) | Minimum (A10G) | Pass (Mobile) | Minimum (Mobile) | Unit |
|--------|-------------|----------------|---------------|-------------------|------|
| Time to first audio | <= 200 | <= 500 | <= 500 | <= 1000 | ms |
| Real-time factor | <= 0.5 | <= 1.0 | <= 1.0 | <= 2.0 | ratio |
| Peak memory (GPU) | <= 2 | <= 4 | — | — | GB |
| Peak memory (CPU) | — | — | <= 1 | <= 2 | GB |
| Chunk boundary delta | <= 0.3 | — | — | — | MOS |

### Phonological Accuracy (ABX Discrimination)

| Contrast Category | Pass | Minimum | Unit |
|-------------------|------|---------|------|
| 4-way aspiration (5 places) | >= 90% | >= 80% | % correct |
| Retroflex vs dental | >= 90% | >= 80% | % correct |
| Oral vs nasal vowels | >= 85% | >= 75% | % correct |
| Gemination | >= 85% | >= 75% | % correct |
| Schwa deletion | >= 80% | >= 70% | % correct |
| Human ABX (50-pair subset) | >= 90% | >= 80% | % correct |

### Normalizer Accuracy

| Metric | Pass | Minimum | Unit |
|--------|------|---------|------|
| Exact match (overall) | >= 98% | >= 95% | % |
| Exact match (per category) | >= 95% | >= 90% | % |

### Code-Switching

| Metric | Pass | Minimum | Unit |
|--------|------|---------|------|
| Boundary DNSMOS delta | <= 0.3 | — | MOS |
| Speaker sim across languages | >= 0.88 | >= 0.80 | cosine similarity |
| Phonology correctness | >= 85% | >= 75% | % correct |
| F0 jump at boundaries | <= 50 | — | Hz |

## Comparative Baselines

Each evaluation protocol should be run against multiple baselines to contextualize student model performance.

| Baseline | Description | Purpose |
|----------|-------------|---------|
| **Teacher (Gemini Flash 2.5 TTS)** | The teacher model used for distillation training data | Quality ceiling — student should approach teacher quality |
| **Google TTS `ne-NP`** | Google Cloud TTS Nepali voice | Commercial baseline — student should match or exceed |
| **Ground truth (human recordings)** | Native Nepali speaker recordings from the training corpus | Upper bound on naturalness and phonological accuracy |
| **Ablation: Layer 1+2 only** | Student model trained on only phonological core + conversational layers | Measures value added by edge cases, English, and prosody layers |

### Baseline Evaluation Procedure

1. Generate audio for the full evaluation set using each baseline system
2. Run all automated metrics (acoustic quality, speaker consistency, intelligibility, latency, phonological accuracy, normalizer)
3. Conduct human evaluations (MOS, ABX) using the same listener panels
4. Report per-metric comparison tables: student vs each baseline
5. Flag metrics where student falls below the commercial baseline (Google TTS `ne-NP`)

## Regression Tracking

Track benchmark results across model versions to detect quality regressions early.

### Version-Tagged Runs

Every benchmark evaluation run must be tagged with:
- **Model version**: checkpoint identifier (e.g., `v0.1.0`, `epoch-50`, commit hash)
- **Training data version**: corpus layer composition and total hours
- **Evaluation date**: ISO 8601 timestamp
- **Hardware**: inference hardware used for latency measurements
- **Protocol version**: git commit of the benchmark suite

### Per-Category Trend Monitoring

Maintain a time series of per-category aggregate scores across versions:

| Category | Tracked Metric | Granularity |
|----------|---------------|-------------|
| Acoustic quality | DNSMOS OVRL mean, UTMOS mean, Human MOS | Per checkpoint |
| Speaker consistency | Embedding sim mean (teacher-student) | Per checkpoint |
| Intelligibility | CER mean, WER mean | Per checkpoint |
| Latency | TTFA p50, RTF p50 | Per checkpoint |
| Phonological accuracy | Per-category ABX accuracy | Per checkpoint |
| Normalizer | Overall exact match % | Per normalizer change |
| Code-switching | Boundary DNSMOS delta mean, speaker sim mean | Per checkpoint |

### Regression Detection Rules

A **regression** is flagged when a new version shows statistically significant degradation on any metric:

1. **Hard regression**: any metric drops below its 'minimum' threshold → block release
2. **Soft regression**: any metric drops > 5% relative to the previous best version → investigate and document
3. **Category regression**: a specific category (e.g., aspiration accuracy) drops > 10% even if overall metrics hold → investigate phonological coverage
4. **Latency regression**: TTFA or RTF increases > 20% relative to previous version → profile and optimize before release

### Reporting Format

Store results in a structured format (JSON or CSV) indexed by model version:
```
results/
  v0.1.0/
    acoustic_quality.json
    speaker_consistency.json
    intelligibility.json
    latency.json
    phonological_accuracy.json
    normalizer.json
    code_switching.json
    summary.json          # aggregate pass/fail per category
  v0.2.0/
    ...
```

## Evaluation Protocol

1. **Generate audio** for all benchmark utterances using both teacher and student models
2. **Run automated metrics** (acoustic quality, speaker consistency, intelligibility, latency, phonological accuracy, normalizer) on all outputs
3. **Run prosody/intelligibility/stability** evaluation using the JSON test sets
4. **Human calibration** on stratified subsets: 100-sample (acoustic MOS), 200-sample (speaker consistency), 50-pair (phonological ABX)
5. **Teacher baseline** comparison — same protocol on Gemini output to quantify quality gap
6. **Comparative baselines** — run on Google TTS and ground truth recordings
7. **Report** per-category pass rates, aggregate statistics, teacher-student gap analysis, and regression status
