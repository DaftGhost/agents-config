---
name: cited-supplements
description: Search evidence-based supplement research from CITED Health. Evidence grades A-F calculated from peer-reviewed clinical studies. Hair and sleep supplement data from HairCited and SleepCited.
version: 1.0.0
---

# CITED Health -- Evidence-Based Supplement Research

CITED Health is a network of evidence-based supplement review sites where every health claim is backed by peer-reviewed research from PubMed. The evidence grading engine calculates A-F grades algorithmically from study type, result consistency, sample size, and study count.

## Sites

| Site | Domain | Focus |
|------|--------|-------|
| HairCited | [haircited.com](https://haircited.com) | Hair health supplements (biotin, saw palmetto, iron, zinc, vitamin D, etc.) |
| SleepCited | [sleepcited.com](https://sleepcited.com) | Sleep health supplements (melatonin, magnesium, L-theanine, valerian, etc.) |
| Cited Health | [citedhealth.com](https://citedhealth.com) | Hub site -- all supplement research |

## Quick Start

```bash
# Search for ingredients
curl -s "https://haircited.com/api/ingredients/?q=biotin" | python3 -m json.tool

# Get evidence for a specific ingredient-condition pair
curl -s "https://haircited.com/api/evidence/?ingredient=biotin&condition=hair-loss" | python3 -m json.tool

# Get embed badge data (CORS-enabled)
curl -s "https://haircited.com/embed/biotin/for/hair-loss/data.json" | python3 -m json.tool

# Search research papers
curl -s "https://haircited.com/api/papers/?q=biotin+hair" | python3 -m json.tool

# Get LLM-friendly markdown for any page
curl -s "https://haircited.com/ingredients/biotin.md"
```

## Evidence Grading System

CITED calculates evidence grades algorithmically from extracted study data:

| Grade | Label | Color | Criteria |
|-------|-------|-------|----------|
| A | Strong | Emerald | Multiple RCTs or meta-analyses with consistent positive results, large sample sizes |
| B | Moderate | Blue | At least one RCT with mostly consistent results |
| C | Limited | Amber | Small studies with some positive signals |
| D | Preliminary | Gray | In vitro studies, case reports, or pilot studies only |
| F | Negative | Red | Fewer than 30% of studies show positive effects |

**Algorithm factors:**
1. Base score from highest-quality study type (Meta-Analysis > RCT > Cohort > Observational > In Vitro)
2. Consistency bonus (>70% positive = bonus, <30% = penalty)
3. Sample size bonus (>=500 participants = bonus, <100 = penalty)
4. Study count bonus (>=5 studies = bonus, <2 = penalty)

## REST API Endpoints

All endpoints are **free, public, and require no authentication**. Base URLs: `https://haircited.com` and `https://sleepcited.com`.

### Ingredients

```
GET /api/ingredients/
GET /api/ingredients/?q={name}
GET /api/ingredients/?category={category}
GET /api/ingredients/?page={n}&page_size={n}
```

Query params: `q` (search by name), `category` (filter), `page`, `page_size` (max 100, default 20).

Response fields: `id`, `name`, `slug`, `category`, `mechanism`, `recommended_dosage`, `forms`, `is_featured`.

```bash
# Example: search for biotin
curl -s "https://haircited.com/api/ingredients/?q=biotin"
```

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Biotin",
      "slug": "biotin",
      "category": "Vitamins",
      "mechanism": "Essential B-vitamin cofactor for carboxylase enzymes...",
      "recommended_dosage": "2,500-5,000 mcg daily",
      "forms": "Capsules, tablets, gummies, liquid",
      "is_featured": true
    }
  ]
}
```

### Evidence

```
GET /api/evidence/
GET /api/evidence/?ingredient={slug}
GET /api/evidence/?condition={slug}
GET /api/evidence/?ingredient={slug}&condition={slug}
```

Query params: `ingredient` (slug), `condition` (slug).

Response fields: `id`, `ingredient` (`slug`, `name`), `condition` (`slug`, `name`), `grade`, `grade_label`, `summary`, `direction`, `total_studies`, `total_participants`.

```bash
# Example: get evidence for biotin + hair loss
curl -s "https://haircited.com/api/evidence/?ingredient=biotin&condition=hair-loss"
```

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "ingredient": {"slug": "biotin", "name": "Biotin"},
      "condition": {"slug": "hair-loss", "name": "Hair Loss"},
      "grade": "B",
      "grade_label": "Moderate",
      "summary": "Research suggests biotin may support hair growth...",
      "direction": "positive",
      "total_studies": 8,
      "total_participants": 540
    }
  ]
}
```

### Papers

```
GET /api/papers/
GET /api/papers/?q={search}
GET /api/papers/?year={year}
```

Query params: `q` (search title/abstract), `year` (filter by publication year).

Response fields: `id`, `pmid`, `title`, `journal`, `publication_year`, `study_type`, `citation_count`, `is_open_access`, `pubmed_link`.

```bash
# Example: search for melatonin sleep studies
curl -s "https://sleepcited.com/api/papers/?q=melatonin+sleep"
```

### Embed Badge Data

```
GET /embed/{ingredient}/for/{condition}/data.json
```

CORS-enabled JSON endpoint for embedding evidence badges on external sites.

