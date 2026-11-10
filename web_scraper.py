"""
Task 1: Web Scraping & Data Extraction
Internship Track: Data Analyst
Organization: SAM AI Technologies

Description:
This script extracts book data from 'Books to Scrape' (http://books.toscrape.com/),
a sandbox website specifically designed for testing web scrapers.
It extracts book titles, prices, ratings, and stock status across multiple pages,
cleans the data with Pandas, saves it as a CSV, and generates analytical visualizations.
"""

import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RATING_MAP = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}

BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'

def scrape_books(num_pages=5):
    """Scrapes book information from multiple pages."""
    books_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    print(f"Starting web scraping across {num_pages} pages...")
    for page in range(1, num_pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping Page {page}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch page {page} (Status: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_='product_pod')

            for article in articles:
                # Title
                title_tag = article.h3.find('a')
                title = title_tag['title'] if 'title' in title_tag.attrs else title_tag.text

                # Price (clean currency symbol)
                price_text = article.find('p', class_='price_color').text
                price = float(re.sub(r'[^\d.]', '', price_text))

                # Rating
                rating_class = article.find('p', class_='star-rating')['class']
                rating_word = [cls for cls in rating_class if cls != 'star-rating'][0]
                rating = RATING_MAP.get(rating_word, 0)

                # Availability
                availability_text = article.find('p', class_='instock availability').text.strip()
                in_stock = 1 if 'In stock' in availability_text else 0

                # Relative Link
                relative_link = title_tag['href']
                full_link = f"http://books.toscrape.com/catalogue/{relative_link}"

                books_data.append({
                    'Title': title,
                    'Price_GBP': price,
                    'Rating_Stars': rating,
                    'In_Stock': in_stock,
                    'Availability': availability_text,
                    'URL': full_link
                })

            time.sleep(1) # Polite scraping delay
        except Exception as e:
            print(f"Error on page {page}: {e}")

    df = pd.DataFrame(books_data)
    print(f"\nScraping complete! Total books extracted: {len(df)}")
    return df

def generate_insights_and_plots(df, output_dir="output"):
    """Generates summary statistics and data visualizations."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "scraped_books_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved dataset to {csv_path}")

    # Summary Statistics
    print("\n--- Summary Statistics ---")
    print(f"Total Records: {len(df)}")
    print(f"Average Price: £{df['Price_GBP'].mean():.2f}")
    print(f"Min Price: £{df['Price_GBP'].min():.2f}")
    print(f"Max Price: £{df['Price_GBP'].max():.2f}")
    print(f"Average Star Rating: {df['Rating_Stars'].mean():.2f} / 5.0")
    print("\nRating Distribution:")
    print(df['Rating_Stars'].value_counts().sort_index())

    # Visualizations
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Rating Distribution
    sns.countplot(data=df, x='Rating_Stars', palette='Blues_d', ax=axes[0])
    axes[0].set_title("Distribution of Book Ratings (Stars)", fontsize=13, fontweight='bold')
    axes[0].set_xlabel("Star Rating (1 - 5)", fontsize=11)
    axes[0].set_ylabel("Count of Books", fontsize=11)

    # Plot 2: Price by Rating Boxplot
    sns.boxplot(data=df, x='Rating_Stars', y='Price_GBP', palette='Set2', ax=axes[1])
    axes[1].set_title("Book Price (£) by Star Rating", fontsize=13, fontweight='bold')
    axes[1].set_xlabel("Star Rating", fontsize=11)
    axes[1].set_ylabel("Price (£)", fontsize=11)

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "scraping_analysis_charts.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Saved analysis plots to {chart_path}")

if __name__ == "__main__":
    df = scrape_books(num_pages=5)
    generate_insights_and_plots(df)
