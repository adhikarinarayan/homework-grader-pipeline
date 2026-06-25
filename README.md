# LLM Homework Grading 

Pipeline for automated grading of handwritten/scanned STEM homework using LLMs. Developed for the report: *Automated Grading of Handwritten STEM Homework: A Five-Stage Pipeline for Nuclear Engineering*

The pipeline has four sequential stages, each in its own module:

```
QP PDF ──► QP_Rubric ──► parser ──► jsonifier ──► grader ──► Grades/
```

---

## Setup

### Requirements

```bash
pip install google-generativeai mistralai pandas
```

### API Keys

The pipeline uses two LLMs:

| Stage | Model | Provider |
|-------|-------|----------|
| QP_Rubric, parser | Gemini 2.0 Flash | Google AI |
| jsonifier, grader | Mistral Large | Mistral AI |

Set your keys as environment variables before running any stage:

```bash
export GEMINI_API_KEY="your_key_here"
export MISTRAL_API_KEY="your_key_here"
```

Replace the hardcoded key strings in each `models.py` / `main.py` with:

```python
import os
API_KEY = os.environ["GEMINI_API_KEY"]
mistral_api = os.environ["MISTRAL_API_KEY"]
```

### Directory Layout

Each homework folder must follow this structure before running the pipeline:

```
<course>_<HW>/
├── Ungraded_Cleaned/   ← scanned student PDFs (one per student)
└── QP_Rubric/
    └── QP.pdf          ← question paper PDF
```

Set the target homework in `config.yaml`:

```yaml
main_path: "'3_HW1'"
```

---

## Stages

### 1. `QP_Rubric/` — Question Paper Processing

Converts the question paper PDF into structured JSON and generates a grading rubric.

**Run:**
```bash
python QP_Rubric/main.py
```

**Outputs** (written to `<main_path>/QP_Rubric/`):

| File | Description |
|------|-------------|
| `QP.txt` | Plain text transcription of the question paper |
| `QP_schema.json` | Question paper in structured JSON |
| `QP_schema_answer.txt` | Empty answer template (used by jsonifier) |
| `rubric.json` | LLM-generated rubric for grading |

---

### 2. `parser/` — PDF to Text

Uploads each student PDF to Gemini and transcribes the handwritten/typed content into plain text.

**Run:**
```bash
python parser/main.py
```

**Input:** `<main_path>/Ungraded_Cleaned/*.pdf`  
**Output:** `<main_path>/Parsed/*.txt` — one text file per submission

---

### 3. `jsonifier/` — Text to Structured JSON

Takes the parsed text and maps each answer to the correct question using a two-step LLM call:
1. **Segregation** — splits the text by question number guided by the question paper
2. **Schema filling** — maps answers into the standard JSON schema

**Run:**
```bash
python jsonifier/main.py
```

**Input:** `<main_path>/Parsed/*.txt`  
**Outputs:**

| Folder | Description |
|--------|-------------|
| `JSON/` | Structured answer JSON (used by grader) |
| `JSON_Seg/` | Intermediate segregated text |
| `JSON_Text/` | Raw LLM output before JSON parsing |

---

### 4. `grader/` — Automated Grading

Grades each question-answer pair against the rubric using a Mistral LLM acting as a TA persona ("QRee").

**Run:**
```bash
python grader/json_grader.py
```

**Input:** `<main_path>/JSON/*.json` + `QP_Rubric/QP_schema.json` + `QP_Rubric/rubric.json`  
**Outputs:**

| File | Description |
|------|-------------|
| `Grades/<submission_id>.csv` | Per-question marks and LLM reasoning |
| `Grades/total_marks.csv` | Total marks per submission |

---

## Module Reference

### `jsonifier/prompts.py`
Prompt templates for the segregation and schema-filling steps. Edit here to tune extraction behavior.

### `grader/utils.py`
- `extract_qa_pairs()` — aligns question paper, student answer, and rubric into a flat list of rows
- `persona_qree()` — TA persona injected into the grading prompt
- `grading_instructions_ocr()` — grading rubric with OCR-aware leniency instructions
- `extract_marks_and_reasoning()` — parses LLM JSON output into marks and reasoning columns

### `QP_Rubric/utils.py`
- `output_to_json()` — extracts a JSON object from raw LLM text
- `modify_key_and_clear_value()` — converts the QP schema into an empty answer template

---

## Notes

- The grader retries automatically if the LLM returns malformed JSON (up to 4 attempts).
- The parser uploads PDFs to the Gemini Files API and deletes them from cache after use via `remove_gemini_cache()`.

