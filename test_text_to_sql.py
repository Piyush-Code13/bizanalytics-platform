from text_to_sql import generate_sql

question = "Top 10 product categories by revenue"

sql_query = generate_sql(question)

print(sql_query)