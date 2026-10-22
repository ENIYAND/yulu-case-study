# Yulu Demand Analysis: What Drives Electric Cycle Rentals?

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange)
![Stats](https://img.shields.io/badge/Focus-Hypothesis%20Testing%20%7C%20EDA-green)
[![Open In Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ENIYAND/yulu-case-study/HEAD?urlpath=lab)

Exploratory and statistical analysis of Yulu's electric cycle rentals. The goal is to find out which factors (day type, season, weather) significantly affect demand, and to turn those findings into operational and marketing recommendations.

---

## Table of Contents
1. [Business Problem](#business-problem)
2. [Dataset](#dataset)
3. [Questions and Hypotheses](#questions-and-hypotheses)
4. [Methodology](#methodology)
5. [Results](#results)
6. [Key Insights](#key-insights)
7. [Recommendations](#recommendations)
8. [Limitations and Next Steps](#limitations-and-next-steps)
9. [Repository Structure](#repository-structure)
10. [How to Run](#how-to-run)
11. [Tech Stack](#tech-stack)
12. [Contact](#contact)

---

## Business Problem

Yulu, a shared electric cycle provider, has seen a dip in revenue. This project looks at the demand side: **which factors significantly drive the number of rentals (`count`)?** Knowing this helps Yulu plan fleet deployment, target marketing, and forecast demand more reliably.

Because the dataset has no revenue or pricing column, rental count is used as the proxy for demand.

---

## Dataset

- **Source:** `bike_sharing.csv` from the Yulu case study (loaded directly from a hosted URL in the notebook)
- **Size:** 10,886 hourly records, 12 columns
- **Period:** 2011-01-01 to 2012-12-19
- **Quality:** no missing values, no duplicate rows

| Column | Description |
|---|---|
| `datetime` | Timestamp (hourly) |
| `season` | Season code, 1 to 4 |
| `holiday` | 1 if the day is a holiday, else 0 |
| `workingday` | 1 if neither weekend nor holiday, else 0 |
| `weather` | 1 Clear/Few clouds, 2 Mist/Cloudy, 3 Light Rain/Snow, 4 Heavy Rain/Snow |
| `temp` | Temperature (°C) |
| `atemp` | "Feels like" temperature (°C) |
| `humidity` | Relative humidity (%) |
| `windspeed` | Wind speed |
| `casual` | Rentals by non-registered users |
| `registered` | Rentals by registered users |
| `count` | Total rentals (`casual` + `registered`), the target variable |

**Target distribution:** mean 191.6, median 145, max 977. It is strongly right-skewed. Registered users account for roughly 81% of rentals.

---

## Questions and Hypotheses

| # | Question | Test | H0 |
|---|---|---|---|
| 1 | Does demand differ between working and non-working days? | 2-sample independent t-test | Mean `count` is equal on both day types |
| 2 | Does demand differ across weather conditions? | One-way ANOVA | Mean `count` is equal across weather types 1 to 3 |
| 3 | Does demand differ across seasons? | One-way ANOVA | Mean `count` is equal across all 4 seasons |
| 4 | Are weather and season related? | Chi-square test of independence | Season and weather are independent |

Significance level: **α = 0.05** for all tests.

---

## Methodology

1. **Data checks:** shape, dtypes, duplicates, constant columns, nulls.
2. **Preparation:** converted `datetime` and the categorical codes to proper types, and binned `temp`, `atemp`, `humidity` and `windspeed` into labelled categories for easier comparison.
3. **Univariate analysis:** histograms, KDE plots, count plots and boxplots for every variable.
4. **Bivariate analysis:** boxplots of `count`, `casual` and `registered` against every categorical variable and bin.
5. **Correlation:** heatmap of continuous variables. `temp` and `atemp` are correlated at 0.98, so `atemp` was dropped to avoid multicollinearity.
6. **Outlier analysis:** IQR rule by group. Outliers were **kept**, because they are genuine high-demand hours and the goal is inference, not prediction.
7. **Hypothesis testing:** assumption checks (Shapiro-Wilk, Levene, Q-Q plots) followed by the tests above.

---

## Results

| Test | Statistic / p-value | Decision |
|---|---|---|
| Working vs non-working day (t-test) | p = 0.226 | Fail to reject H0: no significant difference in total demand |
| Weather types 1 to 3 (ANOVA) | p ≈ 5.0e-43 | Reject H0: demand differs by weather |
| Season (ANOVA) | p ≈ 6.2e-149 | Reject H0: demand differs by season |
| Season × weather (chi-square) | χ² = 46.1, dof = 6, p ≈ 2.8e-8 | Reject H0: weather mix varies by season (small effect) |

**Assumption checks:** Shapiro-Wilk rejects normality in every group (expected for skewed count data). Levene's test passes for working day (p = 0.94) but fails for weather and season. Given the large sample sizes, the tests were run anyway and results were cross-checked against the boxplots. See [Limitations](#limitations-and-next-steps) for the robustness checks I'd add.

Weather type 4 (Heavy Rain/Snow) has a single observation, so it was excluded from the ANOVA and chi-square tests.

---

## Key Insights

- **Commuters vs leisure riders.** Registered users rent more on working days. Casual users rent more on non-working days and holidays. Total demand looks the same because the two effects offset each other.
- **Registered users are the stable core.** They make up about 81% of rentals, and their demand is steadier. Casual demand is more volatile and spikier.
- **Temperature is the strongest continuous driver.** Median hourly rentals by temperature band: **Cold 47, Mild 111, Warm 181, Hot 303**. There is no "too hot to ride" effect in this data.
- **Humidity hurts, wind barely matters.** Correlation with `count`: temp +0.39, humidity −0.32, windspeed +0.10.
- **Casual riders are more weather-sensitive.** Their correlation with temperature is 0.47 (registered: 0.32) and with humidity is −0.35 (registered: −0.27).
- **Worse weather means fewer rentals.** Demand is highest in clear weather and drops sharply in light rain or snow.
- **Seasonality is strong.** The first season of the year (coldest) has by far the lowest demand, and the hottest season has the highest.
- **Holidays shift the mix.** Casual rentals rise and registered rentals fall, with little net change in total.

---

## Recommendations

1. **Segment by day type.**
   - *Working days:* put bikes near offices, metro stations and commuter routes, and target registered users with reliability and pass-style offers.
   - *Non-working days and holidays:* shift bikes and marketing to parks and leisure spots, with all-day or group offers for casual riders.
2. **Plan the fleet by season.** Deploy the full fleet in high-demand seasons. In the lowest-demand season, reduce the active fleet and use the window for heavy maintenance and battery replacement.
3. **React to the daily forecast.** Maximise availability on clear days. On light rain or snow days, reduce the active fleet and schedule maintenance.
4. **Don't pull bikes on hot days.** Heat is a peak-demand condition here.
5. **Treat casual demand as forecast-dependent.** It needs the weather forecast to plan around, while registered demand can be planned more steadily.

---

## Limitations and Next Steps

Being upfront about what this analysis does and does not show:

- **Demand is a proxy for revenue.** The data has no price or revenue field, so the revenue dip itself can't be tested.
- **Normality and equal-variance assumptions fail** for the ANOVAs. A **Kruskal-Wallis** test and **post-hoc pairwise tests (Tukey/Dunn)** would confirm the group differences and the ordering of seasons and weather types.
- **Statistical vs practical significance.** The season × weather association is significant, but the effect is small (Cramér's V ≈ 0.05). Effect sizes should be reported alongside p-values.
- **Season labels need verification.** The dataset documentation and the temperature pattern disagree on season names. Mapping season codes to calendar months would settle this.
- **Zero values in `windspeed` and `humidity`.** Both variables have a spike at 0 that may be a missing-data code. The "calm vs breezy" findings should be treated as tentative until these are investigated.
- **No time dimension yet.** Hour-of-day (commute peaks) and the 2011 vs 2012 growth trend are not analysed, and both likely confound the season comparison.
- **Next steps:** add hour-of-day and year effects, run a multivariate model (e.g. regression or gradient boosting on weather, season, hour and day type) to separate overlapping effects, and build a simple demand forecast.

---

## Repository Structure

```
yulu-case-study/
├── notebooks/
│   └── 01-yulu-exploratory-analysis.ipynb   # Full analysis, plots and tests
├── reports/
│   └── YULU-case-study.pdf                  # Printable report
├── src/                                     # Helper scripts (data processing, plotting)
├── data/                                    # Sample data / instructions to get the full dataset
├── figures/                                 # Static images used in the report
├── requirements.txt
└── README.md
```

---

## How to Run

**Locally**

```bash
git clone https://github.com/ENIYAND/yulu-case-study.git
cd yulu-case-study
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Then open `notebooks/01-yulu-exploratory-analysis.ipynb` and run all cells. The notebook downloads the dataset from its hosted URL, so an internet connection is needed. If you prefer offline use, download `bike_sharing.csv` into `data/` and change the `pd.read_csv(...)` path.

**On Binder:** click the badge at the top. No setup needed.

**`requirements.txt`**

```
numpy
pandas
matplotlib
seaborn
scipy
statsmodels
scikit-learn
pingouin
jupyterlab
```

---

## Tech Stack

- **Language:** Python
- **Analysis:** pandas, NumPy, SciPy, statsmodels
- **Visualisation:** Matplotlib, seaborn
- **Environment:** Jupyter, Google Colab, Binder

---

## Contact

**Eniyan D**
Email: umayalini64@gmail.com
LinkedIn: [linkedin.com/in/tamil-eniyan-](https://www.linkedin.com/in/tamil-eniyan-)
GitHub: [ENIYAND](https://github.com/ENIYAND)
