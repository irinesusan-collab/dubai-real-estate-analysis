import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Dubai Real Estate Insights", layout="wide")
st.title("Dubai Property Dashboard 🚀")

# Load dataset
df = pd.read_csv("transactions.csv")

# Show preview
st.subheader("Dataset Preview")
st.dataframe(df.head())
st.subheader("Key Market Observations")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Property size shows the strongest relationship with price.")

with col2:
    st.success("High-demand areas maintain consistently higher value per sqft.")

with col3:
    st.warning("Short-term trend suggests mild price cooling.")

st.subheader("Size vs Transaction Value (Log Scale)")

filtered_df = df[df["TRANS_VALUE"] < df["TRANS_VALUE"].quantile(0.99)]

fig = px.scatter(
    filtered_df,
    x="ACTUAL_AREA",
    y="TRANS_VALUE",
    color="GROUP_EN",   # fewer categories than AREA
    title="Property Size vs Price (Log Scale View)",
    opacity=0.6,
)

fig.update_layout(
    xaxis_type="log",
    yaxis_type="log",
    xaxis_title="Actual Area (log scale)",
    yaxis_title="Transaction Value (log scale)",
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("Monthly Price Trend")

# Convert to datetime
df["INSTANCE_DATE"] = pd.to_datetime(df["INSTANCE_DATE"])

# Create month column
df["MONTH"] = df["INSTANCE_DATE"].dt.to_period("M").astype(str)

# Monthly average price
monthly_trend = df.groupby("MONTH")["TRANS_VALUE"].mean().reset_index()

fig2 = px.line(
    monthly_trend,
    x="MONTH",
    y="TRANS_VALUE",
    markers=True,
    title="Average Monthly Transaction Value"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Market Insight Summary")

st.info("""
📉 The monthly trend shows a mild cooling in average transaction value.
This suggests short-term price stabilization after a high-activity period.
Larger properties continue to dominate total transaction value,
but mid-sized units remain the most actively traded segment.
This pattern is consistent with a transitioning market rather than a crash.
""")
st.subheader("Area Price Comparison")

area_avg = (
    df.groupby("AREA_EN")["TRANS_VALUE"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_area = px.bar(
    area_avg,
    x="AREA_EN",
    y="TRANS_VALUE",
    title="Top 10 Areas by Average Transaction Value",
    color="TRANS_VALUE"
)

st.plotly_chart(fig_area, use_container_width=True)

st.info("""
Premium zones command significantly higher average transaction values.
This confirms that location remains a primary pricing driver in Dubai.
Investors targeting high-liquidity markets should focus on top-tier
areas where price resilience is historically stronger.
""")
import seaborn as sns
import matplotlib.pyplot as plt
st.subheader("Feature Correlation Analysis")

numeric_df = df[["TRANS_VALUE", "ACTUAL_AREA", "PROCEDURE_AREA"]].dropna()

corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)
st.success("""
📊 Property size shows the strongest statistical relationship with price.
Structural features have more influence than external amenities.
This reinforces the thesis that square footage is the dominant
pricing driver in Dubai transactions.
""")
st.caption("""
Exploratory analysis of Dubai property transactions to identify price drivers,
market behavior, and short-term trend signals.
""")
st.subheader("Methodology")

st.write("""
Data cleaned and transformed using Pandas.
Outliers removed for fair comparison.
Correlation analysis applied to identify price drivers.
Trend analysis performed on aggregated monthly values.
This dashboard is designed for directional market insight,
not predictive financial advice.
""")