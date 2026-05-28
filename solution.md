# Solution overview

## Goal
Implement per-row scoring for Climate Change and Water themes from raw `data.json`, handle data quality issues, output reviewer-friendly CSV, and document QA reasoning.

## Key data realities and handling choices
- Missing fields are ambiguous: if a key is absent, the question was not applicable; if present with `null`, the respondent saw it but left it blank.
- Text and dates are messy: casing differences, extra whitespace, and mixed date formats appear in the data.
- Numeric lists may include `null` entries.

To make scoring stable and reviewable, the solution does the following:
- Normalizes text by lowercasing and collapsing whitespace before matching the required lorem statements.
- Parses dates in ISO (`YYYY-MM-DD`) and slash (`YYYY/MM/DD`) formats; non-parseable or missing dates are treated as missing.
- Filters `c3` values to numeric entries only, ignoring `null` and non-numeric items.

## Scoring approaches

### 1. Per-row scoring
Each row is scored independently for each theme present in `c4`. If a row has both themes, it produces two output rows (one per theme).

### 2. Route selection
The route used for scoring is determined by theme and date rules:

**Climate Change**
- Route A: `c2` is after 2023-01-01
- Non-disclosure: `c2` is on/before 2023-01-01 or missing

**Water**
- Route A: `c2` is after 2023-01-01
- Route B: `c2` is on/before 2023-01-01
- Non-disclosure: `c2` is missing

### 3. Statement and list conditions
After route selection, statement matching and list checks determine points:

**Climate Change Route A**
- +3 points if statement 2 is present and `c3` has more than 3 numeric values
- +1 point if statement 3 is present and `c3` has at least one even value

**Water Route A**
- +1 point if statement 1 is present and `c3` has at least one even value
- +1 point if statement 3 is present and `c3` has more than 3 numeric values

**Water Route B**
- Always 1/2 point when date is on/before 2023-01-01

Non-disclosure routes always score 0 and use a smaller max score, per the criteria.

### 4. Not applicable handling
If a company never selects a theme in any row, a single row is emitted with:
- `row_id = N/A`
- route = "Not applicable"
- score and max score = 0

This makes the CSV complete across both themes for all companies.

## Output format
The output is a CSV saved to `local/output.csv` with fields intended for non-technical QA review, including:
- company and row identifiers
- theme and route
- score and max score
- raw `c1`, `c2`, and `c3` values
- derived flags (statement matches, count of numeric values, even-number presence)
- notes field that explains date-based routing

## How to run
1. Install dependencies with `uv sync` or `pip install -e .`.
2. Run the scoring script with `uv run python ./main.py` or `python ./main.py`.
3. Open the generated `local/output.csv` to review the per-row scores.
4. Run tests with `uv run pytest -v` or `pytest -v`.

## Testing approach
Tests focus on representative edge cases from the dataset:
- Uppercase lorem text and slash date formats
- Missing dates leading to non-disclosure routes
- Route B behavior for Water
- Not applicable theme output
- Company 5 climate rows scoring zero as per criteria

## QA response approach
The QA response explains Company 5’s zero scores in plain language by tying back to the two Route A conditions, and flags potential brittleness in the methodology (exact phrase matching and list-length dependency).

## Summary of decisions
- Normalize and parse inputs to reduce scoring noise from formatting issues.
- Keep route logic explicit to match the specification closely.
- Emit additional diagnostic fields to improve auditability for non-technical reviewers.
- Add not-applicable rows so every company has both themes represented.
