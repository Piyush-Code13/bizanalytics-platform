from text_to_sql import generate_sql
from bigquery_helper import run_query
from chart_generator import generate_chart
from insight_generator import generate_insights


def ask_database(question):

    sql_query = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql_query)

    df = run_query(sql_query)

    fig = generate_chart(df,question)

    insights = generate_insights(
    question,
    df
)

    return (
    sql_query,
    df,
    fig,
    insights
)