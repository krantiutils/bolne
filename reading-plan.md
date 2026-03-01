# TTS Reading Plan: From Foundations to Nepali TTS

A structured learning path for someone with basic ML knowledge (understands backprop, CNNs, RNNs, loss functions) but no DSP or deep generative model background. Mixed media: papers, videos, blogs, notebooks.

**Total estimate: ~80 hours** (or ~20h via the Fast Path at the end)

Tags:
- **[KEY]** — Essential, do not skip
- **[DEEP]** — Optional depth, read if the topic interests you or becomes relevant

---

## Phase 0: Prerequisites (~15h)

### 0A: Audio & DSP Fundamentals

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 1 | [3Blue1Brown — But what is the Fourier Transform?](https://www.youtube.com/watch?v=spUNpyF58BY) | Video | 20 min | [KEY] |
| 2 | [Mike X Cohen — Understanding the FFT Algorithm](https://www.youtube.com/watch?v=h7apO7q16V0) | Video | 30 min | [KEY] |
| 3 | [Librosa tutorial: loading audio, spectrograms, mel-filterbanks](https://librosa.org/doc/latest/tutorial.html) | Notebook | 2h | [KEY] |
| 4 | [Stanford CS224S Lecture 1–2: Speech Processing Fundamentals](https://web.stanford.edu/class/cs224s/) | Video + Slides | 3h | [KEY] |
| 5 | [Lilian Weng — "Speech Synthesis" (2024)](https://lilianweng.github.io/posts/2024-11-22-speech/) | Blog | 2h | [KEY] |

After this block you should be comfortable with: waveforms, sampling rate, spectrograms, mel scale, STFT, and the overall TTS pipeline (text → acoustic model → vocoder → waveform).

### 0B: Deep Learning for Generative Models

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 6 | [Vaswani et al. — "Attention Is All You Need" (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762) | Paper | 2h | [KEY] |
| 7 | [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | Blog | 1h | [KEY] |
| 8 | [Lilian Weng — "What are Diffusion Models?" (2021)](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) | Blog | 2h | [KEY] |
| 9 | [Doersch — Tutorial on Variational Autoencoders (arXiv:1606.05908)](https://arxiv.org/abs/1606.05908) | Paper | 2h | [KEY] |
| 10 | [Kobyzev et al. — Normalizing Flows: An Introduction and Review (arXiv:1908.09257)](https://arxiv.org/abs/1908.09257) | Survey | 1.5h | [DEEP] |
| 11 | [Yannic Kilcher — VITS Walkthrough](https://www.youtube.com/watch?v=gAEcymGVOxA) | Video | 40 min | [DEEP] |

After this block you should understand: self-attention, encoder-decoder, VAEs (ELBO, reparameterization trick), diffusion (forward/reverse process), and have a rough idea of normalizing flows.

---

## Phase 1: The Classics (~10h)

The autoregressive era. These models are no longer SOTA but every modern system builds on their ideas.

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 12 | [van den Oord et al. — WaveNet: A Generative Model for Raw Audio (arXiv:1609.03499)](https://arxiv.org/abs/1609.03499) | Paper | 2h | [KEY] |
| 13 | [DeepMind WaveNet Blog Post + Audio Demos](https://deepmind.google/discover/blog/wavenet-a-generative-model-for-raw-audio/) | Blog | 30 min | [KEY] |
| 14 | [Wang et al. — Tacotron: Towards End-to-End Speech Synthesis (arXiv:1703.10135)](https://arxiv.org/abs/1703.10135) | Paper | 2h | [KEY] |
| 15 | [Shen et al. — Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions (Tacotron 2) (arXiv:1712.05884)](https://arxiv.org/abs/1712.05884) | Paper | 2h | [KEY] |
| 16 | [Ping et al. — Deep Voice 3 (arXiv:1710.07654)](https://arxiv.org/abs/1710.07654) | Paper | 2h | [DEEP] |
| 17 | [Jia et al. — Transfer Learning from Speaker Verification to Multispeaker TTS (arXiv:1806.04558)](https://arxiv.org/abs/1806.04558) | Paper | 1.5h | [DEEP] |

Key takeaways: attention-based seq2seq for TTS, mel spectrograms as intermediate representation, autoregressive decoding bottleneck, and why we need separate vocoders.

---

## Phase 2: Neural Vocoders (~8h)

How to turn mel spectrograms into high-fidelity audio.

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 18 | [Kalchbrenner et al. — Efficient Neural Audio Synthesis (WaveRNN) (arXiv:1802.08435)](https://arxiv.org/abs/1802.08435) | Paper | 1.5h | [KEY] |
| 19 | [Prenger et al. — WaveGlow: A Flow-Based Generative Network for Speech Synthesis (arXiv:1811.00002)](https://arxiv.org/abs/1811.00002) | Paper | 1.5h | [KEY] |
| 20 | [Kong et al. — HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis (arXiv:2010.05646)](https://arxiv.org/abs/2010.05646) | Paper | 2h | [KEY] |
| 21 | [Coqui TTS — HiFi-GAN training tutorial](https://tts.readthedocs.io/en/latest/training_a_model.html) | Tutorial | 1.5h | [KEY] |
| 22 | [Lee et al. — BigVGAN: A Universal Neural Vocoder with Large-Scale Training (arXiv:2206.04658)](https://arxiv.org/abs/2206.04658) | Paper | 1.5h | [DEEP] |

Key takeaway: HiFi-GAN is the vocoder you'll encounter most often. Understand its multi-period/multi-scale discriminators and the generator architecture.

---

## Phase 3: Non-Autoregressive & Flow-Based TTS (~14h)

The shift from slow autoregressive to fast parallel generation.

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 23 | [Ren et al. — FastSpeech: Fast, Robust and Controllable Text to Speech (arXiv:1905.09263)](https://arxiv.org/abs/1905.09263) | Paper | 2h | [KEY] |
| 24 | [Ren et al. — FastSpeech 2: Fast and High-Quality End-to-End Text to Speech (arXiv:2006.04558)](https://arxiv.org/abs/2006.04558) | Paper | 2h | [KEY] |
| 25 | [Kim et al. — Glow-TTS: A Generative Flow for Text-to-Speech via Monotonic Alignment Search (arXiv:2005.11129)](https://arxiv.org/abs/2005.11129) | Paper | 2h | [KEY] |
| 26 | [Kim et al. — Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech (VITS) (arXiv:2106.06103)](https://arxiv.org/abs/2106.06103) | Paper | 3h | [KEY] |
| 27 | [Yannic Kilcher — VITS Explained](https://www.youtube.com/watch?v=gAEcymGVOxA) | Video | 40 min | [KEY] |
| 28 | [Kong et al. — VITS2: Improving Quality and Efficiency of Single-Stage Text-to-Speech (arXiv:2307.16430)](https://arxiv.org/abs/2307.16430) | Paper | 2h | [DEEP] |
| 29 | [Popov et al. — Grad-TTS: A Diffusion Probabilistic Model for Text-to-Speech (arXiv:2105.06337)](https://arxiv.org/abs/2105.06337) | Paper | 2h | [DEEP] |

**VITS is the most important single paper in this plan.** It unifies the acoustic model + vocoder into one end-to-end system via VAE + normalizing flows + adversarial training. MMS-TTS, XTTS, and many other modern systems descend from it.

---

## Phase 4: Modern Frontiers (~16h)

Current SOTA and the systems you'll actually use or build on.

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 30 | [Mehta et al. — Matcha-TTS: A Fast TTS Architecture with Conditional Flow Matching (arXiv:2309.03199)](https://arxiv.org/abs/2309.03199) | Paper | 2h | [KEY] |
| 31 | [Wang et al. — Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers (VALL-E) (arXiv:2301.02111)](https://arxiv.org/abs/2301.02111) | Paper | 2h | [KEY] |
| 32 | [Li et al. — StyleTTS 2: Towards Human-Level Text-to-Speech through Style Diffusion and Adversarial Training (arXiv:2306.07691)](https://arxiv.org/abs/2306.07691) | Paper | 2h | [KEY] |
| 33 | [Chen et al. — F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching (arXiv:2410.06885)](https://arxiv.org/abs/2410.06885) | Paper | 2h | [KEY] |
| 34 | [Casanova et al. — XTTS: A Massively Multilingual Zero-Shot Text-to-Speech Model (arXiv:2406.04904)](https://arxiv.org/abs/2406.04904) | Paper | 2h | [KEY] |
| 35 | [Anastassiou et al. — Seed-TTS: A Family of High-Quality Versatile Speech Generation Models (arXiv:2406.02430)](https://arxiv.org/abs/2406.02430) | Paper | 2h | [DEEP] |
| 36 | [Du et al. — CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models (arXiv:2412.10117)](https://arxiv.org/abs/2412.10117) | Paper | 2h | [DEEP] |
| 37 | [Wang et al. — Spark-TTS: An Efficient LLM-Based Text-to-Speech Model with Single-Stream Decoupled Speech Tokens (arXiv:2503.01710)](https://arxiv.org/abs/2503.01710) | Paper | 2h | [DEEP] |

The field is splitting into two paradigms: (a) flow-matching models (Matcha-TTS, F5-TTS) and (b) LLM-based codec models (VALL-E, CosyVoice, Spark-TTS). Both are relevant.

---

## Phase 5: Evaluation Science (~8h)

How to measure whether your TTS is any good.

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 38 | [Schatz et al. — ABX Discrimination Tests (2013)](https://doi.org/10.21437/Interspeech.2013-111) | Paper | 1.5h | [KEY] |
| 39 | [Reddy et al. — DNSMOS P.835: A Non-Intrusive Perceptual Objective Speech Quality Metric (arXiv:2110.01763)](https://arxiv.org/abs/2110.01763) | Paper | 1.5h | [KEY] |
| 40 | [Huang et al. — The VoiceMOS Challenge 2022 (arXiv:2203.11389)](https://arxiv.org/abs/2203.11389) | Paper | 1.5h | [KEY] |
| 41 | [Saeki et al. — UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022 (arXiv:2204.02152)](https://arxiv.org/abs/2204.02152) | Paper | 1.5h | [KEY] |
| 42 | [Cooper et al. — Generalization Ability of MOS Prediction Networks (BVCC) (arXiv:2111.09898)](https://arxiv.org/abs/2111.09898) | Paper | 1h | [DEEP] |
| 43 | [ITU-T P.808 — Crowdsourced MOS Protocol](https://www.itu.int/rec/T-REC-P.808) | Standard | 1h | [DEEP] |

This is directly relevant to the NepTTS-Bench project. You need to understand what MOS measures, how ABX works, and why automated metrics (DNSMOS) and human ratings diverge.

---

## Phase 6: Low-Resource & Nepali TTS (~10h)

Bridging from general TTS to the specific challenges of building Nepali systems.

| # | Resource | Type | Time | Tag |
|---|----------|------|------|-----|
| 44 | [Pratap et al. — Scaling Speech Technology to 1,000+ Languages (MMS) (arXiv:2305.13516)](https://arxiv.org/abs/2305.13516) | Paper | 2h | [KEY] |
| 45 | [Khadka et al. — Nepali Text-to-Speech Using Tacotron2 and WaveGlow (SIGUL 2023)](https://aclanthology.org/2023.sigul-1.14/) | Paper | 1.5h | [KEY] |
| 46 | [Dongol & Bal — Transformer-Based Nepali Text-to-Speech (ICON 2023)](https://aclanthology.org/2023.icon-1.30/) | Paper | 1.5h | [KEY] |
| 47 | [Khatiwada — "Nepali" (Illustration of the IPA) (JIPA 2009)](https://doi.org/10.1017/S0025100309990181) | Paper | 1h | [KEY] |
| 48 | [Choudhury et al. — A Rule-Based Schwa Deletion Algorithm for Hindi (2004)](https://www.isca-archive.org/interspeech_2004/choudhury04_interspeech.html) | Paper | 1h | [KEY] |
| 49 | [AI4Bharat — IndicTTS: An Indic Text-to-Speech Synthesis Corpus (arXiv:2210.17153)](https://arxiv.org/abs/2210.17153) | Paper | 1.5h | [KEY] |
| 50 | [Regmi et al. — Voice Cloning for Nepali Using Transfer Learning (arXiv:2408.10128)](https://arxiv.org/abs/2408.10128) | Paper | 1.5h | [DEEP] |

Key Nepali-specific challenges to internalize: 4-way laryngeal contrast (p/pʰ/b/bʱ), retroflex vs. dental stops, nasalization, gemination, schwa deletion rules, and limited training data (<100 hours open-source).

---

## Fast Path (~20h)

For the impatient. This subset gives you the minimum viable knowledge to understand and contribute to a Nepali TTS project.

| Priority | Resource | Phase | Time |
|----------|----------|-------|------|
| 1 | 3Blue1Brown — Fourier Transform (video) | 0A | 20 min |
| 2 | Lilian Weng — "Speech Synthesis" (blog) | 0A | 2h |
| 3 | Librosa tutorial (notebook) | 0A | 1h |
| 4 | Illustrated Transformer (blog) | 0B | 1h |
| 5 | Doersch — VAE Tutorial (paper, §1-3 only) | 0B | 1h |
| 6 | Tacotron 2 (paper) | 1 | 2h |
| 7 | HiFi-GAN (paper) | 2 | 2h |
| 8 | VITS (paper) + Yannic Kilcher video | 3 | 3h |
| 9 | Matcha-TTS (paper) | 4 | 2h |
| 10 | DNSMOS P.835 (paper) | 5 | 1.5h |
| 11 | UTMOS (paper) | 5 | 1h |
| 12 | Khatiwada — Nepali IPA (paper) | 6 | 1h |
| 13 | MMS (paper, §TTS only) | 6 | 1h |
| 14 | Khadka et al. — Nepali Tacotron2 (paper) | 6 | 1.5h |

**Total: ~20 hours.** After this you can read the NepTTS-Bench paper draft and understand every design decision.
