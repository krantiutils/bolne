# Nepali Streaming TTS — Distillation Pipeline Design

**Date:** 2026-02-28
**Author:** iggy (bolne/crew)
**Status:** Draft

---

## Goal

Distill Gemini Flash 2.5 TTS into a small (<500M param) on-device streaming TTS model for Nepali and English, optimized for conversational/assistant-style output. Single voice (bilingual). Budget: ~$300 for data generation.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data source | Gemini Flash 2.5 TTS API | Nepali supported (lang code `ne`), good quality |
| Data strategy | Structured core + natural bulk | Phonological coverage + volume |
| Target deployment | On-device, <500M params | Edge-first, cloud is trivially easy later |
| Speaker count | Single speaker (first) | Simpler model, consistent quality, max hours |
| Use case | Conversational / assistant-style | Short natural dialogue turns |
| Budget allocation | ~$300 → data generation | Training on AWS g5.12xlarge (4x A10G) |

## Architecture Overview

```
                    DISTILLATION PIPELINE
                    =====================

  ┌─────────────┐    ┌──────────────────┐    ┌───────────────┐
  │ Text Corpus │───▶│ Text Normalizer  │───▶│ Gemini Flash  │
  │ (3 layers)  │    │ (rule-based)     │    │ 2.5 TTS API   │
  └─────────────┘    └──────────────────┘    └──────┬────────┘
                                                     │
                                                     ▼
                                             ┌───────────────┐
                                             │  Raw Audio     │
                                             └──────┬────────┘
                                                     │
                                                     ▼
                                             ┌───────────────┐
                                             │  Validation    │
                                             │  Pipeline      │
                                             └──────┬────────┘
                                                     │
                                                     ▼
                                             ┌───────────────┐
                                             │ Final Dataset  │
                                             │ (text, audio)  │
                                             └───────────────┘
```

---

## 1. Text Corpus Design

Four layers, ~50,000 utterances total (Nepali + English), targeting ~65-90 hours of audio.
All generated from the **same Gemini voice** for consistency.

### Layer 1 — Phonological Core (~2,000 sentences)

Directly derived from NepTTS-Bench. Each sentence isolates one phonological contrast.

| Category | Count | Notes |
|----------|-------|-------|
| 4-way aspiration (5 places × 4 types × ~3 sentences) | ~60 | All of क/ख/ग/घ, च/छ/ज/झ, ट/ठ/ड/ढ, त/थ/द/ध, प/फ/ब/भ |
| Oral vs nasal vowels | ~55 | 6 oral + 5 nasal, minimal pair sentences |
| Retroflex vs dental | ~50 | त/ट, द/ड pairs in natural sentences |
| Gemination (lexical + productive) | ~60 | चपल/चप्पल type + emphatic doubling |
| Schwa deletion (clear + borderline) | ~100 | Including Hindi-influenced variants |
| Nasal consonants (5 places) | ~50 | All environments, agnostic to 3-vs-5 debate |
| Negation morphology | ~60 | Prefix/suffix, polar/vector/copula verbs |
| Prosody (4 intonation patterns) | ~100 | Rising, falling, rising-falling, falling-rising |
| Numbers/dates/abbreviations | ~200 | Verbalized forms |
| Ambiguity / newspaper challenge | ~100 | Real-world messy input |
| Buffer for gaps | ~1,165 | Discovered during curation |
| **Total** | **~2,000** | |

**Source:** Linguist-curated. All sentences must sound like natural Nepali speech.

### Layer 2 — Conversational Bulk (~35,000 utterances)

Short, natural dialogue turns. Target 3-8 seconds each.

| Type | Count | Source |
|------|-------|--------|
| Greetings / pleasantries | ~2,000 | Templates + LLM generation |
| Questions (info-seeking) | ~8,000 | Nepali QA datasets, LLM-generated |
| Answers / explanations | ~8,000 | Paired with questions |
| Instructions / directions | ~5,000 | How-to, navigation, recipes |
| Emotional range (happy, sad, urgent, calm) | ~4,000 | LLM-generated with emotion tags |
| Filler / backchannels | ~2,000 | हजुर, हो, अँ, ठीक छ, etc. |
| Mixed (English loanwords) | ~3,000 | Tech, daily life code-switching |
| General short statements | ~3,000 | Facts, opinions, summaries |
| **Total** | **~35,000** | |

### Layer 3 — Edge Cases (~3,000 utterances)

All text pre-normalized to spoken form before TTS.

