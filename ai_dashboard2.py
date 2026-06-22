"""
AI-Powered Business Analytics Platform
----------------------------------------
A conversational BI interface — ask questions in plain English,
get back SQL, live BigQuery results, charts, and AI analyst insights.

Design note: styled as a dark analyst terminal rather than a default
Streamlit theme — built to look credible in a recruiter screen-share.
"""

import time
from datetime import datetime

import streamlit as st
from ai_query import ask_database


# =====================================================================
# PAGE CONFIG
# =====================================================================

st.set_page_config(
    page_title="BizAnalytics AI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================================
# THEME — dark analyst-terminal aesthetic
# =====================================================================
# Palette:
#   --bg        #0B0F14   near-black charcoal, not pure black
#   --surface   #11161D   card background
#   --surface2  #161D27   raised card / hover
#   --border    #232B36   hairline borders
#   --signal    #34F5C5   electric mint — the one accent, used sparingly
#   --signal-dim#0E3A33   signal at low opacity for fills
#   --text      #E8ECEF   primary text
#   --text-dim  #7C8896   secondary / caption text
#   --warn      #F5A623   amber for cautions
#   --error     #FF5C5C   soft red for errors
#
# Type:
#   Display / labels : "Space Grotesk" (loaded via Google Fonts)
#   Data / code       : "JetBrains Mono"
#   Body              : system sans fallback (Streamlit default is fine
#                        once color + spacing are corrected)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #0B0F14;
    --surface: #11161D;
    --surface2: #161D27;
    --border: #232B36;
    --signal: #34F5C5;
    --signal-dim: rgba(52, 245, 197, 0.10);
    --signal-border: rgba(52, 245, 197, 0.35);
    --text: #E8ECEF;
    --text-dim: #7C8896;
    --warn: #F5A623;
    --warn-dim: rgba(245, 166, 35, 0.10);
    --error: #FF5C5C;
    --error-dim: rgba(255, 92, 92, 0.10);
}

/* ---------- base canvas ---------- */
.stApp {
    background: var(--bg);
}
html, body, [class*="css"] {
    font-family: 'Space Grotesk', -apple-system, sans-serif;
}

/* ---------- kill default streamlit chrome ---------- */
#MainMenu, header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px; }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.4rem; }

/* ---------- top masthead ---------- */
.masthead {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 18px;
    margin-bottom: 22px;
    border-bottom: 1px solid var(--border);
}
.masthead-left { display: flex; align-items: center; gap: 12px; }
.masthead-mark {
    width: 34px; height: 34px;
    border: 1.5px solid var(--signal-border);
    background: var(--signal-dim);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px; font-weight: 600; color: var(--signal);
}
.masthead-title {
    font-size: 17px; font-weight: 600; color: var(--text);
    letter-spacing: -0.01em; line-height: 1.1;
}
.masthead-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px; color: var(--text-dim);
    letter-spacing: 0.04em; margin-top: 1px;
}
.status-pill {
    display: flex; align-items: center; gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: var(--text-dim);
    border: 1px solid var(--border);
    padding: 5px 12px; border-radius: 20px;
    background: var(--surface2);
}
.status-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--signal);
    box-shadow: 0 0 6px var(--signal);
}

/* ---------- capability strip ---------- */
.capability-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 26px;
}
.cap-item {
    background: var(--surface);
    padding: 14px 16px;
}
.cap-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: var(--signal);
    letter-spacing: 0.05em; margin-bottom: 4px;
}
.cap-label { font-size: 12.5px; color: var(--text); font-weight: 500; }

/* ---------- question input row ---------- */
div[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 14.5px !important;
    padding: 13px 16px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--signal-border) !important;
    box-shadow: 0 0 0 3px var(--signal-dim) !important;
}
div[data-testid="stTextInput"] input::placeholder { color: var(--text-dim) !important; }
div[data-testid="stTextInput"] label { color: var(--text-dim) !important; font-size: 12.5px !important; }

/* ---------- buttons ---------- */
.stButton button {
    background: var(--signal) !important;
    color: #07120F !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0.6rem 1.2rem !important;
    transition: filter 0.15s !important;
}
.stButton button:hover { filter: brightness(1.08); }
.stButton button:active { filter: brightness(0.92); }

/* secondary (sidebar sample question) buttons */
section[data-testid="stSidebar"] .stButton button {
    background: var(--surface2) !important;
    color: var(--text-dim) !important;
    border: 1px solid var(--border) !important;
    font-weight: 400 !important;
    font-size: 12px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.5rem 0.7rem !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    border-color: var(--signal-border) !important;
    color: var(--text) !important;
}

/* ---------- section labels ---------- */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin: 22px 0 10px 0;
    display: flex; align-items: center; gap: 8px;
}
.sec-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.sec-label.signal { color: var(--signal); }

/* ---------- KPI cards ---------- */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--text-dim); margin-bottom: 6px;
}
.kpi-value { font-size: 22px; font-weight: 600; color: var(--text); font-family: 'JetBrains Mono', monospace; }

