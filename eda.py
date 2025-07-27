import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load dataset
file_path = r"C:\Users\askar\Desktop\Flipkart_retail_analysis\data\flipkart_com-ecommerce_sample.csv"
df = pd.read_csv(file_path)

# Clean columns
df.columns = df.columns.str.strip()

# Handle missing values
df.dropna(subset=['discounted_price', 'retail_price'], inplace=True)

# Convert prices to numeric
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce')
df['discount_percent'] = ((df['retail_price'] - df['discounted_price']) / df['retail_price']) * 100

# Plot 1: Distribution of Discount %
plt.figure()
sns.histplot(df['discount_percent'], bins=30, kde=True)
plt.title('Distribution of Discount %')
plt.xlabel('Discount %')
plt.ylabel('Count')
plt.tight_layout()

# Plot 2: Distribution of Ratings
plt.figure()
sns.histplot(df['product_rating'].dropna(), bins=20, kde=True)
plt.title('Distribution of Product Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.tight_layout()

# Plot 3: Category count (excluding top 10)
plt.figure()
top_categories = df['product_category_tree'].value_counts().nlargest(10).index
filtered = df[~df['product_category_tree'].isin(top_categories)]
category_counts = filtered['product_category_tree'].value_counts().nlargest(20)
sns.barplot(x=category_counts.values, y=category_counts.index)
plt.title('Product Count by Category (Excl. Top 10)')
plt.xlabel('Count')
plt.ylabel('Category')
plt.tight_layout()

# Plot 4: Price distribution by category (top 5 categories only)
plt.figure()
top_5 = df['product_category_tree'].value_counts().nlargest(5).index
sns.boxplot(data=df[df['product_category_tree'].isin(top_5)],
            x='product_category_tree', y='discounted_price')
plt.title('Discounted Price by Top 5 Categories')
plt.xticks(rotation=45)
plt.tight_layout()

# Plot 5: Discount % vs Product Rating
plt.figure()
sns.scatterplot(data=df, x='discount_percent', y='product_rating', alpha=0.5)
plt.title('Discount % vs Product Rating')
plt.xlabel('Discount %')
plt.ylabel('Rating')
plt.tight_layout()

# Plot 6: Top 20 Brands by Product Count
if 'brand' in df.columns:
    plt.figure()
    top_brands = df['brand'].value_counts().nlargest(20)
    sns.barplot(x=top_brands.values, y=top_brands.index)
    plt.title('Top 20 Brands by Product Count')
    plt.xlabel('Count')
    plt.ylabel('Brand')
    plt.tight_layout()

# Plot 7: Correlation Heatmap (for numeric columns)
plt.figure()
numeric_cols = df.select_dtypes(include='number')
corr = numeric_cols.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.tight_layout()

# Plot 8: Price vs Discount %
plt.figure()
sns.scatterplot(data=df, x='retail_price', y='discount_percent', alpha=0.5)
plt.title('Retail Price vs Discount %')
plt.xlabel('Retail Price')
plt.ylabel('Discount %')
plt.tight_layout()

# Show all plots at once
plt.show()