| Category | Count |
|----------|-------|
| Number verbalization (various formats) | ~500 |
| Dates (BS and AD, numeric reading) | ~300 |
| Abbreviations | ~300 |
| Phone numbers (all 3 reading patterns) | ~300 |
| English words in Nepali context | ~500 |
| Addresses / place names | ~300 |
| Prices (रु. format) | ~300 |
| Mixed / compound cases | ~500 |

### Layer 4 — English Conversational (~10,000 utterances)

Same Gemini voice, English language. Enables bilingual capability.

| Type | Count | Source |
|------|-------|--------|
| Greetings / pleasantries | ~1,000 | Templates + LLM generation |
| Questions / answers | ~3,000 | Conversational QA |
| Instructions / directions | ~2,000 | How-to, technical |
| Code-switching (Nepali-English mix) | ~2,000 | Natural bilingual dialogue |
| General short statements | ~2,000 | Facts, opinions, summaries |
| **Total** | **~10,000** | |

**Rationale:** Nepali conversational speech naturally mixes English. Training on
both languages from the same voice ensures the model handles code-switching
smoothly without voice identity shifts.

---

## 2. Text Normalization Pipeline

Fully rule-based. No LLM needed — all categories are deterministic.

```
Raw text
  │
  └─▶ Rule-based normalizer (free, deterministic, fast)
        ├─ Numbers: १०१ → एक सय एक
        ├─ Currency: रु. ५०० → पाँच सय रुपैयाँ
        ├─ Dates: २०८१/१०/१५ → दुई हजार एकासी साल दस महिना पन्ध्र गते
        │         (numeric reading — no BS/AD detection needed)
        ├─ Time: ५:३० → पाँच बजेर तीस मिनेट
        ├─ Phone numbers: ९८४१-२३४५६७ → digit by digit
        ├─ Percentages: २०% → बीस प्रतिशत
        └─ Abbreviations: ने.क.पा. → ने का पा (spell out letters, don't expand)

Date format: {year} साल {month} महिना {day} गते
             All numbers converted via number-to-word rules.
             No month name lookup needed — works for both BS and AD.
```

### Nepali Number-to-Word Rules

Rule-based converter for Nepali numerals. Key patterns:
- Units: शून्य, एक, दुई, तीन, चार, पाँच, छ, सात, आठ, नौ
- Teens/twenties: Nepali has unique words (not compositional) — एघार, बाह्र, ... उन्नाइस
- Tens: बीस, तीस, चालीस, पचास, साठी, सत्तरी, अस्सी, नब्बे
- Powers: सय (100), हजार (1,000), लाख (100,000), करोड (10,000,000)
- South Asian grouping: 12,34,567 not 1,234,567

---

## 3. Gemini TTS API Integration

### Voice Selection

Pick one Gemini HD voice that sounds best for Nepali. Process:
1. Generate a test set of ~20 sentences across all phonological categories
2. Run through all 30 Gemini HD voices with `ne` language code
3. Evaluate: naturalness, pronunciation accuracy, consistency
4. Select one voice for full generation

### API Configuration

```python
# Key from .env: GEMINI_KEY
# Model: gemini-2.5-flash-preview-tts
# Language: ne (Nepali)
# Single voice: TBD after voice selection
```

### Batching Strategy

- Batch size: ~100 utterances per API call batch
- Rate limiting: respect Gemini API quotas
- Checkpoint: save progress every batch (resume on failure)
- Estimated total API calls: ~40,000

### Cost Estimate

| Component | Cost |
|-----------|------|
| Text input (~50K utterances, ~250K tokens total) | ~$0.15 |
| Audio output (~65-90 hours, TBD token rate) | ~$180-300 |
| Text normalization (rule-based) | $0 |
| **Total estimate** | **~$180-300** |

Run a calibration batch of 100 utterances first to pin down exact audio token rate.

---

## 4. Validation Pipeline

Every generated audio file goes through quality checks before entering the final dataset.

### Stage 1: Sanity Checks (rule-based, free)
- Audio duration within expected range (0.5s - 30s)
- No silence-only files
- Sample rate / format validation
- File integrity

### Stage 2: ASR Round-Trip Validation
- Run generated audio through Nepali ASR (Whisper or similar)
- Compare ASR transcription to input text
- Flag mismatches above threshold (CER > 0.2)
- Manual review of flagged items

### Stage 3: Audio Quality
- DNSMOS P.835 scoring (target OVRL > 3.0)
- Signal-to-noise ratio check
- Consistent volume normalization

### Expected Yield
- Input: ~50,000 utterances (~40K Nepali + ~10K English)
- After filtering: ~45,000-48,000 (5-10% rejection rate expected)
- Final dataset: ~60-85 hours of validated (text, audio) pairs

