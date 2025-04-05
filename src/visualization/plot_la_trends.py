"""
Plot LA intake trends over time for Australia.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Set style
plt.style.use('bmh')  # Using a built-in style that works well for time series

# Load data
data_dir = Path('data')
metrics_df = pd.read_csv(data_dir / 'processed' / 'australia_dietary_metrics.csv')

# Create figure and axis
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[2, 1])
fig.suptitle('Linoleic Acid (LA) Intake Trends in Australia (1961-2013)', fontsize=14, y=0.95)

# Plot LA intake
ax1.plot(metrics_df['Year'], metrics_df['Total_LA_Intake_g_per_capita_day'], 
         linewidth=2, marker='o', markersize=4, color='#2077B4')
ax1.set_ylabel('LA Intake (g/person/day)')
ax1.set_title('Daily LA Intake per Capita')
ax1.grid(True, alpha=0.3)

# Plot % calories from LA
ax2.plot(metrics_df['Year'], metrics_df['LA_Intake_percent_calories'], 
         linewidth=2, marker='o', markersize=4, color='#D62728')
ax2.set_ylabel('% of Total Calories from LA')
ax2.set_xlabel('Year')
ax2.set_title('Percentage of Total Calories from LA')
ax2.grid(True, alpha=0.3)

# Add annotations for key statistics
avg_la = metrics_df['Total_LA_Intake_g_per_capita_day'].mean()
avg_pct = metrics_df['LA_Intake_percent_calories'].mean()
ax1.text(0.02, 0.95, f'Average: {avg_la:.1f} g/day', 
         transform=ax1.transAxes, fontsize=10)
ax2.text(0.02, 0.95, f'Average: {avg_pct:.1f}%', 
         transform=ax2.transAxes, fontsize=10)

# Adjust layout
plt.tight_layout()

# Save plot
output_dir = Path('figures')
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / 'la_intake_trends.png', dpi=300, bbox_inches='tight')
plt.close() 