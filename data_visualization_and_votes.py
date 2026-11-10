"""
Task 3 & 5: Data Visualization & Votes Analysis
Internship Track: Data Analyst
Company: SAM AI Technologies

Objectives:
1. Identify restaurants with highest and lowest votes.
2. Determine if there is a correlation between the number of votes and restaurant ratings.
3. Build a comprehensive visual dashboard displaying ratings, costs, delivery, and votes.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_votes_and_visualization_analysis(csv_file="restaurant_dataset.csv"):
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}")

    # 1. Pearson Correlation
    correlation = df['Votes'].corr(df['Aggregate_Rating'])
    print(f"\nPearson Correlation between Votes and Rating: {correlation:.3f}")

    # 2. Highest and Lowest Voted Restaurants
    print("\n--- Top 5 Most Voted Restaurants ---")
    print(df.sort_values(by='Votes', ascending=False)[['Restaurant_Name', 'City', 'Votes', 'Aggregate_Rating']].head(5))

    print("\n--- Top 5 Lowest Voted Restaurants ---")
    print(df.sort_values(by='Votes', ascending=True)[['Restaurant_Name', 'City', 'Votes', 'Aggregate_Rating']].head(5))

    # 3. 4-Panel Visualization Dashboard
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # A. Regression Plot: Votes vs. Rating
    sns.regplot(
        data=df, x='Aggregate_Rating', y='Votes',
        scatter_kws={'alpha': 0.6, 'color': '#2b5c8f'},
        line_kws={'color': '#d95f02', 'linewidth': 2},
        ax=axes[0, 0]
    )
    axes[0, 0].set_title(f"Votes vs. Rating Correlation (r = {correlation:.2f})", fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel("Aggregate Rating (1–5)", fontsize=11)
    axes[0, 0].set_ylabel("Total Votes", fontsize=11)

    # B. Rating Distribution
    sns.histplot(df['Aggregate_Rating'], bins=15, kde=True, color='#2ca02c', ax=axes[0, 1])
    axes[0, 1].set_title("Distribution of Customer Ratings", fontsize=13, fontweight='bold')
    axes[0, 1].set_xlabel("Rating", fontsize=11)
    axes[0, 1].set_ylabel("Frequency", fontsize=11)

    # C. Cost for Two vs Online Delivery
    sns.boxplot(
        data=df, x='Has_Online_delivery', y='Average_Cost_for_two',
        hue='Has_Online_delivery', palette='Set2', legend=False,
        ax=axes[1, 0]
    )
    axes[1, 0].set_title("Average Cost for Two vs. Online Delivery", fontsize=13, fontweight='bold')
    axes[1, 0].set_xlabel("Online Delivery Available", fontsize=11)
    axes[1, 0].set_ylabel("Cost for Two (INR)", fontsize=11)

    # D. Top 10 Most Voted Restaurants
    top10_voted = df.sort_values(by='Votes', ascending=False).head(10)
    sns.barplot(
        data=top10_voted, x='Votes', y='Restaurant_Name',
        hue='Restaurant_Name', palette='rocket', legend=False,
        ax=axes[1, 1]
    )
    axes[1, 1].set_title("Top 10 Most Voted Restaurants", fontsize=13, fontweight='bold')
    axes[1, 1].set_xlabel("Total Votes", fontsize=11)
    axes[1, 1].set_ylabel("Restaurant Name", fontsize=11)

    plt.tight_layout()
    plt.savefig("restaurant_analysis_dashboard.png", dpi=300)
    print("\nVisual dashboard exported to 'restaurant_analysis_dashboard.png'")

if __name__ == "__main__":
    run_votes_and_visualization_analysis()
