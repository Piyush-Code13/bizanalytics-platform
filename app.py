import streamlit as st
from bigquery_helper import run_query
from ai_insights import generate_insight
from charts import (
    revenue_chart,
    product_category_chart,
    monthly_revenue_chart,
    orders_status_chart
)

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="AI Business Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# Title
# -----------------------
st.title("📊 AI-Powered Business Analytics Platform")

st.markdown("---")

# -----------------------
# KPIs
# -----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Revenue",
        "13.59 M",
        "From BigQuery"
    )

with col2:
    st.metric(
        "📦 Orders",
        "99,441",
        "Delivered Orders"
    )

with col3:
    st.metric(
        "🏆 Categories",
        "71",
        "Product Categories"
    )

st.markdown("---")

# ===============================
# Total Revenue
# ===============================
st.header("💰 Total Revenue")

query = """
SELECT
ROUND(SUM(payment_value),2) AS f0_
FROM ecommerce_raw.order_payments
"""

df = run_query(query)

revenue_chart(df)

st.markdown("---")

# ===============================
# Top Product Categories
# ===============================
st.header("🏆 Top Product Categories")

query = """
SELECT
    t.product_category_name_english,
    COUNT(*) AS total_sales
FROM ecommerce_raw.orders o
JOIN ecommerce_raw.order_items oi
ON o.order_id = oi.order_id

JOIN ecommerce_raw.products p
ON oi.product_id = p.product_id

JOIN ecommerce_raw.product_category_name_translation t
ON p.product_category_name = t.product_category_name

GROUP BY t.product_category_name_english
ORDER BY total_sales DESC
LIMIT 10
"""
df = run_query(query)

product_category_chart(df)

st.markdown("---")

# ===============================
# Monthly Revenue Trend
# ===============================
st.header("📈 Monthly Revenue Trend")

query = """
SELECT
FORMAT_DATE('%Y-%m', DATE(order_purchase_timestamp)) AS month,
ROUND(SUM(payment_value),2) AS revenue
FROM ecommerce_raw.orders o
JOIN ecommerce_raw.order_payments p
ON o.order_id = p.order_id
WHERE order_status NOT IN ('canceled','unavailable')
AND DATE(order_purchase_timestamp) < '2018-09-01'
GROUP BY month
ORDER BY month
"""
df = run_query(query)

monthly_revenue_chart(df)

st.markdown("---")

# ===============================
# Orders by Status
# ===============================
st.header("📦 Orders by Status")

query = """
SELECT
order_status,
COUNT(*) AS num_orders
FROM ecommerce_raw.orders
GROUP BY order_status
ORDER BY num_orders DESC
"""

df = run_query(query)

orders_status_chart(df)

st.markdown("---")

st.header("🤖 AI Business Insights")

insight = generate_insight(
    "Total Revenue",
    "13.59 Million"
)

st.write(insight)

st.markdown("---")

st.header("💬 Ask AI Business Analyst")

question = st.text_input(
    "Ask a business question"
)

if question:

    answer = generate_insight(question, "")

    st.write(answer)