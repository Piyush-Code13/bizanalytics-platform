import streamlit as st
from ai_query import ask_database

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Business Analytics Platform",
    layout="wide"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Menu",
    [
        "Home",
        "AI Chat",
        "Dashboard",
        "KPI Analysis",
        "Reports"
    ]
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🤖 AI Business Analytics Platform")
# ==================================================
# HEADER
# ==================================================

st.markdown(
"""
### Ask business questions in natural language

Examples:

- Show top 10 product categories by revenue
- Which states have the highest revenue?
- Which categories have the most orders?
- Show average review score by category
- Which sellers generate the highest revenue?

---
"""
)

st.markdown(
"""
Ask questions in natural language and receive:

- SQL queries
- Query results
- Interactive charts
- AI-generated business insights
"""
)
# ==================================================
# SESSION HISTORY
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# QUESTION INPUT
# ---------------------------------------------------

question = st.text_input(
    "Ask your business question",
    placeholder="Example: Show top 10 product categories by revenue"
)

# ---------------------------------------------------
# PROCESS QUERY
# ---------------------------------------------------

if question:

    try:

        with st.spinner("Analyzing business question..."):

            sql_query, df, fig, insights = ask_database(question)
        # Store question history

        st.session_state.history.append(question)
        st.session_state.chat_history.append(
    {
        "question": question,
        "sql": sql_query
    }
)

        # ---------------------------------------------
        # KPI CARDS
        # ---------------------------------------------

        st.markdown("---")
        st.subheader("📊 Business KPIs")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Records",
                len(df)
            )

        with col2:
            st.metric(
                "Columns",
                len(df.columns)
            )

        with col3:
            if len(df.columns) > 1:
                try:
                    st.metric(
                        "Maximum Value",
                        f"{df.iloc[:,1].max():,.2f}"
                    )
                except:
                    st.metric(
                        "Maximum Value",
                        "-"
                    )

        with col4:
            if len(df.columns) > 1:
                try:
                    st.metric(
                        "Average Value",
                        f"{df.iloc[:,1].mean():,.2f}"
                    )
                except:
                    st.metric(
                        "Average Value",
                        "-"
                    )

        # ---------------------------------------------
        # SQL
        # ---------------------------------------------
                # ---------------------------------------------
        # TABS
        # ---------------------------------------------

        tab1, tab2, tab3 = st.tabs(
            ["🛠 SQL", "📋 Results", "📈 Visualization"]
        )

        # ---------------- SQL ----------------

        with tab1:

            st.code(
                sql_query,
                language="sql"
            )

        # ---------------- Results ----------------

        with tab2:

            st.dataframe(
                df,
                use_container_width=True
            )

        # ---------------- Chart ----------------

        with tab3:

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ---------------------------------------------
        # AI INSIGHTS
        # ---------------------------------------------

        st.markdown("---")

        st.subheader("🧠 AI Business Insights")

        st.markdown(insights)
        

    except Exception as e:

        if "429" in str(e):

            st.error(
                "⚠ Gemini API quota exceeded.\n\nPlease wait a while and try again."
            )

        else:

            st.exception(e)
# ==================================================
# FOOTER
# ==================================================

st.sidebar.subheader("Conversation Memory")

for item in reversed(st.session_state.chat_history[-5:]):

    st.sidebar.markdown(
        f"**Q:** {item['question']}"
    )

st.caption(
    "AI Business Analytics Platform | Built with Python, BigQuery, Gemini and Streamlit"
)
