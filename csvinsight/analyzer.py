from __future__ import annotations
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ColumnProfile:
    name: str
    dtype: str
    null_count: int
    null_pct: float
    unique_count: int
    top_values: list[tuple]
    mean: float | None = None
    std: float | None = None
    min: float | None = None
    max: float | None = None
    p25: float | None = None
    p50: float | None = None
    p75: float | None = None
    outlier_count: int = 0


@dataclass
class InsightReport:
    path: str
    rows: int
    columns: int
    duplicate_rows: int
    memory_mb: float
    profiles: list[ColumnProfile] = field(default_factory=list)
    correlations: dict = field(default_factory=dict)


def load_dataframe(path: str) -> pd.DataFrame:
    p = Path(path)
    if p.suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    sep = "\t" if p.suffix == ".tsv" else ","
    return pd.read_csv(path, sep=sep)


def profile_column(series: pd.Series) -> ColumnProfile:
    null_count = int(series.isna().sum())
    null_pct = round(null_count / len(series) * 100, 2) if len(series) else 0
    unique_count = int(series.nunique())
    top_values = series.value_counts().head(5).items()

    profile = ColumnProfile(
        name=series.name,
        dtype=str(series.dtype),
        null_count=null_count,
        null_pct=null_pct,
        unique_count=unique_count,
        top_values=[(str(k), int(v)) for k, v in top_values],
    )

    if pd.api.types.is_numeric_dtype(series):
        clean = series.dropna()
        q1, q3 = clean.quantile(0.25), clean.quantile(0.75)
        iqr = q3 - q1
        outliers = ((clean < q1 - 1.5 * iqr) | (clean > q3 + 1.5 * iqr)).sum()
        profile.mean = round(float(clean.mean()), 4)
        profile.std  = round(float(clean.std()), 4)
        profile.min  = round(float(clean.min()), 4)
        profile.max  = round(float(clean.max()), 4)
        profile.p25  = round(float(q1), 4)
        profile.p50  = round(float(clean.median()), 4)
        profile.p75  = round(float(q3), 4)
        profile.outlier_count = int(outliers)

    return profile


def analyze(path: str) -> InsightReport:
    df = load_dataframe(path)
    report = InsightReport(
        path=path,
        rows=len(df),
        columns=len(df.columns),
        duplicate_rows=int(df.duplicated().sum()),
        memory_mb=round(df.memory_usage(deep=True).sum() / 1e6, 3),
    )

    for col in df.columns:
        report.profiles.append(profile_column(df[col]))

    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().round(3)
        report.correlations = corr.to_dict()

    return report
