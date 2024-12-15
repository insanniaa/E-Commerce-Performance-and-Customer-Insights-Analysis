import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from babel.numbers import format_currency

# Function to prepare and filter data
def prepare_data(df, start_date, end_date):
    # Ensure 'order_approved_at' is a datetime column
    df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])
    
    # Convert start_date and end_date to pandas.Timestamp
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # Filter dataframe based on the selected date range
    filtered_df = df[(df['order_approved_at'] >= start_date) & (df['order_approved_at'] <= end_date)]
    return filtered_df

#MELENGKAPI DASHBOARD DENGAN BERBAGAI VISUALISASI DATA
st.header('E-Commerce Public Dashboard :')

# Load data
final_df = pd.read_csv(r"C:\Users\ACER\Documents\course\dicoding\projek\Proyek Analisis Data\dashboard\final_df.csv")

# Create date input for filtering
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2016-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2018-12-31"))

# Prepare filtered data
filtered_df = prepare_data(final_df, start_date, end_date)

# Daily orders: Count and revenue
st.write("## Daily Orders")
daily_orders_df = filtered_df.resample('D', on='order_approved_at').agg({
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

daily_orders_df.rename(columns={
    "order_approved_at": "order_date",
    "order_id": "order_count",
    "price": "revenue"
}, inplace=True)

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='en_AU') 
    st.metric("Total Revenue", value=total_revenue)


# Plot daily orders
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(daily_orders_df['order_date'], daily_orders_df['order_count'], color='b', alpha=0.6, label='Jumlah Order')
ax1.set_xlabel('Tanggal')
ax1.set_ylabel('Jumlah Order', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_title('Jumlah Order Harian dan Total Revenue')

ax2 = ax1.twinx()
ax2.plot(daily_orders_df['order_date'], daily_orders_df['revenue'], color='r', marker='o', label='Total Revenue')
ax2.set_ylabel('Total Revenue (USD)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

ax1.grid(axis='y', alpha=0.5)
fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.xticks(rotation=45)
st.pyplot(fig)

# Best Performing Products
st.write("## Best Performing Products")

# Get the best performing products
best_products = filtered_df.groupby(['product_id', 'product_category_name']).agg(
    purchase_count=('order_id', 'size')
).reset_index().sort_values(by='purchase_count', ascending=False).head(5)

# Plot for best performing products
plt.figure(figsize=(10, 6))
sns.barplot(
    data=best_products,
    x='purchase_count',
    y='product_id',
    hue='product_category_name',
    palette="muted"
)
plt.title('Best Performing Products')
plt.xlabel('Jumlah Pembelian')
plt.ylabel('Product ID')
plt.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# Worst Performing Products
st.write("## Worst Performing Products")

# Get the worst performing products
worst_products = filtered_df.groupby(['product_id', 'product_category_name']).agg(
    purchase_count=('order_id', 'size')
).reset_index().sort_values(by='purchase_count', ascending=True).head(5)

# Plot for worst performing products
plt.figure(figsize=(10, 6))
sns.barplot(
    data=worst_products,
    x='purchase_count',
    y='product_id',
    hue='product_category_name',
    palette="muted"
)
plt.title('Worst Performing Products')
plt.xlabel('Jumlah Pembelian')
plt.ylabel('Product ID')
plt.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# Best Performing Product Categories
st.write("## Best Performing Product Categories")

# Get the best performing categories
best_categories = filtered_df.groupby('product_category_name').agg(
    purchase_count=('order_id', 'size')
).reset_index().sort_values(by='purchase_count', ascending=False).head(5)
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# Plot for best performing categories
plt.figure(figsize=(10, 6))
sns.barplot(
    data=best_categories,
    x='purchase_count',
    y='product_category_name',
    palette=colors
)
plt.title('Best Performing Product Categories')
plt.xlabel('Jumlah Pembelian')
plt.ylabel('Kategori Produk')
plt.tight_layout()
st.pyplot(plt)

# Worst Performing Product Categories
st.write("## Worst Performing Product Categories")

# Get the worst performing categories
worst_categories = filtered_df.groupby('product_category_name').agg(
    purchase_count=('order_id', 'size')
).reset_index().sort_values(by='purchase_count', ascending=True).head(5)

# Plot for worst performing categories
plt.figure(figsize=(10, 6))
sns.barplot(
    data=worst_categories,
    x='purchase_count',
    y='product_category_name',
    palette=colors
)
plt.title('Worst Performing Product Categories')
plt.xlabel('Jumlah Pembelian')
plt.ylabel('Kategori Produk')
plt.tight_layout()
st.pyplot(plt)

# Highest Rated Products
st.write("## Highest Rated Products")

# Get the highest rated products using the filtered data
highest_rated = filtered_df.groupby(['product_id', 'product_category_name']).agg(
    average_rating=('review_score', 'mean')
).reset_index().sort_values(by='average_rating', ascending=False).head(5)

# Plot for highest rated products
plt.figure(figsize=(10, 6))
sns.barplot(
    data=highest_rated,
    x='average_rating',
    y='product_id',
    hue='product_category_name',
    palette="muted"
)
plt.title('Highest Rated Products')
plt.xlabel('Average Rating')
plt.ylabel('Product ID')
plt.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# Lowest Rated Products
st.write("## Lowest Rated Products")

# Get the lowest rated products using the filtered data
lowest_rated = filtered_df.groupby(['product_id', 'product_category_name']).agg(
    average_rating=('review_score', 'mean')
).reset_index().sort_values(by='average_rating', ascending=True).head(5)

# Plot for lowest rated products
plt.figure(figsize=(10, 6))
sns.barplot(
    data=lowest_rated,
    x='average_rating',
    y='product_id',
    hue='product_category_name',
    palette="muted"
)
plt.title('Lowest Rated Products')
plt.xlabel('Average Rating')
plt.ylabel('Product ID')
plt.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# Highest Rated Product Categories
st.write("## Highest Rated Product Categories")

# Get the highest rated product categories using the filtered data
average_category_rating = filtered_df.groupby(['product_category_name']).agg(
    average_rating=('review_score', 'mean')
).reset_index()

top_average_category_rating = average_category_rating.sort_values(by='average_rating', ascending=False).head(5)

# Plot for highest rated product category
plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_average_category_rating,
    x='average_rating',
    y='product_category_name',
    palette=colors
)
plt.title('Highest Rated Product Category')
plt.xlabel('Average Rating')
plt.ylabel('Product Category Name')
plt.tight_layout()
st.pyplot(plt)

# Lowesr Rated Product Categories
st.write("## Lowest Rated Product Categories")

# Get the lowest rated product categories using the filtered data
low_average_category_rating = average_category_rating.sort_values(by='average_rating', ascending=True).head(5)

# Plot for highest rated product category
plt.figure(figsize=(10, 6))
sns.barplot(
    data=low_average_category_rating,
    x='average_rating',
    y='product_category_name',
    palette=colors
)
plt.title('Highest Rated Product Category')
plt.xlabel('Average Rating')
plt.ylabel('Product Category Name')
plt.tight_layout()
st.pyplot(plt)

# Customer demographics
st.write("## Demografi Pelanggan")
customer_demographics = filtered_df.groupby("customer_state").customer_id.nunique().reset_index()
customer_demographics.rename(columns={"customer_id": "customer_count"}, inplace=True)

plt.figure(figsize=(10, 6))
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=customer_demographics.sort_values(by="customer_count", ascending=False).head(10),
    palette="viridis"
)
plt.title("Jumlah Pelanggan Berdasarkan Kota")
plt.xlabel(None)
plt.ylabel(None)
plt.tight_layout()
st.pyplot(plt)

## RFM Analysis
st.write("## RFM Analysis")
rfm_df = filtered_df.groupby(by="customer_id", as_index=False).agg({
    "order_approved_at": "max",
    "order_id": "nunique",
    "price": "sum"
})

rfm_df.columns = ["customer_id", "last_order_date", "frequency", "monetary"]
recent_date = filtered_df["order_approved_at"].max()
rfm_df["recency"] = (recent_date - rfm_df["last_order_date"]).dt.days

rfm_df.drop("last_order_date", axis=1, inplace=True)

# Calculate averages
average_recency = rfm_df["recency"].mean()
average_frequency = rfm_df["frequency"].mean()
average_monetary = rfm_df["monetary"].mean()

# Display the RFM DataFrame
st.write(rfm_df)

# Display RFM Summary Metrics
st.subheader("Best Customer Based on RFM Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Recency (days)", round(average_recency, 2))

with col2:
    st.metric("Average Frequency", round(average_frequency, 2))

with col3:
    total_average_monetary = format_currency(average_monetary, "AUD", locale='en_AU')
    st.metric("Average Monetary", total_average_monetary)

# Visualizing RFM in separate plots
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
# Recency Plot
plt.figure(figsize=(10, 6))
sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency").head(5), palette=colors)
plt.title("Top 5 Customers by Recency (days)")
plt.xticks(rotation=45)  # Rotate x labels for better visibility
st.pyplot(plt)

# Frequency Plot
plt.figure(figsize=(10, 6))
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors)
plt.title("Top 5 Customers by Frequency")
plt.xticks(rotation=45)  # Rotate x labels for better visibility
st.pyplot(plt)

# Monetary Plot
plt.figure(figsize=(10, 6))
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors)
plt.title("Top 5 Customers by Monetary Value")
plt.xticks(rotation=45)  # Rotate x labels for better visibility
st.pyplot(plt)


st.caption('Copyright (c) Insania Cindy 2024')
