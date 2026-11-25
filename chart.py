"""Card-minus-cash gap under three comparisons. Usage: python chart.py path/to/csv"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv(sys.argv[1], index_col=0)
d = df[df.payment_type.isin([1, 2])].copy()
fmt = "%m/%d/%Y %I:%M:%S %p"
d["minutes"] = (pd.to_datetime(d.tpep_dropoff_datetime, format=fmt)
                - pd.to_datetime(d.tpep_pickup_datetime, format=fmt)).dt.total_seconds() / 60
d = d[(d.fare_amount > 0) & (d.fare_amount <= 200) & (d.trip_distance > 0)
      & (d.minutes > 0) & (d.minutes <= 180)].copy()
d["card"] = (d.payment_type == 1).astype(int)

specs = [("Total amount\n(includes card tips only)", "total_amount ~ card"),
         ("Metered fare\n(tips excluded)", "fare_amount ~ card"),
         ("Metered fare, holding\ntrip distance constant", "fare_amount ~ card + trip_distance")]
rows = []
for label, f in specs:
    m = smf.ols(f, data=d).fit(cov_type="HC3")
    lo, hi = m.conf_int().loc["card"]
    rows.append((label, m.params["card"], lo, hi))

surface, ink, muted, grid, blue = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0", "#2a78d6"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": ink})
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=150, facecolor=surface)
ax.set_facecolor(surface)
y = np.arange(len(rows))[::-1]
for yi, (_, est, lo, hi) in zip(y, rows):
    ax.plot([lo, hi], [yi, yi], color=blue, lw=2, solid_capstyle="round")
    ax.plot(est, yi, "o", ms=11, color=blue, mec=surface, mew=2)
    ax.annotate(f"${est:.2f}", (est, yi), textcoords="offset points",
                xytext=(10, 14) if est < 0.3 else (0, 14), ha="left" if est < 0.3 else "center", fontsize=14, color=ink)
ax.axvline(0, color=muted, lw=1)
ax.set_yticks(y, [r[0] for r in rows], fontsize=13)
ax.set_ylim(-0.6, len(rows) - 0.4)
ax.set_xlim(-0.4, 4.6)
ax.set_xlabel("Card minus cash, USD per trip (point estimate and 95% interval)", color=muted, fontsize=12)
ax.xaxis.grid(True, color=grid, lw=1)
ax.set_axisbelow(True)
ax.tick_params(length=0, colors=muted)
ax.tick_params(axis="y", labelcolor=ink)
for s in ax.spines.values():
    s.set_visible(False)
fig.subplots_adjust(left=0.25, right=0.97, top=0.80, bottom=0.17)
fig.text(0.03, 0.93, "Most of the card–cash gap is tips and trip length", fontsize=20, fontweight="bold")
fig.text(0.03, 0.865, f"{len(d):,} trips, 2017 NYC yellow taxi course sample. Observational: not an experiment.",
         fontsize=12.5, color=muted)
fig.text(0.03, 0.035, "Cash tips are not recorded in TLC data. Dataset altered by the course provider for teaching.",
         fontsize=10.5, color=muted)
fig.savefig("card_cash_gap.png", facecolor=surface)
print(rows)
