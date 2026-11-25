"""Payment type and fare in a 2017 NYC yellow taxi sample (observational re-analysis).

Usage: python analysis.py path/to/2017_Yellow_Taxi_Trip_Data.csv
"""
import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv(sys.argv[1], index_col=0)
print(f"Rows in file: {len(df):,}")

# payment_type 1 = credit card, 2 = cash
d = df[df.payment_type.isin([1, 2])].copy()
print(f"Card or cash trips: {len(d):,}")
d["card"] = (d.payment_type == 1).astype(int)
d["pickup"] = pd.to_datetime(d.tpep_pickup_datetime, format="%m/%d/%Y %I:%M:%S %p")
d["dropoff"] = pd.to_datetime(d.tpep_dropoff_datetime, format="%m/%d/%Y %I:%M:%S %p")
d["minutes"] = (d.dropoff - d.pickup).dt.total_seconds() / 60

print("\nData quality flags (card and cash trips)")
flags = {
    "fare <= 0": d.fare_amount <= 0,
    "distance <= 0": d.trip_distance <= 0,
    "duration <= 0": d.minutes <= 0,
    "duration > 180 min": d.minutes > 180,
    "fare > 200": d.fare_amount > 200,
    "cash trip with a recorded tip": (d.card == 0) & (d.tip_amount > 0),
}
for name, mask in flags.items():
    print(f"  {name}: {int(mask.sum())}")

bad = (d.fare_amount <= 0) | (d.trip_distance <= 0) | (d.minutes <= 0) | (d.minutes > 180) | (d.fare_amount > 200)
c = d[~bad].copy()
print(f"Trips kept after filtering: {len(c):,} (removed {int(bad.sum()):,})")


def compare(data, col, label):
    a, b = data.loc[data.card == 1, col], data.loc[data.card == 0, col]
    res = stats.ttest_ind(a, b, equal_var=False)
    se2a, se2b = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = np.sqrt(se2a + se2b)
    dof = (se2a + se2b) ** 2 / (se2a**2 / (len(a) - 1) + se2b**2 / (len(b) - 1))
    diff = a.mean() - b.mean()
    half = stats.t.ppf(0.975, dof) * se
    pooled = np.sqrt(((len(a) - 1) * a.var() + (len(b) - 1) * b.var()) / (len(a) + len(b) - 2))
    print(f"{label:38s} card {a.mean():6.2f}  cash {b.mean():6.2f}  diff {diff:5.2f} "
          f"[95% CI {diff - half:5.2f}, {diff + half:5.2f}]  d={diff / pooled:4.2f}  "
          f"t={res.statistic:5.2f}  p={res.pvalue:.2g}  n={len(a):,}/{len(b):,}")


print("\nWelch comparisons, USD")
compare(d, "total_amount", "total_amount, unfiltered (original)")
compare(d, "fare_amount", "fare_amount, unfiltered")
compare(c, "total_amount", "total_amount, filtered")
compare(c, "fare_amount", "fare_amount, filtered")
compare(c, "trip_distance", "trip_distance (miles), filtered")

tip_gap = c.loc[c.card == 1, "tip_amount"].mean() - c.loc[c.card == 0, "tip_amount"].mean()
total_gap = c.loc[c.card == 1, "total_amount"].mean() - c.loc[c.card == 0, "total_amount"].mean()
print(f"\nRecorded tips account for {tip_gap:.2f} of the {total_gap:.2f} filtered total_amount gap "
      f"({tip_gap / total_gap:.0%}).")

print("\nOLS on fare_amount, HC3 robust standard errors (association, not causation)")
for formula in ["fare_amount ~ card",
                "fare_amount ~ card + trip_distance",
                "fare_amount ~ card + trip_distance + minutes + C(RatecodeID)"]:
    m = smf.ols(formula, data=c).fit(cov_type="HC3")
    lo, hi = m.conf_int().loc["card"]
    print(f"  {formula:62s} card={m.params['card']:6.3f} [{lo:6.3f}, {hi:6.3f}] "
          f"p={m.pvalues['card']:.2g} R2={m.rsquared:.3f}")
