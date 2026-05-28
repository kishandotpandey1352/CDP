"""DSSA Technical Assessment.

uv run python ./main.py
"""

from datetime import date, datetime
import json

from src.utils import load_data, save_output


STATEMENT_1 = "Lorem ipsum dolor sit amet"
STATEMENT_2 = "consectetur adipiscing elit"
STATEMENT_3 = "sed do eiusmod tempor"

CUTOFF_DATE = date(2023, 1, 1)

OUTPUT_FIELDS = [
    "company_id",
    "row_id",
    "theme",
    "route",
    "score",
    "max_score",
    "c2",
    "c1",
    "c3",
    "statement_1_present",
    "statement_2_present",
    "statement_3_present",
    "c3_count",
    "c3_has_even",
    "notes",
]


def normalize_text(value):
    if not isinstance(value, str):
        return ""
    return " ".join(value.lower().split())


def statement_present(answer, statement):
    normalized_answer = normalize_text(answer)
    if not normalized_answer:
        return False
    return normalize_text(statement) in normalized_answer


def parse_date(value):
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        pass
    try:
        return datetime.strptime(value, "%Y/%m/%d").date()
    except ValueError:
        return None


def normalize_c3(value):
    if not isinstance(value, list):
        return []
    numbers = []
    for item in value:
        if isinstance(item, bool):
            continue
        if isinstance(item, (int, float)):
            numbers.append(item)
    return numbers


def format_c3(value):
    if value is None:
        return ""
    try:
        return json.dumps(value, ensure_ascii=True)
    except TypeError:
        return ""


def analyze_row(row):
    c1 = row.get("c1") if "c1" in row else None
    c2_raw = row.get("c2") if "c2" in row else None
    c3_raw = row.get("c3") if "c3" in row else None
    parsed_date = parse_date(c2_raw)
    c3_numbers = normalize_c3(c3_raw)
    return {
        "c1": c1 if isinstance(c1, str) else None,
        "c2_raw": c2_raw,
        "c3_raw": c3_raw,
        "parsed_date": parsed_date,
        "statement_1_present": statement_present(c1, STATEMENT_1),
        "statement_2_present": statement_present(c1, STATEMENT_2),
        "statement_3_present": statement_present(c1, STATEMENT_3),
        "c3_count": len(c3_numbers),
        "c3_has_even": any(number % 2 == 0 for number in c3_numbers),
    }


def date_note(c2_raw, parsed_date):
    if c2_raw is None:
        return "Date missing."
    if parsed_date is None:
        return "Date not parseable; treated as missing."
    if parsed_date <= CUTOFF_DATE:
        return "Date on/before 2023-01-01."
    return ""


def build_output_row(
    company_id,
    row_id,
    theme,
    analysis,
    route,
    score,
    max_score,
    notes,
):
    return {
        "company_id": company_id,
        "row_id": row_id,
        "theme": theme,
        "route": route,
        "score": score,
        "max_score": max_score,
        "c2": "" if analysis.get("c2_raw") is None else str(analysis.get("c2_raw")),
        "c1": analysis.get("c1") or "",
        "c3": format_c3(analysis.get("c3_raw")),
        "statement_1_present": analysis.get("statement_1_present", False),
        "statement_2_present": analysis.get("statement_2_present", False),
        "statement_3_present": analysis.get("statement_3_present", False),
        "c3_count": analysis.get("c3_count", 0),
        "c3_has_even": analysis.get("c3_has_even", False),
        "notes": notes,
    }


def score_climate_row(company_id, row_id, analysis):
    parsed_date = analysis["parsed_date"]
    if parsed_date is None or parsed_date <= CUTOFF_DATE:
        return build_output_row(
            company_id,
            row_id,
            "Climate Change",
            analysis,
            "Non-disclosure",
            0,
            0.5,
            date_note(analysis.get("c2_raw"), parsed_date),
        )

    score = 0
    if analysis["statement_2_present"] and analysis["c3_count"] > 3:
        score += 3
    if analysis["statement_3_present"] and analysis["c3_has_even"]:
        score += 1

    return build_output_row(
        company_id,
        row_id,
        "Climate Change",
        analysis,
        "Route A",
        score,
        4,
        "",
    )


def score_water_row(company_id, row_id, analysis):
    parsed_date = analysis["parsed_date"]
    if parsed_date is None:
        return build_output_row(
            company_id,
            row_id,
            "Water",
            analysis,
            "Non-disclosure",
            0,
            0.5,
            date_note(analysis.get("c2_raw"), parsed_date),
        )

    if parsed_date <= CUTOFF_DATE:
        return build_output_row(
            company_id,
            row_id,
            "Water",
            analysis,
            "Route B",
            1,
            2,
            date_note(analysis.get("c2_raw"), parsed_date),
        )

    score = 0
    if analysis["statement_1_present"] and analysis["c3_has_even"]:
        score += 1
    if analysis["statement_3_present"] and analysis["c3_count"] > 3:
        score += 1

    return build_output_row(
        company_id,
        row_id,
        "Water",
        analysis,
        "Route A",
        score,
        2,
        "",
    )


def score_all(data):
    """Compute per-row scores for every company under both themes."""
    output = []
    companies = data.get("companies", {})
    for company_id, company_data in companies.items():
        rows = company_data.get("q_1_1", {})
        company_themes: set[str] = set()
        for row in rows.values():
            themes = row.get("c4") if isinstance(row.get("c4"), list) else []
            for theme in themes:
                company_themes.add(theme)

        for row_id, row in rows.items():
            themes = row.get("c4") if isinstance(row.get("c4"), list) else []
            analysis = analyze_row(row)
            if "Climate Change" in themes:
                output.append(score_climate_row(company_id, row_id, analysis))
            if "Water" in themes:
                output.append(score_water_row(company_id, row_id, analysis))

        for theme in ("Climate Change", "Water"):
            if theme not in company_themes:
                output.append(
                    {
                        "company_id": company_id,
                        "row_id": "N/A",
                        "theme": theme,
                        "route": "Not applicable",
                        "score": 0,
                        "max_score": 0,
                        "c2": "",
                        "c1": "",
                        "c3": "",
                        "statement_1_present": False,
                        "statement_2_present": False,
                        "statement_3_present": False,
                        "c3_count": 0,
                        "c3_has_even": False,
                        "notes": "Theme not selected in any row for this company.",
                    }
                )

    return output


if __name__ == "__main__":
    data = load_data()
    scores = score_all(data)
    save_output(scores, OUTPUT_FIELDS)

    
