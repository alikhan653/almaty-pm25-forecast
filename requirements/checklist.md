# Thesis Quality Checklist

Use this checklist at the end of each chapter draft and again before final submission.

---

## Per-chapter checklist (run after each chapter)

### Content
- [ ] Every claim is backed by a citation or by our own experimental results
- [ ] No placeholder `[CITATION NEEDED]` blocks remain unresolved
- [ ] All tables are discussed in text; no orphan tables
- [ ] All figures are discussed in text; no orphan figures
- [ ] Scientific novelty angle is visible — every section connects to why this
      work is new for Almaty / Central Asia
- [ ] No results discussed before they are presented (no forward spoilers)

### Language
- [ ] No first-person singular ("I")
- [ ] No contractions
- [ ] No banned filler phrases (see `writing_style.md`)
- [ ] Numbers follow formatting rules (units, decimal separator, ranges)
- [ ] All abbreviations defined at first use

### Anti-plagiarism / Anti-AI
- [ ] No paragraph starts with "In recent years", "It is worth noting", or
      "Furthermore" as an opener
- [ ] No three-item bullet-point summaries at section ends
- [ ] Sentence lengths vary (mix short and long)
- [ ] Every result paragraph contains at least one specific number
- [ ] Text does not read as a generic survey — Almaty-specific context is present

### Formatting (GOST 7.32)
- [ ] Table captions ABOVE tables, figure captions BELOW figures
- [ ] Tables and figures numbered per-chapter (3.1, 3.2 ...)
- [ ] All headings follow level convention (not more than 3 levels)
- [ ] Code listings ≤ 20 lines in body; longer code in appendices
- [ ] All equations numbered at right margin

---

## Pre-submission final checklist

### References
- [ ] Minimum **25** references in `thesis/references.bib` (KBTU official minimum)
- [ ] Majority of references from last **5 years** (2021–2026) — recommended
- [ ] All BibTeX entries verified (no hallucinated citations)
- [ ] All DOIs tested and working
- [ ] APA 7th edition format used consistently

### Structure
- [ ] All 4 body chapters complete (no "TODO" sections)
- [ ] Introduction contains: relevance, problem statement, aim, objectives (4–5),
      scientific novelty (≥ 2 points), practical significance, structure overview
- [ ] Conclusion covers all objectives stated in Introduction
- [ ] Abstract: 250–300 words, states aim/methods/results/conclusions
- [ ] List of abbreviations present (≥ 5 abbreviations used)
- [ ] Appendices labelled A, B, C...

### Technical results
- [ ] Model comparison table present (all 4 models × 3 horizons × 4 metrics)
- [ ] Test set evaluation on held-out data only (no training-set metrics reported
      as final results)
- [ ] Application deployment URL included (or noted as pending)
- [ ] All figures are high-resolution (≥ 300 DPI or vector)

### Repository
- [ ] `README.md` contains reproduction instructions
- [ ] No API keys in committed files
- [ ] `data/` folder excluded via `.gitignore`
- [ ] All Python dependencies locked in `pyproject.toml` / `uv.lock`

### Anti-plagiarism
- [ ] Run through Antiplagiat.ru — originality ≥ 70%
- [ ] AI similarity score checked and within acceptable range
- [ ] All quoted text (if any) in quotation marks with page citation
- [ ] All paraphrased text cited with (Author, Year)
