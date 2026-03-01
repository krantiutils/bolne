# NepTTS-Bench — Full Reference Collection

Comprehensive references gathered for the Interspeech 2026 paper. Organized by category.

---

## 1. Nepali Phonology and Phonetics

### Standard References

- **Khatiwada, Rajesh (2009).** "Nepali." *Journal of the International Phonetic Association*, 39(3), 373-380. [DOI](https://doi.org/10.1017/S0025100309990181)
  - Definitive IPA description. Full consonant/vowel inventories, spectrograms, audio. Part of "Illustrations of the IPA" series. CNRS/Sorbonne-Nouvelle.

- **Bandhu, Chudamani, Ballabh Mani Dahal, Andreas Holzhausen & Austin Hale (1971).** *Nepali Segmental Phonology*. SIL, Tribhuvan University.
  - Foundational work on Nepali phonological system. Establishes six oral vowels; notes weaker evidence for vowel nasalization being phonemically distinctive.

- **Pokharel, Madhav Prasad (1989).** *Experimental Analysis of Nepali Sound System*. Ph.D., University of Pune.
  - Instrumental phonetic study. Recognizes ten diphthongs. Key reference for acoustic analysis.

- **Acharya, Jayaraj (1991).** *A Descriptive Grammar of Nepali and an Analyzed Corpus*. Georgetown University Press.
  - Corpus-based morphology and grammar study.

### Four-Way Aspiration Contrast

- **Schwarz, Martha, Morgan Sonderegger & Heather Goad (2019).** "Realization and representation of Nepali laryngeal contrasts: Voiced aspirates and laryngeal realism." *Journal of Phonetics*, 73, 113-127. [PDF](http://people.linguistics.mcgill.ca/~morgan/schwarzEtAl_JPhon_2019.pdf)
  - Studies 4-way stop contrast in Nepali from Sikkim. Demonstrates VOT and voicing lead co-vary with speech rate. Supports laryngeal realism.

- **Khatiwada, Rajesh (2007).** "Phonetic realization of contrastively aspirated affricates in Nepali." [ResearchGate](https://www.researchgate.net/publication/228495938)
  - 4-way aspiration in affricates specifically.

### Retroflex vs Dental Contrasts

- **Khatiwada, Rajesh (2007).** "Nepalese retroflex stops: A static palatography study of inter- and intra-speaker variability." [ResearchGate](https://www.researchgate.net/publication/221485241)
  - Articulatory study confirming 3-way place contrast (dental, alveolar, retroflex). Documents inter/intra-speaker variability.

- **Hamann, Silke (2003).** *The Phonetics and Phonology of Retroflexes*. LOT Dissertation Series 75, Utrecht. [PDF](https://www.lotpublications.nl/Documents/075_fulltext.pdf)
  - Cross-linguistic study of retroflexion including South Asian languages.

- **Comparative Acoustic-Phonetic Analysis of Retroflex Consonants of Some Indian Languages (2019).** ICA Aachen. [PDF](https://pub.dega-akustik.de/ICA2019/data/articles/000954.pdf)
  - Analyzes retroflex sounds in Hindi, Nepali, Punjabi. 50 native speakers/language. F2, F3, F4 burst transitions are key discriminators.

### Nasalization

- Khatiwada (2009): 11 phonologically distinctive vowels: 6 oral + 5 nasal counterparts.
- **"Acoustic Study of the Nepali Nasal Consonants" (2023).** *Linguistic Society of Nepal Journal*. [PDF](https://www.nepjol.info/index.php/lsnj/article/download/60006/44875)

### Schwa Deletion

- **Choudhury, Monojit, Anupam Basu & Sudeshna Sarkar (2004).** "A Diachronic Approach for Schwa Deletion in Indo-Aryan Languages." *Proc. SIGPHON*, ACL. [PDF](https://aclanthology.org/W04-0103.pdf)
  - Syllable-minimization algorithm for schwa deletion. Examines Bengali, Hindi, Nepali. Standard rule achieves ~89%.

- **"Schwa Deletion in Hindi Language Speech Synthesis" (2019).** *IJEAT*, 8(6S). [PDF](https://www.ijeat.org/wp-content/uploads/papers/v8i6S/F10420886S19.pdf)
  - Directly relevant to TTS: schwa deletion for Devanagari speech synthesis front-ends.

- **Nair & Ananthapadmanabha (2016).** "Schwa Deletion and Syllable Economy in Indo-Aryan Languages." [Academia](https://www.academia.edu/1489537/)
  - Important: Nepali orthography is more phonetic than Hindi re: schwa retention.

- **Tyson, Adi & Arora (2020).** "Supervised Grapheme-to-Phoneme Conversion of Orthographic Schwas in Hindi and Punjabi." arXiv:2004.10353.
  - First statistical schwa deletion classifier relying on orthography alone.

### Prosody

- **"Exploring Intonation Patterns in Nepali Speech: A Phonetic and Linguistic Analysis for Text-to-Speech System" (2025).** [ResearchGate](https://www.researchgate.net/publication/389452140)
  - Nepali: no phonemic stress/lexical tone; syllable-timed rhythm; stress on first syllable; statements=falling, questions=rising.

---

## 2. Nepali TTS Systems

### Neural TTS

- **Khadka et al. (2023).** "Nepali Text-to-Speech Synthesis using Tacotron2 for Melspectrogram Generation." *SIGUL 2023*. [PDF](https://www.isca-archive.org/sigul_2023/khadka23_sigul.pdf)
  - Tacotron2 + HiFi-GAN. MOS 4.03 naturalness, 4.01 accuracy — highest for Nepali TTS.

- **Dongol, Ishan & Bal Krishna Bal (2023).** "Transformer-based Nepali Text-to-Speech." *ICON 2023*, pp. 651-656. [ACL Anthology](https://aclanthology.org/2023.icon-1.64/)
  - FastPitch + HiFi-GAN. MOS 3.70 / 3.40 on two datasets.

- **Regmi et al. (2024).** "Advancing Voice Cloning for Nepali." arXiv:2408.10128. [arXiv](https://arxiv.org/abs/2408.10128)
  - Transfer learning from high-resource languages. 546 speakers, 168 hours. MOS 3.93.

- **"Neural Multi-Speaker Voice Cloning for Nepali in Low-Resource Settings" (2025).** arXiv:2601.18694. [arXiv HTML](https://arxiv.org/html/2601.18694v1)
  - Tacotron2 + speaker embeddings + WaveRNN. First multi-speaker Nepali voice cloning.

### Earlier/Concatenative TTS

- **Shah & Chaudhary (2018).** "Nepali Text to Speech Synthesis System using FreeTTS." *SCITECH Nepal*. [NepJOL](https://www.nepjol.info/index.php/scitech/article/view/23498)
- **Bal & Shrestha (2017).** "Building a Natural Sounding Text-to-Speech System for the Nepali Language." [ResearchGate](https://www.researchgate.net/publication/349855900)
  - Festival + concatenative/unit selection. Kathmandu University ILPRL lab.
- **Chettri & Shah.** "Nepali Text to Speech Synthesis System using ESNOLA Method of Concatenation." [Semantic Scholar](https://www.semanticscholar.org/paper/39482a4a144f8ca58a83921d55d7a8dbf2af5bc6)

### Large-Scale Indic TTS (including Nepali)

- **AI4Bharat (2022).** "Towards Developing State-of-the-Art TTS Synthesisers for 13 Indian Languages." arXiv:2210.17153.
- **AI4Bharat (2024).** "Indic Parler-TTS." [HuggingFace](https://huggingface.co/ai4bharat/indic-parler-tts)
  - 21 languages including Nepali. VITS2 + multilingual ID + BERT. 69 voices.
- **Meta AI (2023).** "MMS: Scaling Speech Technology to 1000+ Languages." arXiv:2305.13516. [arXiv](https://arxiv.org/abs/2305.13516)
  - ASR + TTS for 1,100+ languages. Halves Whisper's WER on FLEURS.

---

## 3. TTS Evaluation Benchmarks

- **Seed-TTS-Eval (2024).** Anastassiou et al. "Seed-TTS: A Family of High-Quality Versatile Speech Generation Models." arXiv:2406.02430. [GitHub](https://github.com/BytedanceSpeech/seed-tts-eval)
  - WavLM-large speaker similarity + ASR-based WER. Zero-shot evaluation.

- **LibriTTS (2019).** Zen et al. "LibriTTS: A Corpus Derived from LibriSpeech for TTS." *Interspeech*. [OpenSLR 60](https://www.openslr.org/60/)
  - 585 hours, 2,456 speakers, 24kHz.

- **LibriTTS-R (2023).** Koizumi et al. "LibriTTS-R: A Restored Multi-Speaker Text-to-Speech Corpus." *Interspeech*. [OpenSLR 141](https://www.openslr.org/141/)
  - Miipher restoration applied. Naturalness on par with ground truth.

- **VoiceMOS Challenge (2022).** Huang et al. [arXiv:2203.11389](https://arxiv.org/abs/2203.11389)
  - Shared task for automatic MOS prediction. 22 teams.

- **MUSHRA (ITU-R BS.1534-3).** [PDF](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1534-3-201510-I!!PDF-E.pdf)
- **webMUSHRA (2018).** Schoeffler et al. [GitHub](https://github.com/audiolabs/webMUSHRA)

---

## 4. Automated TTS Metrics

- **DNSMOS P.835 (2022).** Reddy et al. "DNSMOS P.835: A Non-Intrusive Perceptual Objective Speech Quality Metric." *ICASSP*. [arXiv:2110.01763](https://arxiv.org/abs/2110.01763)
  - SIG, BAK, OVRL scores. PCC 0.94-0.98 with human ratings.

- **UTMOS (2022).** Saeki et al. "UTokyo-SaruLab System for VoiceMOS Challenge 2022." *Interspeech*. [arXiv:2204.02152](https://arxiv.org/abs/2204.02152)
  - VoiceMOS Challenge winner. SSL + contrastive learning.

- **ECAPA-TDNN (2020).** Desplanques et al. "ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification." *Interspeech*, pp. 3830-3834. [arXiv:2005.07143](https://arxiv.org/abs/2005.07143)
  - 192-dim embeddings. State-of-the-art on VoxCeleb.

- **WavLM (2022).** Chen et al. *IEEE JSTSP*, 16, 1505-1518. [arXiv:2110.13900](https://arxiv.org/abs/2110.13900)
  - 94K hours SSL. Used in Seed-TTS-Eval for speaker similarity.

- **PESQ (2001).** Rix et al. *ICASSP*. ITU-T P.862.
- **POLQA (2013).** Beerends et al. *JAES*, 61(6). ITU-T P.863.
- **ViSQOL v3 (2020).** Chinen et al. *QoMEX*. [GitHub](https://github.com/google/visqol)

---

## 5. ABX Discrimination and Phonological Evaluation

- **Schatz et al. (2013).** "Evaluating Speech Features with the Minimal-Pair ABX Task." *Interspeech*. [PDF](https://www.di.ens.fr/~fbach/Schatz_PBJHD_mpABX_1_analysis_of_the_MFC-PLP_pipeline.Interspeech.pdf)
  - Introduces Minimal-Pair ABX. Three stimuli, DTW divergence.

- **Schatz (2016).** "ABX-Discriminability Measures and Applications." Ph.D., UPMC. [HAL](https://hal.science/tel-01407461)
  - Comprehensive formalization. Generalizes beyond speech.

- **ZeroSpeech 2019.** Dunbar et al. "TTS without T." *Interspeech*. [arXiv:1904.11469](https://arxiv.org/abs/1904.11469)
  - ABX as primary metric for unit discovery + synthesis evaluation.

- **ZeroSpeech 2020.** Dunbar et al. *Interspeech*. [HAL](https://hal.science/hal-02962224v1/document)

- **Montreal Forced Aligner (2017).** McAuliffe et al. *Interspeech*. [Docs](https://montreal-forced-aligner.readthedocs.io/)
  - Kaldi-based trainable alignment. Supports any language with pronunciation dictionary.

- **"Evaluating Speech-Phoneme Alignment and Its Impact on Neural TTS" (2023).** *ICASSP*. [AudioLabs](https://www.audiolabs-erlangen.de/resources/NLUI/2023-ICASSP-eval-alignment-tts)
  - Alignment errors <75ms don't decrease synthesis quality.

---

## 6. ASR / Whisper

- **Radford et al. (2023).** "Robust Speech Recognition via Large-Scale Weak Supervision." *ICML*. [arXiv:2212.04356](https://arxiv.org/abs/2212.04356)
  - 680K hours multilingual. Supports 99 languages including Nepali.

- **Rai et al. (2024).** "Whisper Finetuning on Nepali Language." arXiv:2411.12587. [IEEE Xplore](https://ieeexplore.ieee.org/document/11277459)
  - 36% WER reduction on small, 24% on medium. Uses FLEURS + Common Voice + OpenSLR + custom data.

- **XLS-R (2022).** Babu et al. "Self-supervised Cross-lingual Speech Representation Learning at Scale." *Interspeech*. [arXiv:2111.09296](https://arxiv.org/abs/2111.09296)
  - wav2vec 2.0, 2B params, 500K hours, 128 languages.

---

## 7. TTS Architectures

- **VITS (2021).** Kim et al. *ICML*. [arXiv:2106.06103](https://arxiv.org/abs/2106.06103)
- **FastSpeech 2 (2021).** Ren et al. *ICLR*. [arXiv:2006.04558](https://arxiv.org/abs/2006.04558)
- **CosyVoice (2024).** Du et al. arXiv:2407.05407. [GitHub](https://github.com/FunAudioLLM/CosyVoice)
- **CosyVoice 2 (2024).** Du et al. arXiv:2412.10117. Streaming, 150ms latency.
- **Spark-TTS (2025).** Wang et al. arXiv:2503.01710. [GitHub](https://github.com/SparkAudio/Spark-TTS). Qwen2.5 backbone, BiCodec, UTMOS 4.35.
- **YourTTS (2022).** Casanova et al. *ICML*. First multilingual zero-shot TTS.
- **XTTS (2024).** Casanova et al. *Interspeech*. 16 languages zero-shot.
- **MeloTTS (2023).** MyShell.ai. [GitHub](https://github.com/myshell-ai/MeloTTS). Real-time CPU inference.

---

## 8. TTS Knowledge Distillation

- **Nix-TTS (2022).** Chevi & Prasojo. *IEEE SLT*. [arXiv:2203.15643](https://arxiv.org/abs/2203.15643)
  - Module-wise distillation. 5.23M params (89% reduction), 3x CPU speedup.

- **LightSpeech (2021).** Luo et al. *ICASSP*. [arXiv:2102.04040](https://arxiv.org/abs/2102.04040)
  - NAS-based. 15x compression, 6.5x CPU speedup, on-par quality.

- **Spotify TTS KD (2025).** Henriksson et al. *SSW 2025*. [PDF](https://www.isca-archive.org/ssw_2025/henriksson25_ssw.pdf)
  - CFG-enhanced teacher → student. 50% size reduction, 2x speedup.

---

## 9. Text Normalization

- **Sproat & Jaitly (2016).** "RNN Approaches to Text Normalization: A Challenge." arXiv:1611.00068.
- **Zhang et al. (2019).** "Neural Models of Text Normalization for Speech Applications." *Computational Linguistics*, 45(2).
- **Ebden & Sproat (2014).** "The Kestrel TTS Text Normalization System." Google. WFST-based.
- **Bali et al. (2007).** "Text Processing for TTS in Indian Languages." *SSW6*. 96.6% Hindi, 93.4% Tamil.
- **"Hindi Text Normalization" (2006).** [ResearchGate](https://www.researchgate.net/publication/228596823)

---

## 10. Code-Switching

- **Sitaram & Black (2016).** "Speech Synthesis of Code-Mixed Text." *LREC*. [ACL Anthology](https://aclanthology.org/L16-1546/)
  - Hindi-English code-mixed TTS. Independent bilingual datasets work well.

- **Gurung, Dinesh (2019).** "Nepali-English code-switching in the conversations of Nepalese people." Ph.D., University of Roehampton.
  - English nouns dominate lexical switching. Education/location influence mixing.

- **"Code-Mixed Text to Speech Synthesis under Low-Resource Constraints" (2023).** arXiv:2312.01103.
- **Diwan et al. (2021).** "Multilingual and Code-switching ASR Challenges for Low Resource Indian Languages." arXiv:2104.00235.

---

## 11. Speech Quality Standards

- **EBU R 128 (2020).** Loudness normalisation. Target -23 LUFS. [PDF](https://tech.ebu.ch/docs/r/r128.pdf)
- **ITU-T P.808 (2018/2020).** Crowdsourced MOS. Naderi & Cutler. [GitHub](https://github.com/microsoft/P.808)
- **ITU-T P.835 (2003).** Speech quality in noise: SIG, BAK, OVRL (1-5 scale).

---

## 12. Nepali NLP Surveys and Language Models

- **Shahi & Sitaula (2021).** "Natural language processing for Nepali text: a review." *AI Review*, Springer.
- **NepBERTa (2022).** Timilsina et al. *AACL short papers*. BERT on 0.8B Nepali words.
- **"A Breadth-First Catalog..." (2025).** arXiv:2501.00029. Survey of South Asian speech/text processing.

---

## 13. Nepali Speech Datasets

| Dataset | Size | Use | Link |
|---------|------|-----|------|
| OpenSLR-54 (Google) | 165 hrs, 527 speakers | ASR | [openslr.org/54](https://www.openslr.org/54/) |
| OpenSLR-43 | Single speaker, HQ | TTS | [openslr.org/43](https://www.openslr.org/43/) |
| OpenSLR-143 | Male + Female | TTS | [openslr.org/143](http://openslr.org/143/) |
| Mozilla Common Voice | Community-contributed | ASR | [HuggingFace](https://huggingface.co/datasets/mozilla-foundation/common_voice_10_0) |
| FLEURS (Google) | ~12 hrs | Multilingual benchmark | [HuggingFace](https://huggingface.co/datasets/google/fleurs) |
| IndicVoices | 7,348 hrs, 22 langs | ASR | [arXiv:2403.01926](https://arxiv.org/abs/2403.01926) |
| IndicVoices-R | 1,704 hrs, 22 langs | TTS | [NeurIPS 2024](https://openreview.net/forum?id=3qH8q02x0n) |
