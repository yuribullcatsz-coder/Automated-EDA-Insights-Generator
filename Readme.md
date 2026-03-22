# Automated EDA & Insights Generator

Educational Streamlit app for a data science course: upload a CSV, explore the dataset with summaries and charts, inspect correlations, read auto-generated insights, and download a short PDF report.

**Repository:** [github.com/yuribullcatsz-coder/Automated-EDA-Insights-Generator](https://github.com/yuribullcatsz-coder/Automated-EDA-Insights-Generator)

---

## Features

| Area | What you get |
|------|----------------|
| **Upload** | CSV file picker; empty files are rejected with a clear message |
| **Overview** | Row/column counts, missing values, memory estimate, dtypes table, preview, `describe()` summary |
| **Visualizations** | Histograms for numeric columns (up to 6); bar charts for categorical / `category` columns (top 10 levels, up to 6 columns) |
| **Correlations** | Interactive heatmap for numeric columns; table of pairs with \|r\| > 0.5 (NaN pairs ignored) |
| **Insights** | Missing-data share, numeric vs categorical counts, high-cardinality categoricals, skew notes for the first few numeric columns |
| **Report** | One-click PDF (overview + numeric means/std for up to three columns); download works with current `fpdf2` (PDF bytes normalized for Streamlit) |

---

## Requirements

- **Python** 3.10 or newer (3.9 may work; the project is tested on current 3.x releases)
- **pip** (or another installer that understands `requirements.txt`)

Dependencies are listed in [`requirements.txt`](requirements.txt). The app uses **Streamlit**, **pandas**, **NumPy**, **Plotly**, and **fpdf2**. Unit tests use **pytest**.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yuribullcatsz-coder/Automated-EDA-Insights-Generator.git
cd Automated-EDA-Insights-Generator
```

### 2. Create a virtual environment (recommended)

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

---

## Run the application

From the project root (the folder that contains `eda_app.py` and `eda_analysis.py`):

```bash
streamlit run eda_app.py
```

If `streamlit` is not on your `PATH`, use:

```bash
py -m streamlit run eda_app.py
```

The app opens in your browser (default URL: [http://localhost:8501](http://localhost:8501)).

---

## How to use the app

1. **Upload a CSV** using "Browse files". The file is read in memory; nothing is stored on disk by the app.
2. **Overview** — Check shape, missing values, dtypes, first rows, and descriptive statistics.
3. **Visualizations** — Scroll distributions for numeric and categorical columns. Columns with no plottable values show a short caption instead of an empty chart.
4. **Correlations** — Requires at least two numeric columns with data. Strong correlations use a threshold of **0.5** on the absolute value of Pearson correlation in `eda_app.py` (backed by `strong_correlations()` in `eda_analysis.py`).
5. **Insights** — Bullet-style cards summarizing data quality and simple distributional hints.
6. **Report** — Click **Generate Report**, then **Download PDF Report**. If the download fails, ensure you are on a recent version of Streamlit and fpdf2; the app converts PDF output to `bytes` for compatibility.

---

## Project layout

| File / folder | Role |
|---------------|------|
| `eda_app.py` | Streamlit UI, Plotly figures, PDF layout class, wiring to analysis helpers |
| `eda_analysis.py` | Pure Python helpers (metrics, correlations table, insights text, PDF numeric lines) — easy to unit test |
| `requirements.txt` | Pinned minimum versions for runtime and tests |
| `tests/` | Pytest suite for `eda_analysis.py` |
| `.gitignore` | Ignores caches, virtual envs, bytecode |

---

## Running unit tests

From the project root, with the same environment where you installed `requirements.txt`:

```bash
pytest tests -v
```

Or:

```bash
py -m pytest tests -v
```

All tests target **`eda_analysis`** only (no Streamlit runtime required).

---

## Customization

| Goal | Where to look |
|------|----------------|
| Strong correlation threshold (default 0.5) | `show_correlations()` in `eda_app.py`, or `strong_correlations()` in `eda_analysis.py` |
| Insight rules (missing %, cardinality, skew) | `build_insights()`, `numeric_skew_insights()`, `high_cardinality_columns()` in `eda_analysis.py` |
| New chart types or tabs | `eda_app.py` (`show_visualizations`, etc.) |
| PDF sections and wording | `PDFReport` and `generate_report()` in `eda_app.py`; numeric lines from `pdf_numeric_summary_lines()` in `eda_analysis.py` |

---

## Limitations

- Large files (for example **> 100 MB**) or very wide tables can feel slow; everything runs **in memory**.
- For responsiveness, datasets of **under ~100,000 rows** are a practical target on a typical laptop.
- The PDF is a **short** summary, not a full audit of every column.

---

## Screenshots

<p align="center">
  <img width="800" alt="Overview sample" src="https://github.com/user-attachments/assets/53d45d22-7b90-47ae-ab45-e9e7a0dd8df2" />
</p>

<p align="center">
  <img width="800" alt="Visualizations sample" src="https://github.com/user-attachments/assets/271f5515-80cb-4b29-af30-d386bf8d9abe" />
</p>

<p align="center">
  <img width="800" alt="Correlations sample" src="https://github.com/user-attachments/assets/90d4d502-8953-4b47-9106-078c7758de6a" />
</p>

<p align="center">
  <img width="800" alt="Insights sample" src="https://github.com/user-attachments/assets/64787789-005d-4aa1-839f-efd0993ae4e7" />
</p>

<p align="center">
  <img width="800" alt="Report sample" src="https://github.com/user-attachments/assets/0e71412e-5a6e-4393-be2a-cef17a32d370" />
</p>

<p align="center">
  <img width="800" alt="Additional UI" src="https://github.com/user-attachments/assets/77f8e346-e9f0-4cfc-ab50-4111ef54d776" />
</p>

<p align="center">
  <img width="800" alt="Additional UI" src="https://github.com/user-attachments/assets/18e4c62c-5dd0-4e30-93bc-afb4d318f647" />
</p>

<p align="center">
  <img width="800" alt="Additional UI" src="https://github.com/user-attachments/assets/7d840787-7fa8-460b-bb10-cbbd25852f68" />
</p>

---

## License / course use

This project is intended as an **educational** example for a data science course. Adapt and extend it for your own learning or teaching.