---

## 5. Output Format

```
dataset/
├── metadata.jsonl          # {id, text, normalized_text, audio_path, duration_s, layer}
├── audio/
│   ├── phon_0001.wav       # Layer 1: phonological core
│   ├── conv_0001.wav       # Layer 2: conversational (Nepali)
│   ├── edge_0001.wav       # Layer 3: edge cases
│   └── en_0001.wav         # Layer 4: English conversational
└── splits/
    ├── train.jsonl          # 90%
    ├── val.jsonl            # 5%
    └── test.jsonl           # 5% (stratified by layer)
```

Test split stratified to ensure phonological core sentences appear in test set — enables direct NepTTS-Bench evaluation.

---

## 6. Model Architecture (Deferred)

Architecture selection deferred until data is generated. Top candidates:

| Model | Params | Architecture | Streaming latency |
|-------|--------|-------------|-------------------|
| Spark-TTS | ~500M | Pure LLM (Qwen2.5) + BiCodec | Partial |
| VibeVoice-0.5B | 500M | Next-token diffusion, 7.5Hz | ~300ms |
| Mini CosyVoice | ~300-500M | Small AR + chunked flow matching | ~150ms |

Decision will be informed by data quality and volume achieved.

---

## 7. Training Environment

- **Hardware:** AWS g5.12xlarge (4x NVIDIA A10G, 96GB total GPU memory)
- **Strategy:** PEFT/LoRA fine-tuning on chosen base model
- **Data:** Distilled dataset from this pipeline

---

## 8. Quality Gate

Before committing the full $300 budget, run a small calibration batch:

1. Generate ~50 utterances across all layers (~$1-2)
2. Evaluate Gemini's Nepali pronunciation quality (native speaker review)
3. Pin down exact audio token rate → refine cost estimate
4. Test text normalization pipeline end-to-end
5. Validate ASR round-trip works for Nepali

**Go/no-go decision based on calibration results.**

---

## 9. Text Corpus Sourcing

The agent (iggy) curates the text corpus **sentence by sentence**. No bulk scraping.

### Layer 1 — Phonological Core
- Hand-crafted based on NepTTS-Bench phonological categories
- Each sentence isolates one contrast, reviewed for naturalness
- Cross-referenced against linguist feedback

### Layer 2 — Conversational Bulk
- Agent generates sentences one by one, covering all subcategories
- Sources for inspiration: Nepali dialogue patterns, common phrases, daily scenarios
- Each sentence reviewed for naturalness — must sound like real Nepali conversation
- No machine-translated English. Native Nepali phrasing only.

### Layer 3 — Edge Cases
- Hand-crafted for each normalization category
- Covers all number/date/abbreviation patterns
- Pre-normalized text paired with original written form

### Layer 4 — English Conversational
- Agent generates natural English dialogue turns
- Code-switching subset: natural Nepali-English mixing patterns

### Train/Test Separation
- NepTTS-Bench sentences are **excluded** from training data entirely
- Test split drawn from held-out sentences per layer
- Phonological core test sentences are separate from benchmark sentences

---

## 10. Audio Format Specification

| Parameter | Value |
|-----------|-------|
| Format | WAV (PCM) |
| Sample rate | 24kHz (standard for modern TTS) |
| Bit depth | 16-bit |
| Channels | Mono |
| Silence trimming | Strip leading/trailing silence > 100ms |
| Volume normalization | -23 LUFS (EBU R128) |

---

## 11. Evaluation Plan

### During Distillation (data quality)
- ASR round-trip CER < 0.2 per utterance
- DNSMOS OVRL > 3.0 per utterance
- Native speaker spot-check (~5% sample)

### After Model Training
- **NepTTS-Bench** — phonological accuracy across all contrast categories
- **MOS** — Mean Opinion Score from native Nepali speakers (naturalness)
- **Streaming metrics** — first-packet latency, real-time factor
- **ASR round-trip CER** — on held-out test set
- **English baseline** — compare against base model's English quality (should not degrade)

---

## 12. Open Questions

1. Which Gemini voice sounds best for Nepali? (requires voice selection experiment)
2. Exact audio token rate for cost pinning (requires calibration batch)
3. Nepali number words for 21-99 — need complete lookup table with all irregular forms
4. Final model architecture — decide after data is ready
5. NepTTS-Bench benchmark sentences — depends on linguist collaboration timeline
6. OpenSLR Nepali data — evaluate quality, decide if usable for supplementary training later
