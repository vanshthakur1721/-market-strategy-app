# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Market Strategy Analysis", layout="wide")
st.title("📊 Smart Tool for Market Strategy Analysis")

st.sidebar.header("Upload Datasets")
iphone_file = st.sidebar.file_uploader("Upload Apple Dataset (CSV)", type="csv")
samsung_file = st.sidebar.file_uploader("Upload Samsung Dataset (CSV)", type="csv")

if iphone_file:
    iphone_df = pd.read_csv(iphone_file)
else:
    st.sidebar.warning("Apple dataset not uploaded.")

if samsung_file:
    samsung_df = pd.read_csv(samsung_file)
else:
    st.sidebar.warning("Samsung dataset not uploaded.")

if iphone_file and samsung_file:
    # Preprocessing
    iphone_df["Ram"] = iphone_df["Ram"].str.replace(" GB", "").astype(int)
    iphone_df["Sale Price"] = iphone_df["Sale Price"].astype(float)
    iphone_df["Mrp"] = iphone_df["Mrp"].astype(float)
    iphone_df["Discount Percentage"] = iphone_df["Discount Percentage"].astype(float)
    if 'Brand' in iphone_df.columns:
        iphone_df.drop("Brand", axis=1, inplace=True)

    analysis = st.sidebar.selectbox("Select Analysis", [
        "📦 iPhone: Sale Price vs Rating",
        "📊 iPhone: RAM Preference",
        "💸 iPhone: Discount % vs Rating",
        "📶 Samsung: 5G Coverage by Region",
        "📈 Samsung: Year-wise Revenue"
    ])

    st.markdown("---")

    if analysis == "📦 iPhone: Sale Price vs Rating":
        st.subheader("Sale Price vs Star Rating (iPhone)")
        fig, ax = plt.subplots()
        sns.boxplot(x="Star Rating", y="Sale Price", data=iphone_df, ax=ax)
        st.pyplot(fig)

    elif analysis == "📊 iPhone: RAM Preference":
        st.subheader("RAM Preference Among iPhone Users")
        ram_percent = iphone_df['Ram'].value_counts(normalize=True) * 100
        fig, ax = plt.subplots()
        sns.barplot(x=ram_percent.index, y=ram_percent.values, palette='pastel', ax=ax)
        for i, p in enumerate(ram_percent.values):
            ax.text(i, p + 1, f'{p:.1f}%', ha='center', fontweight='bold')
        ax.set_ylabel("Percentage (%)")
        ax.set_xlabel("RAM (GB)")
        st.pyplot(fig)

    elif analysis == "💸 iPhone: Discount % vs Rating":
        st.subheader("Discount % vs User Rating (iPhone)")
        fig, ax = plt.subplots()
        sns.boxplot(x="Star Rating", y="Discount Percentage", data=iphone_df, ax=ax)
        st.pyplot(fig)

    elif analysis == "📶 Samsung: 5G Coverage by Region":
        st.subheader("Top 5 Regions by Avg 5G Coverage (Samsung)")
        top_regions = samsung_df.groupby('Region')['Regional 5G Coverage (%)'].mean().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots()
        ax.pie(top_regions, labels=top_regions.index, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)

    elif analysis == "📈 Samsung: Year-wise Revenue":
        st.subheader("Year-wise Avg Revenue (Samsung)")
        yearly_revenue = samsung_df.groupby('Year')['Revenue ($)'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.lineplot(data=yearly_revenue, x='Year', y='Revenue ($)', marker='o', ax=ax)
        st.pyplot(fig)
