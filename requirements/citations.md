# Citation Requirements — APA 7th Edition

KBTU requires APA 7th edition for all in-text citations and the reference list.
The thesis uses BibTeX (`thesis/references.bib`); BibTeX keys follow the pattern
`authorYYYY_keyword` (e.g., `chen2006_neural`, `openaq_platform`).

---

## In-text citation formats

| Situation | Format | Example |
|---|---|---|
| Parenthetical | (Author, Year) | (Chen et al., 2006) |
| Narrative | Author (Year) | Chen et al. (2006) demonstrated... |
| Two authors | Both names | (Zhang & Li, 2010) |
| Three or more | First author + et al. | (Vaswani et al., 2017) |
| Multiple citations | Semicolon, chronological | (Chen et al., 2006; Zhang et al., 2010) |
| Direct quote | Include page | (Nanda, 2024, p. 3) |
| No author | Short title in italics | (*OpenAQ Platform*, 2024) |

---

## Reference list format

### Journal article
```
Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Volume*(Issue), page–page. https://doi.org/xxxxx
```

### Conference paper
```
Author, A. A. (Year). Title of paper. In *Proceedings of the Conference Name* (pp. page–page). Publisher.
```

### Online dataset / platform
```
Organisation. (Year). *Name of dataset/platform* [Dataset]. URL
```

### Book
```
Author, A. A. (Year). *Title of book* (Edition if not first). Publisher.
```

### Report / technical document
```
Author, A. A. (Year). *Title of report* (Report No. if available). Organisation. URL
```

---

## Required citations for this thesis

The following sources are already documented in `plan.md` and **must** appear
in `thesis/references.bib` with verified BibTeX entries:

| Key (suggested) | Source |
|---|---|
| `openaq_platform` | OpenAQ (2024). OpenAQ Platform. https://openaq.org |
| `zippenfenig2023_openmeteo` | Zippenfenig, P. (2023). Open-Meteo.com Weather API. Zenodo. https://doi.org/10.5281/ZENODO.7970649 |
| `iqair2024_world` | IQAir (2024). World Air Quality Report. IQAir. |
| `snyder2013_lcs` | Snyder et al. (2013). The changing paradigm of air pollution monitoring. *ES&T*, 47(20), 11369–11377. |
| `morawska2018_lcs` | Morawska et al. (2018). Applications of low-cost sensing technologies for air quality monitoring. *Environment International*, 116, 286–299. |

---

## Rules for citation integrity (CRITICAL)

1. **Never cite a paper you have not read.** At minimum, read the abstract and
   verify the claim you are citing appears in the paper.
2. **Never generate BibTeX from memory.** Always verify via Semantic Scholar,
   CrossRef, or the publisher DOI page.
3. If a citation cannot be verified, write `[CITATION NEEDED: description]` as
   a placeholder and flag it for manual verification.
4. Self-citation is allowed but must be genuine publications — do not inflate.
5. Avoid citing only Wikipedia, news articles, or non-peer-reviewed sources.
   Wikipedia may appear in footnotes for general context only.
6. All URLs must have an access date if the resource is not archived:
   "Retrieved May 10, 2026, from https://..."

---

## BibTeX conventions for this project

```bibtex
@article{authorYYYY_keyword,
  author    = {Last, First and Last2, First2},
  title     = {Full title of the paper},
  journal   = {Journal Name},
  year      = {2024},
  volume    = {47},
  number    = {20},
  pages     = {11369--11377},
  doi       = {10.xxxx/xxxxx},
}

@misc{openaq_platform,
  author       = {{OpenAQ}},
  title        = {{OpenAQ} Platform},
  year         = {2024},
  url          = {https://openaq.org},
  note         = {Retrieved May 10, 2026},
}
```

Key rules:
- Use `--` for page ranges in BibTeX, not `-`.
- Wrap proper nouns in `{{}}` to prevent lowercasing: `{PM2.5}`, `{Almaty}`.
- Double-brace organisation names: `{{OpenAQ}}`, `{{Open-Meteo}}`.
- Always include DOI when available; URL as fallback.
