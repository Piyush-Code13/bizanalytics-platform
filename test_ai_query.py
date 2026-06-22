from ai_query import ask_database

question = "Show top 10 product categories by revenue"

(
    sql_query,
    df,
    fig,
    summary,
    executive_summary
) = ask_database(question)

print("\nGenerated SQL:\n")
print(sql_query)

print("\nResults:\n")
print(df.head())

print("\nBusiness Analyst Insight:\n")
print(summary)

print("\nExecutive Summary:\n")
print(executive_summary)

fig.show()