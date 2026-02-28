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
Tests whether the TTS system correctly disambiguates and pronounces ambiguous text.

| File | What it tests |
|------|---------------|
| `nepali_homographs.json` | Same spelling, different pronunciation/meaning based on context |
| `nepali_newspaper_ambiguities.json` | Real-world messy text from Nepali news (mixed scripts, abbreviations, numbers) |

### stability/
Tests whether the TTS system remains stable and intelligible under challenging conditions.

| File | What it tests |
|------|---------------|
| `nepali_long_form_sentences.json` | Long utterances — tests for attention collapse, quality degradation over time |
| `nepali_robustness_tests.json` | Edge cases: tongue twisters, repetition, very short inputs, code-switching, rare words |

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

## Evaluation Protocol

1. **Generate audio** for all benchmark utterances using both teacher and student models
2. **Run automated metrics** (acoustic quality + speaker consistency) on all outputs
3. **Run prosody/intelligibility/stability** evaluation using the JSON test sets
4. **Human calibration** on stratified 100-sample (acoustic) and 200-sample (speaker) subsets
5. **Teacher baseline** comparison — same protocol on Gemini output to quantify quality gap
6. **Report** per-category pass rates, aggregate statistics, and teacher-student gap analysis
