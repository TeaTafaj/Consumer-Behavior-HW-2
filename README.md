
[![CI](https://github.com/TeaTafaj/Consumer-Behavior-HW-2/actions/workflows/ci.yml/badge.svg)](https://github.com/TeaTafaj/Consumer-Behavior-HW-2/actions/workflows/ci.yml)

# Consumer Behavior – Ads Engagement Analysis

Identifying whether **smartphone users** engage more with ads than users on other devices.

Tea Tafaj  
Data Engineering Systems (IDS 706) — Duke University  
Date: _September 30th 2025_

---

## Table of Contents
- Research Summary
  - Research Question
  - Key Findings (Snapshot)
  - Implications for Marketers
- Project Setup
  - File Structure
  - Tech Stack & Tools
  - Dependencies
  - Quick Start
  - CI/CD Pipeline
  - Code Refactoring
- Analysis
  - Data Pipeline
  - Analysis Workflow
  - Visualizations
  - How I Reached My Conclusions
- Screenshots
- Troubleshooting
- Data Source
- Author

---

## Research Summary

### Research Question
> **Do smartphone users have higher engagement with ads than users on other devices?**

### Key Findings (Snapshot)
- Engagement labels are standardized to **None / Low / Medium / High** and mapped to **0–3**.
- Average engagement by device is computed and plotted in `ads_by_device.png`.
- A simple logistic regression predicts **High** engagement using device features and reports accuracy/coefficients.

### Implications for Marketers
1. If a device segment shows higher engagement, prioritize **placements, creatives, and bids** there.  
2. Track numeric scores to measure **uplift** after experiments.  
3. Extend features (e.g., region/frequency) to improve predictive power.

---

## Project Setup

### File Structure
```
.
├── Consumer_Behavior.py            # main analysis script (entry point)
├── Ecommerce_Consumer_Behavior_Analysis_Data.csv
├── test_consumer_behavior.py       # unit tests
├── requirements.txt
├── Makefile                        # install, format, lint, test, run, clean
├── Dockerfile                      # containerized runtime
├── images/                         # screenshots for submission
└── .github/workflows/ci.yml        # CI pipeline (flake8, black --check, pytest)
```

### Tech Stack & Tools
**Core:** Python 3.11, pandas, scikit-learn, matplotlib  
**Dev:** pytest, black, flake8, Makefile, GitHub Actions, Docker

### Dependencies
Installed via `requirements.txt` plus dev tools:
```
pandas
scikit-learn
matplotlib
pytest
black
flake8
```

### Quick Start

> **Windows note:** If `make` isn’t available, either install it (GnuWin32.Make) or run the Python commands shown below.

1) **Install**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black flake8 pytest
# or
make install
```

2) **Run the analysis**
```bash
python Consumer_Behavior.py
# or
make run
```

3) **Quality checks**
```bash
# format
python -m black .
# or
make format

# lint
flake8 . --max-line-length=100 --per-file-ignores="test_consumer_behavior.py:F401"
# or
make lint

# tests
pytest -q
# or
make test
```

---

## CI/CD Pipeline
The workflow in `.github/workflows/ci.yml` runs on every push/PR:
1. Set up Python 3.11  
2. Install dependencies  
3. **flake8** (lint, `--max-line-length=100`)  
4. **black --check** (format check)  
5. **pytest** (unit tests)  

The badge at the top links to recent runs.

---

## Code Refactoring
- **Rename:** Standardized `df` → `consumer_data` for clarity.  
![alt text](<Screenshots/before-after 1.PNG>)
![alt text](<Screenshots/before-after 2.PNG>)
![alt text](<Screenshots/before-after 3.PNG>)
- **Extract Method:** Created `summarize_dataframe()` to encapsulate head/info/describe/NA prints.
![alt text](<Screenshots/refractor extract method sc.PNG>)
See commit diffs also in the screenshots folder for before/after.

---

## Analysis

### Data Pipeline
1. **Load** — `load_data(path)` reads the CSV.  
2. **Clean** — `clean_engagement()` trims/title-cases engagement labels and maps them to numeric scores with `ENGAGEMENT_MAP`.  
3. **Slice** — `filter_smartphone_users()` returns only smartphone rows (example transformation).  
4. **Aggregate** — `group_device_ads_mean()` computes mean engagement by device (0=None … 3=High).  
5. **Visualize** — `plot_device_ads()` saves `ads_by_device.png`.  
6. **Model** — `prepare_ml_frame()` + `train_and_eval_logreg()` build a simple classifier and print accuracy.

### Analysis Workflow
```bash
make run        # or: python Consumer_Behavior.py
```
Outputs include console logs and the figure `ads_by_device.png` saved in the repo root.

### Visualizations
- `ads_by_device.png` — bar chart of mean engagement score by device (descending).

### How I Reached My Conclusions
- Cleaning ensures consistent labels and preserves true missing values.  
- Device-level aggregation shows relative engagement levels per device.  
- A minimal model checks whether device alone has signal for **High** engagement.

---

## Screenshots - Tests Passed

### CI Success
![CI Tests Passed](<Screenshots\CI passed test.PNG>)

### Local Tests Passing
![Local Tests Passed](<Screenshots\Passed Tests.PNG>)



---

## Troubleshooting
- **Windows & make:** If `make` isn’t found, add `C:\Program Files (x86)\GnuWin32\bin` to PATH or run the underlying Python commands directly.  
- **Black on notebooks:** This project formats `.py`. For notebooks, use `pip install "black[jupyter]"`.  
- **Line length errors:** CI/Makefile use `--max-line-length=100`.

---

## Data Source
Course-provided CSV: `Ecommerce_Consumer_Behavior_Analysis_Data.csv`.

## Author
Tea Tafaj — Duke University, IDS 706.