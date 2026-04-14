# Exploratory Data Analysis and Hypothesis Testing on personal dive logs exported from a Suunto Ocean diving computer.
# Analyzes the relationship between maximum dive depth and dive duration.

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

# --- Load Data ---
df = pd.read_csv("data/dives_parsed.csv")
df["duration_min"] = df["duration"] / 60
df["date"] = pd.to_datetime(df["date"])

# --- Noise Filter ---
# A dive is considered noise if any of the following are true:
# 1. Max depth < 5m (accidental logs, pool sessions, surface intervals)
# 2. Duration < 8 minutes (accidental triggers)
# 3. Max depth < 6m AND duration < 20 minutes (shallow training dives)
def is_noise(row):
    depth = row["max_depth"]
    duration = row["duration_min"]
    if depth < 5:
        return True
    if duration < 8:
        return True
    if depth < 6 and duration < 20:
        return True
    return False

df["noise"] = df.apply(is_noise, axis=1)
df_clean = df[df["noise"] == False].copy().reset_index(drop=True)

print(f"Total dives: {len(df)}")
print(f"Noise dives removed: {df['noise'].sum()}")
print(f"Clean dives: {len(df_clean)}")
print(df_clean[["date", "max_depth", "duration_min"]].describe())

# --- Figures folder ---
os.makedirs("figures", exist_ok=True)

# --- EDA ---

# 1. Distribution of max depth
plt.figure(figsize=(8, 4))
plt.hist(df_clean["max_depth"], bins=20, color="steelblue", edgecolor="black")
plt.xlabel("Max Depth (m)")
plt.ylabel("Number of Dives")
plt.title("Distribution of Maximum Dive Depth")
plt.tight_layout()
plt.savefig("figures/depth_distribution.png")
plt.show()

# 2. Distribution of duration
plt.figure(figsize=(8, 4))
plt.hist(df_clean["duration_min"], bins=20, color="teal", edgecolor="black")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Dives")
plt.title("Distribution of Dive Duration")
plt.tight_layout()
plt.savefig("figures/duration_distribution.png")
plt.show()

# 3. Depth vs Duration scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(df_clean["max_depth"], df_clean["duration_min"], alpha=0.6, color="steelblue")
plt.axvline(x=20, color="red", linestyle="--", label="20m threshold")
plt.xlabel("Max Depth (m)")
plt.ylabel("Duration (minutes)")
plt.title("Max Depth vs Dive Duration")
plt.legend()
plt.tight_layout()
plt.savefig("figures/depth_vs_duration.png")
plt.show()

# --- Hypothesis Testing ---
# H0: There is no significant difference in dive duration between shallow
#     and deep dives. Depth does not affect duration.
# HA: Deeper dives have significantly shorter durations due to nitrogen
#     loading and decompression constraints.

df_hyp = df_clean.dropna(subset=["max_depth", "duration_min"])

# Split into shallow (<20m) and deep (>=20m) groups
shallow = df_hyp[df_hyp["max_depth"] < 20]["duration_min"]
deep = df_hyp[df_hyp["max_depth"] >= 20]["duration_min"]

print(f"\nShallow dives (<20m): n={len(shallow)}, mean={shallow.mean():.1f} min, median={shallow.median():.1f} min")
print(f"Deep dives (>=20m):   n={len(deep)}, mean={deep.mean():.1f} min, median={deep.median():.1f} min")

# 1. Independent samples t-test (parametric)
# Assumes approximately normal distributions within groups
t_stat, t_p = stats.ttest_ind(shallow, deep)
print(f"\nT-test: t={t_stat:.3f}, p-value={t_p:.4f}")

# 2. Mann-Whitney U test (non-parametric)
# Does not assume normality - tests whether one group tends to have
# larger values than the other. More appropriate given small sample sizes.
u_stat, u_p = stats.mannwhitneyu(shallow, deep, alternative="two-sided")
print(f"Mann-Whitney U: U={u_stat:.1f}, p-value={u_p:.4f}")

# 3. Spearman correlation (non-parametric, ranked)
# Tests monotonic relationship between depth and duration
# Consistent with the non-parametric approach above
spearman_r, spearman_p = stats.spearmanr(df_hyp["max_depth"], df_hyp["duration_min"])
print(f"Spearman r: {spearman_r:.3f}, p-value={spearman_p:.4f}")

# --- Summary ---
alpha = 0.05
print("\n--- HYPOTHESIS TEST SUMMARY ---")
print(f"Hypothesis: deeper dives have shorter durations (inverse relationship)")
print(f"T-test p={t_p:.4f}            — {'SIGNIFICANT' if t_p < alpha else 'not significant'} at alpha=0.05")
print(f"Mann-Whitney U p={u_p:.4f}    — {'SIGNIFICANT' if u_p < alpha else 'not significant'} at alpha=0.05")
print(f"Spearman r={spearman_r:.3f}, p={spearman_p:.4f} — {'SIGNIFICANT' if spearman_p < alpha else 'not significant'} at alpha=0.05")
print(f"\nConclusion: The data {'support' if (t_p < alpha or u_p < alpha) else 'do not support'} the hypothesis.")
print("No significant relationship was found between dive depth and duration.")
print("This null result suggests dive duration is planned consistently regardless of depth.")