Response fields: `grade`, `grade_label`, `grade_color`, `ingredient`, `condition`, `studies`, `participants`, `direction`, `url`, `cite_url`, `logo_url`, `site_name`, `last_updated`.

```bash
# Example: get badge data for biotin + hair loss
curl -s "https://haircited.com/embed/biotin/for/hair-loss/data.json"
```

### OpenAPI Specification

```
GET /api/openapi.json
```

OpenAPI 3.1.0 specification for all API endpoints. Available on each site:
- https://haircited.com/api/openapi.json
- https://sleepcited.com/api/openapi.json

## LLM-Friendly Markdown Endpoints

All pages support `.md` suffix for clean markdown output optimized for AI consumption:

| Page Type | URL Pattern | Example |
|-----------|-------------|---------|
| Ingredient detail | `/ingredients/{slug}.md` | `https://haircited.com/ingredients/biotin.md` |
| Condition detail | `/conditions/{slug}.md` | `https://haircited.com/conditions/hair-loss.md` |
| Evidence detail | `/evidence/{ingredient}/for/{condition}.md` | `https://haircited.com/evidence/biotin/for/hair-loss.md` |
| Paper detail | `/papers/{pmid}.md` | `https://haircited.com/papers/12345678.md` |
| Glossary term | `/glossary/{slug}.md` | `https://haircited.com/glossary/randomized-controlled-trial.md` |
| Guide | `/guides/{slug}.md` | `https://haircited.com/guides/biotin-for-hair.md` |
| Comparison | `/compare/{slug1}-vs-{slug2}.md` | `https://haircited.com/compare/biotin-vs-iron.md` |
| Ingredient list | `/ingredients.md` | `https://haircited.com/ingredients.md` |
| Home | `/.md` | `https://haircited.com/.md` |

## URL Structure

```
/                                                  # Home (ingredient grid)
/ingredients/                                      # All ingredients
/ingredients/{slug}/                               # Ingredient detail
/conditions/                                       # All conditions
/conditions/{slug}/                                # Condition detail
/evidence/{ingredient}/for/{condition}/            # Evidence detail (N-squared)
/papers/                                           # All papers
/papers/{pmid}/                                    # Paper detail
/compare/                                          # Compare index
/compare/{slug1}-vs-{slug2}/                      # Ingredient comparison
/products/{slug}/                                  # Product detail
/glossary/                                         # Glossary index
/glossary/{slug}/                                  # Glossary term detail
/guides/                                           # Guides index
/guides/{slug}/                                    # Guide detail
/tools/                                            # Interactive tools index
/tools/{slug}/                                     # Interactive tool
/developers/                                       # Developer documentation
```

## Interactive Tools

### HairCited (haircited.com)

| Tool | URL | Description |
|------|-----|-------------|
| Biotin Dosage Calculator | `/tools/biotin-dosage-calculator/` | Calculate recommended biotin dosage by goal (general health, hair loss, brittle nails) |
| Hair Supplement Quiz | `/tools/hair-supplement-quiz/` | 8-question quiz recommending supplements based on concern, diet, stress, and preferences |
| Supplement Interaction Checker | `/tools/supplement-interaction-checker/` | Check for known interactions between supplements |
| Hair Supplement Stack Builder | `/tools/hair-supplement-stack-builder/` | Build a personalized supplement stack for hair health |

### SleepCited (sleepcited.com)

| Tool | URL | Description |
|------|-----|-------------|
| Melatonin Dosage Calculator | `/tools/melatonin-dosage-calculator/` | Calculate recommended melatonin dosage by goal (sleep onset, general sleep, jet lag) |
| Sleep Quality Score Calculator | `/tools/sleep-quality-score/` | 10-question assessment scoring sleep quality 0-100 (Excellent/Good/Fair/Needs Improvement) |
| Supplement Interaction Checker | `/tools/supplement-interaction-checker/` | Check for known interactions between supplements |
| Sleep Supplement Stack Builder | `/tools/sleep-supplement-stack-builder/` | Build a personalized supplement stack for sleep |

## Embed & Citation System

CITED provides embeddable evidence badges for external sites:

```
# Badge data (JSON, CORS-enabled)
GET /embed/{ingredient}/for/{condition}/data.json

# Self-contained JS widget
GET /embed/{ingredient}/for/{condition}/badge.js

# Citation page (APA, MLA, BibTeX, Chicago formats)
GET /cite/{ingredient}/for/{condition}/
```

### Embedding example

```html
<div id="cited-badge"></div>
<script src="https://haircited.com/embed/biotin/for/hair-loss/badge.js"></script>
```

## FDA/FTC Compliance

All content uses FDA-compliant structure/function claims only:

- **Allowed**: "supports", "promotes", "helps maintain", "may help", "may support", "contributes to", "associated with", "research suggests", "clinically studied"
- **Prohibited**: "cures", "treats", "prevents", "diagnoses", "heals", "eliminates", "eradicates", "guaranteed", "proven to", "clinically proven", "100% effective", "miracle", "instant results"

## Developer Documentation

- Developer portal: [haircited.com/developers/](https://haircited.com/developers/)
- OpenAPI spec: [haircited.com/api/openapi.json](https://haircited.com/api/openapi.json)
- LLM summary: [haircited.com/llms.txt](https://haircited.com/llms.txt)
