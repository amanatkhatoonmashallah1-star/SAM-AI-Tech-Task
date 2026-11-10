"""
Task 2: Cuisine Combination Analysis
Internship Track: Data Analyst
Company: SAM AI Technologies

Objectives:
1. Identify the most common combinations of cuisines in the dataset.
2. Determine if certain cuisine combinations tend to have higher customer ratings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_cuisine_combinations(csv_file="restaurant_dataset.csv"):
    # Load dataset
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} restaurant records from {csv_file}")

    # 1. Most common combinations of cuisines
    combo_counts = df['Cuisines'].value_counts()
    print("\n--- Top 10 Most Common Cuisine Combinations ---")
    print(combo_counts.head(10))

    # 2. Rating performance across cuisine combinations (minimum 5 restaurant sample)
    combo_stats = df.groupby('Cuisines').agg(
        Average_Rating=('Aggregate_Rating', 'mean'),
        Restaurant_Count=('Restaurant_ID', 'count')
    ).query('Restaurant_Count >= 5').sort_values(by='Average_Rating', ascending=False)

    print("\n--- Top Rated Cuisine Combinations (Min 5 Outlets) ---")
    print(combo_stats.head(10))

    # 3. Visualizations
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    top10_combos = combo_counts.head(10)
    sns.barplot(x=top10_combos.values, y=top10_combos.index, hue=top10_combos.index, palette="mako", legend=False, ax=axes[0])
    axes[0].set_title("Top 10 Most Common Cuisine Combinations", fontsize=14, fontweight='bold')
    axes[0].set_xlabel("Number of Restaurants", fontsize=12)
    axes[0].set_ylabel("Cuisine Combination", fontsize=12)

    top_rated = combo_stats.head(8)
    sns.barplot(x=top_rated['Average_Rating'], y=top_rated.index, hue=top_rated.index, palette="viridis", legend=False, ax=axes[1])
    axes[1].set_title("Highest Rated Cuisine Combinations (Min 5 Outlets)", fontsize=14, fontweight='bold')
    axes[1].set_xlabel("Average Aggregate Rating (out of 5.0)", fontsize=12)
    axes[1].set_xlim(3.0, 5.0)
    axes[1].set_ylabel("")

    plt.tight_layout()
    plt.savefig("cuisine_combination_analysis.png", dpi=300)
    print("\nAnalysis chart saved as 'cuisine_combination_analysis.png'")

if __name__ == "__main__":
    analyze_cuisine_combinations()