/* ---------- SQL code block wrapper ---------- */
.sql-wrap {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 4px;
}
.sql-header {
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    padding: 7px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    color: var(--text-dim);
    display: flex; justify-content: space-between;
}
div[data-testid="stCodeBlock"] pre {
    background: var(--surface) !important;
    border-radius: 0 !important;
}

/* ---------- dataframe ---------- */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ---------- AI insight / analyst card ---------- */
.analyst-card {
    background: linear-gradient(180deg, var(--signal-dim), transparent 60%);
    border: 1px solid var(--signal-border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-top: 4px;
}
.analyst-card-header {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 10px;
}
.analyst-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.06em;
    color: #07120F; background: var(--signal);
    padding: 3px 8px; border-radius: 5px; font-weight: 600;
}
.analyst-card-title { font-size: 13px; color: var(--text); font-weight: 600; }
.analyst-body { color: var(--text); font-size: 14px; line-height: 1.65; }
.analyst-body p { margin: 0 0 8px 0; }

/* ---------- history items ---------- */
.history-item {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    color: var(--text-dim);
    padding: 7px 0;
    border-bottom: 1px solid var(--border);
    cursor: default;
}
.history-item:last-child { border-bottom: none; }
.history-time { color: #4A5563; font-size: 10px; }

/* ---------- empty state ---------- */
.empty-state {
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 48px 24px;
    text-align: center;
    margin-top: 8px;
}
.empty-state-icon {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px; color: var(--text-dim); margin-bottom: 10px;
}
.empty-state-title { font-size: 15px; color: var(--text); font-weight: 500; margin-bottom: 6px; }
.empty-state-sub { font-size: 12.5px; color: var(--text-dim); max-width: 420px; margin: 0 auto; }

/* ---------- error / quota banners ---------- */
.banner {
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    border: 1px solid;
    margin-bottom: 12px;
    line-height: 1.6;
}
.banner.warn { background: var(--warn-dim); border-color: rgba(245,166,35,0.35); color: #F5C77E; }
.banner.error { background: var(--error-dim); border-color: rgba(255,92,92,0.35); color: #FF9A9A; }
.banner b { color: var(--text); }

/* ---------- footer ---------- */
.app-footer {
    margin-top: 40px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 8px;
}
.app-footer-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px; color: var(--text-dim); letter-spacing: 0.02em;
}
.stack-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: var(--text-dim);
    border: 1px solid var(--border);
    padding: 2px 8px; border-radius: 5px;
    margin-left: 4px;
}

/* ---------- misc text colors override ---------- */
h1, h2, h3, p, label, .stMarkdown { color: var(--text); }
hr { border-color: var(--border) !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =====================================================================
# SESSION STATE
# =====================================================================

if "history" not in st.session_state:
    st.session_state.history = []  # list of (question, timestamp)

if "query_count" not in st.session_state:
    st.session_state.query_count = 0


# =====================================================================
# SIDEBAR — navigation + live session info
# =====================================================================

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:28px;height:28px;border:1.5px solid var(--signal-border);
                        background:var(--signal-dim);border-radius:6px;display:flex;
                        align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;
                        font-size:13px;color:var(--signal);font-weight:600;">◆</div>
            <div style="font-size:14px;font-weight:600;color:var(--text);">BizAnalytics AI</div>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-dim);
                    letter-spacing:0.05em;margin-bottom:18px;">v1.0 · OLIST E-COMMERCE</div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        ["Home", "AI Chat", "Dashboard", "KPI Analysis", "Reports"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sec-label">Session</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:11.5px;color:var(--text-dim);
                    display:flex;justify-content:space-between;padding:3px 0;">
            <span>Queries run</span><span style="color:var(--text)">{st.session_state.query_count}</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:11.5px;color:var(--text-dim);
                    display:flex;justify-content:space-between;padding:3px 0;">
            <span>Connected DB</span><span style="color:var(--signal)">BigQuery</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:11.5px;color:var(--text-dim);
                    display:flex;justify-content:space-between;padding:3px 0;">
            <span>Model</span><span style="color:var(--text)">Gemini 1.5</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec-label">Try asking</div>', unsafe_allow_html=True)
    sample_questions = [
        "Top 10 categories by revenue",
        "Revenue trend by month, 2017–2018",
        "Average delivery time by state",
        "Which states have the lowest review scores?",
    ]
    for sq in sample_questions:
        if st.button(sq, key=f"sample_{sq}", use_container_width=True):
            st.session_state["pending_question"] = sq

    if st.session_state.history:
        st.markdown('<div class="sec-label">Recent questions</div>', unsafe_allow_html=True)
        history_html = ""
        for q, ts in reversed(st.session_state.history[-5:]):
            history_html += (
                f'<div class="history-item">{q}'
                f'<div class="history-time">{ts}</div></div>'
            )
        st.markdown(history_html, unsafe_allow_html=True)


# =====================================================================
# MASTHEAD
# =====================================================================

st.markdown(
    """
    <div class="masthead">
        <div class="masthead-left">
            <div class="masthead-mark">◆</div>
            <div>
                <div class="masthead-title">AI-Powered Business Analytics Platform</div>
                <div class="masthead-sub">NATURAL LANGUAGE → SQL → INSIGHT</div>
            </div>
        </div>
        <div class="status-pill"><div class="status-dot"></div>LIVE · BIGQUERY CONNECTED</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================================
# HOME / default landing — capability strip
# =====================================================================

if page == "Home" or page == "AI Chat":
    st.markdown(
        """
        <div class="capability-strip">
            <div class="cap-item"><div class="cap-num">01 · SQL</div><div class="cap-label">Auto-generated queries</div></div>
            <div class="cap-item"><div class="cap-num">02 · DATA</div><div class="cap-label">Live BigQuery results</div></div>
            <div class="cap-item"><div class="cap-num">03 · VISUAL</div><div class="cap-label">Interactive charts</div></div>
            <div class="cap-item"><div class="cap-num">04 · INSIGHT</div><div class="cap-label">AI analyst summary</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- question input ----------------
    default_q = st.session_state.pop("pending_question", "")
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        question = st.text_input(
            "Ask a business question",
            value=default_q,
            placeholder="e.g. Show top 10 product categories by revenue",
            label_visibility="collapsed",
        )
    with col_btn:
        run_clicked = st.button("Run query →", use_container_width=True)

    should_run = bool(question) and (run_clicked or default_q)

    # ---------------- process query ----------------
    if should_run:
        st.session_state.query_count += 1
        st.session_state.history.append((question, datetime.now().strftime("%H:%M:%S")))

        with st.spinner("Generating SQL and querying BigQuery…"):
            try:
                sql_query, df, fig, insights = ask_database(question)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str:
                    st.markdown(
                        """
                        <div class="banner warn">
                            <b>⚠ Gemini API quota exceeded.</b><br>
                            The free tier rate limit was hit. Wait about a minute before
                            running another query, or reduce request frequency.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="banner error">
                            <b>Query failed.</b><br>
                            {err_str}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                df = None

            else:
                # ---------------- KPI row ----------------
                st.markdown('<div class="sec-label signal">Result Summary</div>', unsafe_allow_html=True)

                total_records = len(df)
                total_cols = len(df.columns)
                max_val = "—"
                avg_val = "—"
                if len(df.columns) > 1:
                    try:
                        max_val = f"{df.iloc[:, 1].max():,.2f}"
                    except Exception:
                        pass
                    try:
                        avg_val = f"{df.iloc[:, 1].mean():,.2f}"
                    except Exception:
                        pass

                st.markdown(
                    f"""
                    <div class="kpi-row">
                        <div class="kpi-card"><div class="kpi-label">Records</div><div class="kpi-value">{total_records}</div></div>
                        <div class="kpi-card"><div class="kpi-label">Columns</div><div class="kpi-value">{total_cols}</div></div>
                        <div class="kpi-card"><div class="kpi-label">Max value</div><div class="kpi-value">{max_val}</div></div>
                        <div class="kpi-card"><div class="kpi-label">Avg value</div><div class="kpi-value">{avg_val}</div></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ---------------- generated SQL ----------------
                st.markdown('<div class="sec-label">Generated SQL</div>', unsafe_allow_html=True)
                st.code(sql_query, language="sql")

                # ---------------- results + viz side by side ----------------
                res_col, viz_col = st.columns([1, 1.3])
                with res_col:
                    st.markdown('<div class="sec-label">Results</div>', unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True, height=320)
                with viz_col:
                    st.markdown('<div class="sec-label">Visualization</div>', unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=True)

                # ---------------- AI analyst insight ----------------
                st.markdown(
                    f"""
                    <div class="analyst-card">
                        <div class="analyst-card-header">
                            <span class="analyst-badge">AI ANALYST</span>
                            <span class="analyst-card-title">Business interpretation of this result</span>
                        </div>
                        <div class="analyst-body">{insights}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:
        # ---------------- empty state ----------------
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">◆</div>
                <div class="empty-state-title">Ask your first question</div>
                <div class="empty-state-sub">
                    Try a question from the sidebar, or type your own — e.g.
                    "What was total revenue in November 2017?"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif page == "Dashboard":
    st.markdown('<div class="sec-label signal">Dashboard</div>', unsafe_allow_html=True)
    st.info("Embed your Looker Studio dashboard here — e.g. via `st.components.v1.iframe(LOOKER_URL, height=800)`.")

elif page == "KPI Analysis":
    st.markdown('<div class="sec-label signal">KPI Analysis</div>', unsafe_allow_html=True)
    st.info("Plug in your dedicated KPI breakdown view here.")

elif page == "Reports":
    st.markdown('<div class="sec-label signal">Reports</div>', unsafe_allow_html=True)
    st.info("Hook up your Executive_Summary.pdf generator here.")


# =====================================================================
# FOOTER
# =====================================================================

st.markdown(
    """
    <div class="app-footer">
        <div class="app-footer-text">AI-Powered Business Analytics Platform · Built end-to-end with</div>
        <div>
            <span class="stack-pill">Python</span>
            <span class="stack-pill">BigQuery</span>
            <span class="stack-pill">dbt</span>
            <span class="stack-pill">Gemini</span>
            <span class="stack-pill">Streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)