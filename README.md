# Yulu Case Study

**Short summary:** Analysis of Yulu bike rentals to identify demand drivers (seasonality, weather, user types) and business recommendations.

---

## Repo contents
- `notebooks/01-yulu-exploratory-analysis.ipynb` — final Jupyter notebook with analysis and plots.
- `reports/YULU-case-study.pdf` — printable report (moved here from local upload).
  - Original uploaded path (local): `/mnt/data/YULU-case-study.pdf`
- `src/` — helper scripts (data processing, plotting).
- `data/` — small sample data or instructions to obtain the full dataset.
- `figures/` — static images used in the report.

---

## TL;DR — Key findings
-  Working Days: Dominated by registered (commuter) users.
   Non-Working Days: Dominated by casual (leisure) users.
-  Both weather and season have a massive impact on rental count.
-  Casual Riders are More Weather-Sensitive.correlation heatmap showed that different user types react to weather with different sensitivity.
-  weather=1 (Clear): Maximize bike availability. These are the highest-demand days.weather=3 (Light Rain/Snow): Minimize the active fleet. Demand is lowest.
   Pull bikes for maintenance.

---

## Badges / Demos
- Report PDF: reports/YULU-case-study.pdf
  
---

## Launch Notebook in Binder
[![Open In Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/eniyand/yulu-case-study/main?urlpath=lab)

---
## Contact
ENIYAN D — umayalini64@gmail.com
LinkedIn - www.linkedin.com/in/tamil-eniyan-


## How to run locally
```bash
git clone https://github.com/<your-username>/yulu-case-study.git
cd yulu-case-study
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
jupyter lab
# open notebooks/01-yulu-exploratory-analysis.ipynb
