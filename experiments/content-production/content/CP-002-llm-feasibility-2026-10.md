# CP-002 / Казахоязычная LLM — юридическая и экономическая оценка

Date 2026-10-13. Status RESEARCH, not implementation. MPE decision: EXPERIMENT; cost gate 0 KZT for research and benchmark design. No paid compute, no training, no new repo, no deploy.

## Conclusion
Three distinct projects: (1) zero-cost evaluation of open models with scientific, colloquial and literary Kazakh registers; (2) adaptation of licensed 3–8B open-weight model with rights-cleared data and LoRA/SFT; (3) foundation-model training from scratch. Do not equate Kazakh-first product with from-scratch weights. No evidence existing KLC was used in KazLLM.

## Source facts
- 2013 KLC paper confirms >135 million words, genres literary/publicistic/official/scientific/informal, separately annotated text and speech subcorpora. https://aclanthology.org/D13-1104.pdf
- Partial public KLC news: 14,939,567 alphabetic tokens, 55,352 documents. Rights need review, inspect LICENSE.txt; do not infer commercial ML rights from public repository. https://github.com/makazhan/kazcorpus-news
- ISSAI KazLLM 8B/70B: Llama-derived and CC BY-NC 4.0 + upstream Llama terms, commercial rights are NOT automatically granted. https://issai.nu.edu.kz/kazllm/ ; https://huggingface.co/issai/LLama-3.1-KazLLM-1.0-70B
- KazCulture cultural adaptation work reports Qwen3-32B cultural benchmark 39.51% to 64.54% after adaptation, not general fluency proof. https://issai.nu.edu.kz/2026/03/19/introducing-cultural-knowledge-in-language-models-kazculture-dataset-for-kazakh-culture/ ; https://huggingface.co/datasets/issai/KazCulture
- Kazakh small language model study includes public text and preference datasets. https://doi.org/10.3390/bdcc9050137 ; https://huggingface.co/datasets/farabi-lab/raw-text-for-clm-v1
- Instruction-tuning on Kazakhstan governance data (10,600 samples). https://huggingface.co/papers/2502.13647 ; https://huggingface.co/datasets/nurkhan5l/kazakh-ift
- Kazakhstan AI law No 230-VIII, 17 Nov 2025, amended 2026, arts 10/21/23. Specific machine-readable opt-out, rights and contracts require counsel. https://old.adilet.zan.kz/rus/docs/Z2500000230 ; implementation rules https://old.adilet.zan.kz/rus/docs/V2600038444
- Runpod published GPU pricing as of 8 Oct 2026 (vary per model/configuration): https://www.runpod.io/pricing

## Planning estimates (USD, not vendor quotations)
| Path | Estimate | Includes / excludes |
|---|---:|---|
| Research and prompt-only benchmarks | $0 to $1k | excluding unpaid labor |
| Pilot fine-tune with licensed data | $3.5k to $5k | small team, low-cost experiments |
| More robust 3–8B adapted MVP | $5k to $30k | cleaning, experts, multiple runs, legal |
| Foundation model from scratch | $0.5m to $5m+ | team, many runs, compute, lawful corpus |

Illustrative robust MVP line items: GPUs $2k; corpus cleanup $4k; linguists $7k; ML engineering+evaluation $6k; counsel $3k; testing/contingency $3k = $25k. This is a hypothesis, not binding quote.
GPU illustrative hourly price: A100 80GB $1.59; H100 PCIe $2.89; H100 SXM $3.49. A100 100 GPU hours = $159 compute-only. Model architecture, steps, batch, tokens, hardware dictate actual run time.

## Rights checklist
1. Verify each corpus license, creator/annotation rights, source newspaper/book licenses; dataset accessibility != ML permission.
2. Analyze AI Law 2025 arts 21/23, 2026 machine-readable restrictions, copyright and cross-border applicability with counsel.
3. Privacy: consent and removal of personal data in conversational texts. Avoid scraped private messages.
4. Base model weights and redistribution: Meta Llama, Qwen, other licenses differ; KazLLM CC BY-NC.
5. Contracts: data provenance, rights to fine-tuned weights/adapters, derivative datasets, redistribution and commercial service.
6. Independent copyright check before training on modern writers; prefer public domain with verified rights or explicit permission.
7. Document any AI-generated text/synthetic media labeling obligations for eventual user-facing service.

## Research-gated technical design
- Characterize KLC stylistic genres and sizes per genre, licenses and normalization quality.
- Build 30-60 original prompts per register: scientific, colloquial/slang, literary + switching.
- Human native speaker blind assessment on morphology, idiomaticity, dialect fidelity, lexical richness, factual citations, code switching, safety, output length, diversity.
- Compare prompt-only and retrieval against LoRA on a legally cleared small corpus only if first benchmarks show a meaningful gap.
- Evaluate tokenizer inefficiency and cost per 1k tokens, inference requirements, offline feasibility; track version, dataset hashes, training provenance.
- No training or purchase until separately approved. Research output not an authorization to build a model.

## Open questions for KLC and KazLLM authors
- Which sections of 135m-word KLC are still available? Exact rights for commercial model training?
- Genre labels? annotation coverage and metadata? source-level provenance?
- Was KLC or KazNLP material actually used for ISSAI KazLLM?
- Are clean, consented informal Kazakh and licensed literary texts available for three-register adaptation?
- Can commercial KazLLM licensing be negotiated, or use different permissive base?
- How do dialect variation and literary language experts judge generated output?
