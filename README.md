# CSVInsight

> Drop a CSV — get an instant statistical summary, correlation heatmap, and anomaly flags

## What it does
Point it at any CSV file and CSVInsight auto-generates: column type detection, descriptive statistics, null/duplicate analysis, correlation matrix, distribution plots, and anomaly detection (outliers via IQR and Z-score). Outputs a self-contained HTML report you can share with anyone.

## Quick Start
```bash
git clone https://github.com/MrHassan2027/CSVInsight
cd CSVInsight
pip install -e .

csvinsight sales_data.csv                   # generate HTML report
csvinsight sales_data.csv --open            # generate + open in browser
csvinsight sales_data.csv -o report.html    # custom output path
```

## Features
- **Column profiling**: type, nulls %, unique count, top values
- **Descriptive stats**: mean, median, std, min/max, percentiles
- **Correlation heatmap**: Pearson / Spearman for numeric columns
- **Distribution plots**: histogram per numeric column
- **Anomaly detection**: IQR + Z-score outlier flags per column
- **Duplicate detection**: exact + near-duplicate rows
- Self-contained HTML report (no internet needed to view)
- Supports CSV, TSV, Excel `.xlsx`

## Tech Stack
| Tool | Why |
|------|-----|
| Python 3.11+ | Orchestration |
| `pandas` | Data loading + stats |
| `scipy` | Z-score, correlation |
| `plotly` | Interactive charts in HTML |
| `jinja2` | HTML report templating |
| `openpyxl` | Excel file support |

## Example Report Sections
```
1. Overview        — rows, columns, memory usage
2. Column Details  — per-column stats + value distribution
3. Correlations    — heatmap of numeric columns
4. Anomalies       — rows flagged as outliers
5. Duplicates      — exact duplicate rows
```
