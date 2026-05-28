"""Tests for scoring logic."""

from main import score_all
from src.utils import load_data


def find_row(rows, company_id, row_id, theme):
    for row in rows:
        if (
            row["company_id"] == company_id
            and row["row_id"] == row_id
            and row["theme"] == theme
        ):
            return row
    return None


def test_company_5_climate_scores_zero():
    data = load_data()
    output = score_all(data)

    row_1 = find_row(output, "5", "r1", "Climate Change")
    row_2 = find_row(output, "5", "r2", "Climate Change")

    assert row_1 is not None
    assert row_2 is not None
    assert row_1["route"] == "Route A"
    assert row_1["score"] == 0
    assert row_1["max_score"] == 4
    assert row_2["score"] == 0
    assert row_2["max_score"] == 4


def test_company_2_water_route_b():
    data = load_data()
    output = score_all(data)

    row = find_row(output, "2", "r3", "Water")

    assert row is not None
    assert row["route"] == "Route B"
    assert row["score"] == 1
    assert row["max_score"] == 2


def test_company_4_climate_uppercase_and_slash_date():
    data = load_data()
    output = score_all(data)

    row = find_row(output, "4", "r1", "Climate Change")

    assert row is not None
    assert row["route"] == "Route A"
    assert row["score"] == 4
    assert row["max_score"] == 4


def test_company_7_climate_missing_date():
    data = load_data()
    output = score_all(data)

    row = find_row(output, "7", "r1", "Climate Change")

    assert row is not None
    assert row["route"] == "Non-disclosure"
    assert row["score"] == 0
    assert row["max_score"] == 0.5


def test_company_9_climate_not_applicable():
    data = load_data()
    output = score_all(data)

    row = find_row(output, "9", "N/A", "Climate Change")

    assert row is not None
    assert row["route"] == "Not applicable"
    assert row["score"] == 0
    assert row["max_score"] == 0
