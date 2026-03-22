"""
Pure analysis helpers for the EDA Streamlit app (unit-testable, no Streamlit).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def memory_usage_mb(df: pd.DataFrame) -> float:
    return float(df.memory_usage(deep=True).sum() / (1024**2))


def dtypes_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = df.dtypes.value_counts().reset_index()
    out.columns = ["Type", "Count"]
    return out


def strong_correlations(
    corr_matrix: pd.DataFrame, threshold: float = 0.5
) -> pd.DataFrame:
    """Upper-triangle pairs with |r| > threshold; NaN correlations skipped."""
    pairs = []
    cols = list(corr_matrix.columns)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            if pd.isna(val):
                continue
            if abs(float(val)) > threshold:
                pairs.append(
                    {
                        "Feature 1": cols[i],
                        "Feature 2": cols[j],
                        "Correlation": float(val),
                    }
                )
    if not pairs:
        return pd.DataFrame(columns=["Feature 1", "Feature 2", "Correlation"])
    out = pd.DataFrame(pairs)
    return out.reindex(out["Correlation"].abs().sort_values(ascending=False).index)


def missing_summary(df: pd.DataFrame) -> tuple[int, float]:
    """Total missing cells and percentage of all cells (0 if empty)."""
    missing = int(df.isnull().sum().sum())
    total_cells = df.shape[0] * df.shape[1]
    if total_cells == 0:
        return missing, 0.0
    return missing, (missing / total_cells) * 100.0


def high_cardinality_columns(
    df: pd.DataFrame, categorical_cols: list[str], min_unique: int = 50
) -> list[str]:
    return [c for c in categorical_cols if df[c].nunique(dropna=True) > min_unique]


def numeric_skew_insights(
    df: pd.DataFrame,
    numeric_cols: list[str],
    max_cols: int = 3,
    skew_threshold: float = 1.0,
) -> list[str]:
    insights: list[str] = []
    for col in numeric_cols[:max_cols]:
        s = df[col].dropna()
        if len(s) < 3:
            continue
        skewness = float(s.skew())
        if abs(skewness) > skew_threshold:
            direction = "right" if skewness > 0 else "left"
            insights.append(
                f"📈 Feature '{col}' is highly skewed to the {direction} "
                f"(skewness: {skewness:.2f})"
            )
    return insights


def build_insights(
    df: pd.DataFrame,
    cardinality_threshold: int = 50,
    skew_max_cols: int = 3,
) -> list[str]:
    """Generate human-readable insight strings (emoji prefixes preserved for UI)."""
    insights: list[str] = []
    missing_count, missing_pct = missing_summary(df)
    if missing_pct > 0:
        insights.append(
            f"⚠️ Dataset has {missing_count} missing values "
            f"({missing_pct:.2f}% of total data)"
        )

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    insights.append(
        f"📊 Dataset contains {len(numeric_cols)} numeric and "
        f"{len(categorical_cols)} categorical features"
    )

    high_card = high_cardinality_columns(
        df, categorical_cols, min_unique=cardinality_threshold
    )
    if high_card:
        insights.append(f"🔍 Features with high cardinality: {', '.join(high_card)}")

    insights.extend(
        numeric_skew_insights(df, numeric_cols, max_cols=skew_max_cols)
    )
    return insights


def pdf_numeric_summary_lines(df: pd.DataFrame, max_cols: int = 3) -> list[str]:
    """Text lines for PDF: mean/std for first N numeric columns."""
    lines: list[str] = []
    for col in df.select_dtypes(include=[np.number]).columns[:max_cols]:
        s = df[col].dropna()
        if len(s) == 0:
            lines.append(f"{col}: no numeric values")
            continue
        lines.append(f"{col}: Mean={s.mean():.2f}, Std={s.std():.2f}")
    return lines
