import plotly.express as px


def generate_chart(df, question):

    question = question.lower()

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(exclude="number").columns

    if len(numeric_cols) == 0:
        return None

    # ==========================================
    # Revenue trend / monthly trend
    # ==========================================
    if (
        "month" in question
        or "trend" in question
        or "time" in question
    ):

        if len(df.columns) >= 2:

            fig = px.line(
                df,
                x=df.columns[0],
                y=numeric_cols[0],
                markers=True,
                title="Trend Analysis"
            )

            fig.update_layout(
                template="plotly_white",
                title_x=0.35
            )

            return fig

    # ==========================================
    # Distribution / share
    # ==========================================
    if (
        "share" in question
        or "distribution" in question
        or "status" in question
    ):

        if len(categorical_cols) >= 1:

            fig = px.pie(
                df.head(10),
                names=categorical_cols[0],
                values=numeric_cols[0],
                hole=0.45,
                title="Distribution"
            )

            fig.update_layout(
                template="plotly_white",
                title_x=0.35
            )

            return fig

    # ==========================================
    # Correlation
    # ==========================================
    if (
        "relationship" in question
        or "correlation" in question
    ):

        if len(numeric_cols) >= 2:

            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title="Correlation Analysis"
            )

            fig.update_layout(
                template="plotly_white",
                title_x=0.35
            )

            return fig

    # ==========================================
    # Default horizontal bar
    # ==========================================

    if len(categorical_cols) >= 1:

        fig = px.bar(
            df.head(10),
            x=numeric_cols[0],
            y=categorical_cols[0],
            orientation="h",
            color=numeric_cols[0],
            color_continuous_scale="Blues",
            text=numeric_cols[0]
        )

        fig.update_layout(
            template="plotly_white",
            title_x=0.35,
            coloraxis_showscale=False,
            height=600
        )

        fig.update_traces(
            textposition="outside"
        )

        return fig

    return None

