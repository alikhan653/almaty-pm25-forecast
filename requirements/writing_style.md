# Academic Writing Style Guide

## Core principle

Write for a technically literate reader who is NOT familiar with this specific
project. Every section must be self-contained enough to be understood without
reading earlier sections (use forward/backward references to connect them).

---

## Tone and register

- Formal academic English throughout.
- **No contractions**: "do not" not "don't", "it is" not "it's".
- **No colloquialisms**: avoid "a lot of", "get", "show up", "deal with".
- **No first person singular**: use "the present study", "this work", "we" (if
  co-authored) or passive voice.
  - ✅ "The model was trained on..."
  - ✅ "This study proposes..."
  - ❌ "I trained the model on..."
- **Precise language**: say exactly what you mean.
  - ❌ "performance" → ✅ "RMSE" or "forecast accuracy"
  - ❌ "the results are good" → ✅ "XGBoost achieves RMSE = 23.4 μg/m³"
- **Active voice preferred** for method descriptions (passive acceptable for
  results): "The pipeline fetches hourly measurements..." rather than "Hourly
  measurements are fetched by the pipeline..."

---

## Paragraph structure

Every paragraph follows this pattern:
1. **Topic sentence** — states the single claim the paragraph supports.
2. **Evidence / development** — data, citations, or reasoning that supports it.
3. **Transition** — links to the next paragraph or chapter.

One paragraph = one idea. If you have two ideas, split into two paragraphs.
Maximum paragraph length: ~150 words.

---

## Numbers and units

- Spell out numbers one through nine; use numerals for 10 and above.
  Exception: always use numerals with units: "3 hours", "6 μg/m³".
- Unit symbols: μg/m³ (not ug/m3), km, m, h (not hr), %.
- Decimal separator: period (.) not comma.
- Thousands separator: comma for English: 13,488 rows.
- Percentages: "22.2%" with no space before the symbol.
- Ranges: "6–24 h" with an en-dash (–), not a hyphen (-).
- Approximate values: "approximately 30–60 seconds" or "~30 s".

---

## Tables and figures — caption writing

Table caption (above): concise, describes what the table shows and the context.
> ✅ "Table 3.1. Model comparison on the held-out test set (2,311 hours, winter 2025–26)."
> ❌ "Table 3.1. Results."

Figure caption (below): must be self-contained — reader must understand the
figure WITHOUT reading the body text.
> ✅ "Figure 3.2. Monthly mean PM2.5 (μg/m³) across all active sensors, 2024–2026. Error bars show ±1 standard deviation. The grey band marks the WHO 24-hour guideline (25 μg/m³)."
> ❌ "Figure 3.2. Monthly PM2.5."

---

## Citing results

Always pair a number with its context:
- ✅ "XGBoost achieves RMSE = 23.44 μg/m³ at the 6-hour horizon, a 22% improvement over the persistence baseline."
- ❌ "XGBoost performs better."

When comparing models, always state the baseline being compared against.

---

## Literature review writing

- Organise by theme or methodology, NOT by chronological list of papers.
- For each cited work, state: what they did, what dataset/context, what result,
  and crucially — what gap they leave that motivates the present work.
- Do not plagiarise abstracts. Paraphrase and synthesise.
- Minimum 30 references total; at least 15 in the literature review chapter.

---

## Avoiding AI-detectable patterns

The following patterns are statistically associated with AI-generated text and
will be flagged by Antiplagiat.ru's AI-detection module. Avoid them:

### Banned openers
- "In recent years..." → start with the specific claim instead
- "It is worth noting that..." → just state the note
- "Importantly, ..." → the content should show it's important
- "Furthermore, ..." (when overused) → use specific transitions: "This result suggests...", "By contrast...", "Building on this..."
- "In conclusion, ..." at section ends → just write the conclusion

### Banned filler phrases
- "plays a crucial role in"
- "has gained significant attention"
- "a wide range of"
- "state-of-the-art"  (use "current best-performing" or cite the specific method)
- "novel approach"  (you decide what's novel — state it, don't label it)
- "leverage" (use "use", "apply", "employ")
- "robust" unless backed by a specific test
- "comprehensive" — too vague

### Punctuation
- **Em-dash (—) is banned.** Replace every em-dash with a regular hyphen (-) or
  rewrite the sentence with a comma or parentheses.
  - ❌ "The model — trained on 578 k observations — achieves RMSE = 23.4."
  - ✅ "The model, trained on 578 k observations, achieves RMSE = 23.4."
- En-dash (–) is allowed only in numeric ranges: "6–24 h", "2024–2026".

### Structural anti-patterns
- Avoid bullet-point summaries at the end of every section ("In summary, this
  section has shown that...") — these are characteristic of AI output.
- Avoid perfectly parallel three-item lists everywhere. Vary sentence structure.
- Avoid hedging every claim with "may", "might", "could potentially" — be direct
  where evidence supports it.
- Vary sentence length. AI text tends to have uniform medium-length sentences.
  Mix short punchy sentences with longer analytical ones.

### Humanising techniques
- Include specific numbers and measurements in every paragraph.
- Reference your own code and data decisions: "The 3-sensor minimum threshold
  (line 42 of `pipeline.py`) was chosen after observing..."
- Use field-specific jargon correctly and precisely.
- Acknowledge uncertainty honestly: "The 12-hour horizon result is surprising
  and warrants investigation in future work."
- Quote specific dates, file names, API endpoints, error messages when relevant.

---

## Chapter-specific guidance

### Introduction
- Open with a concrete fact about Almaty's air quality, not a general statement
  about AI or environmental monitoring.
- State the research gap in one sentence.
- List objectives as a numbered list (4–5 items), each starting with an
  infinitive verb: "To develop...", "To evaluate...", "To compare..."

### Literature review (Chapter 1)
- Each subsection should end with a sentence that links back to the Almaty case
  and explains why that body of work is relevant.
- Every claim about existing work must be cited. "Studies have shown" without
  a citation is unacceptable.

### Methodology (Chapter 2)
- Methods must be reproducible: describe parameters, thresholds, and decisions
  precisely enough that another researcher could reimplement the pipeline.
- Justify every non-obvious choice: why median and not mean? why 500 μg/m³ cap?

### Results (Chapter 3)
- Never present a table without discussing it in text.
- Discuss unexpected results honestly — do not suppress them.
- Use precise comparative language: "outperforms by X%", "reduces RMSE by Y μg/m³".

### Discussion (Chapter 4)
- Connect results back to objectives stated in the Introduction.
- Limitations section must be honest about LCS data quality, network coverage
  gaps, and the restricted geography.
  