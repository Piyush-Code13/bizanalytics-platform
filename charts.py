
import plotly.express as px
import streamlit as st
# ==================================================
# Total Revenue
# ==================================================
def revenue_chart(df):

    total_revenue = df["f0_"].iloc[0]

    fig = px.bar(
        x=["Revenue"],
        y=[total_revenue],
        text=[f"${total_revenue:,.0f}"],
        title="💰 Total Revenue"
    )

    fig.update_traces(
        marker_color="#2E86DE",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.35,
        xaxis_title="",
        yaxis_title="Revenue",
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# Top Product Categories
# ==================================================
def product_category_chart(df):

    fig = px.bar(
        df,
        x="total_sales",
        y="product_category_name_english",
        orientation="h",
        color="total_sales",
        color_continuous_scale="Blues",
        text="total_sales",
        title="🏆 Top 10 Product Categories"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.30,
        xaxis_title="Number of Sales",
        yaxis_title="Category",
        coloraxis_showscale=False,
        height=600
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# Monthly Revenue Trend
# ==================================================
def monthly_revenue_chart(df):

    fig = px.line(
        df,
        x="month",
        y="revenue",
        markers=True,
        title="📈 Monthly Revenue Trend"
    )

    fig.update_traces(
        line_color="#1ABC9C",
        line_width=4,
        marker_size=8
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.35,
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode="x unified",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# Orders by Status
# ==================================================
def orders_status_chart(df):

    fig = px.pie(
        df,
        names="order_status",
        values="num_orders",
        hole=0.45,
        title="📦 Orders by Status"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.35,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

