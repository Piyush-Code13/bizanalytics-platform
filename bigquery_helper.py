from config import client


def run_query(sql_query):
    """
    Execute SQL query on BigQuery and return a dataframe.
    """

    query_job = client.query(sql_query)

    df = query_job.to_dataframe()

    return df