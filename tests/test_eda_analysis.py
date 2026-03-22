import numpy as np
import pandas as pd
import pytest

from eda_analysis import (
    build_insights,
    dtypes_summary,
    high_cardinality_columns,
    memory_usage_mb,
    missing_summary,
    numeric_skew_insights,
    pdf_numeric_summary_lines,
    strong_correlations,
)


def test_memory_usage_mb_positive():
    df = pd.DataFrame({"a": [1, 2, 3]})
    assert memory_usage_mb(df) > 0


def test_dtypes_summary_columns():
    df = pd.DataFrame({"x": [1], "y": ["a"]})
    out = dtypes_summary(df)
    assert list(out.columns) == ["Type", "Count"]
    assert out["Count"].sum() == 2


def test_strong_correlations_filters_and_sorts():
    corr = pd.DataFrame(
        [[1.0, 0.2, 0.9], [0.2, 1.0, -0.6], [0.9, -0.6, 1.0]],
        columns=list("abc"),
        index=list("abc"),
    )
    out = strong_correlations(corr, threshold=0.5)
    assert len(out) == 2
    assert out.iloc[0]["Feature 1"] == "a" and out.iloc[0]["Feature 2"] == "c"
    assert abs(out.iloc[0]["Correlation"] - 0.9) < 1e-9


def test_strong_correlations_skips_nan():
    corr = pd.DataFrame(
        [[1.0, np.nan], [np.nan, 1.0]],
        columns=["u", "v"],
        index=["u", "v"],
    )
    out = strong_correlations(corr, threshold=0.5)
    assert out.empty


def test_missing_summary_empty_frame():
    df = pd.DataFrame()
    m, pct = missing_summary(df)
    assert m == 0
    assert pct == 0.0


def test_missing_summary_percent():
    df = pd.DataFrame({"a": [1.0, np.nan], "b": [np.nan, 2.0]})
    m, pct = missing_summary(df)
    assert m == 2
    assert abs(pct - 50.0) < 1e-6


def test_high_cardinality_columns():
    n = 60
    df = pd.DataFrame(
        {
            "lo": ["a", "b"] * (n // 2),
            "hi": [f"id_{i}" for i in range(n)],
        }
    )
    cat = ["lo", "hi"]
    hi = high_cardinality_columns(df, cat, min_unique=50)
    assert hi == ["hi"]


def test_numeric_skew_insights_skips_short_series():
    df = pd.DataFrame({"a": [1.0, 2.0]})
    assert numeric_skew_insights(df, ["a"], max_cols=1) == []


def test_pdf_numeric_summary_lines_all_nan():
    df = pd.DataFrame({"a": [np.nan, np.nan]})
    lines = pdf_numeric_summary_lines(df, max_cols=3)
    assert lines == ["a: no numeric values"]


def test_build_insights_includes_missing_and_features():
    df = pd.DataFrame({"n": [1.0, np.nan], "c": ["x", "y"]})
    lines = build_insights(df)
    assert any("missing values" in s for s in lines)
    assert any("numeric" in s and "categorical" in s for s in lines)


@pytest.mark.parametrize(
    "threshold,expected_count",
    [(0.99, 0), (0.5, 1)],
)
def test_strong_correlations_threshold(threshold, expected_count):
    corr = pd.DataFrame([[1.0, 0.7], [0.7, 1.0]], columns=["p", "q"], index=["p", "q"])
    out = strong_correlations(corr, threshold=threshold)
    assert len(out) == expected_count
