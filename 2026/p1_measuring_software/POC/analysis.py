import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.parse import urlparse
import os
from config import OUTPUT_FILE, POWER_COLUMN

# --- 1. Load and Prepare the Data ---
try:
    df = pd.read_csv(OUTPUT_FILE)
except FileNotFoundError:
    print(f"Error: The file '{OUTPUT_FILE}' was not found.")
    exit()

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['adblock_enabled'] = df['adblock_enabled'].astype(bool)

def shorten_url(url):
    return urlparse(url).netloc

# --- 2. Aggregate Per Experiment (last row = cumulative network totals) ---
# Network bytes are cumulative counters, so take the last value per experiment.
# Power is a time-series reading, so take the mean.
agg_dict = {
    POWER_COLUMN: 'mean',
    'total_bytes': 'last',
    'ad_bytes': 'last',
    'total_requests': 'last',
    'ad_requests': 'last',
    'blocked_by_client_requests': 'last'
}
grouped = df.groupby(['url', 'adblock_enabled']).agg(agg_dict).reset_index()
grouped['total_mb'] = grouped['total_bytes'] / (1024 * 1024)
grouped['ad_mb'] = grouped['ad_bytes'] / (1024 * 1024)
grouped['website'] = grouped['url'].apply(shorten_url)
grouped['Condition'] = grouped['adblock_enabled'].map({True: 'With Adblock', False: 'Without Adblock'})

# --- 3. Pivot for Summary Table ---
power_pivot = grouped.pivot(index='url', columns='adblock_enabled', values=POWER_COLUMN)
power_pivot.columns = ['Power (Without Adblock)', 'Power (With Adblock)']

data_pivot = grouped.pivot(index='url', columns='adblock_enabled', values='total_mb')
data_pivot.columns = ['Data MB (Without Adblock)', 'Data MB (With Adblock)']

summary = pd.concat([power_pivot, data_pivot], axis=1)

summary['Power Reduction (%)'] = (
    (summary['Power (Without Adblock)'] - summary['Power (With Adblock)'])
    / summary['Power (Without Adblock)'] * 100
)
summary['Data Reduction (%)'] = (
    (summary['Data MB (Without Adblock)'] - summary['Data MB (With Adblock)'])
    / summary['Data MB (Without Adblock)'] * 100
)

print("\n" + "="*80)
print("Per-Website Power and Data Consumption Analysis")
print("="*80)
print(summary.to_string(float_format="%.2f"))
print("="*80 + "\n")

diff_df = pd.DataFrame({
    'delta_power': summary['Power (Without Adblock)'] - summary['Power (With Adblock)'],
    'delta_mb': summary['Data MB (Without Adblock)'] - summary['Data MB (With Adblock)']
})
diff_corr = diff_df.corr().iloc[0, 1]
print(f"Correlation of Δpower vs Δdata (adblock effect, n=14): r = {diff_corr:.3f}")

# Correlation between data downloaded and power (across all 28 site+condition combos)
corr = grouped[[POWER_COLUMN, 'total_mb']].corr().iloc[0, 1]
print(f"Pearson correlation (data downloaded vs. avg power): r = {corr:.3f}\n")

# --- 4. Plots ---
sns.set_theme(style="whitegrid")
palette = {'Without Adblock': 'orangered', 'With Adblock': 'mediumseagreen'}

# a) Existing power bar chart
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=grouped, x='website', y=POWER_COLUMN, hue='Condition',
            palette=palette, ax=ax)
ax.set_title('Average CPU Package Power by Website', fontsize=14)
ax.set_ylabel('Power (Watts)')
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig('power_by_site.png', dpi=150)
plt.show()

# b) Data downloaded bar chart
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=grouped, x='website', y='total_mb', hue='Condition',
            palette=palette, ax=ax)
ax.set_title('Total Data Downloaded by Website', fontsize=14)
ax.set_ylabel('Data Downloaded (MB)')
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig('data_by_site.png', dpi=150)
plt.show()

# c) Scatter: data downloaded vs. power, colored by condition
fig, ax = plt.subplots(figsize=(9, 6))
for condition, grp in grouped.groupby('Condition'):
    ax.scatter(grp['total_mb'], grp[POWER_COLUMN],
               label=condition, color=palette[condition],
               s=80, alpha=0.8, zorder=3)
    # Annotate each point with the site name
    for _, row in grp.iterrows():
        ax.annotate(row['website'], (row['total_mb'], row[POWER_COLUMN]),
                    fontsize=7, alpha=0.7,
                    xytext=(4, 4), textcoords='offset points')

ax.set_xlabel('Total Data Downloaded (MB)')
ax.set_ylabel('Average Power (Watts)')
ax.set_title('Data Downloaded vs. Power Consumption', fontsize=14)
ax.legend(title='Condition')
plt.tight_layout()
plt.savefig('scatter_data_vs_power.png', dpi=150)
plt.show()