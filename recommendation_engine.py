import pandas as pd
def top_categories(category_df, n=5):
    """Top N categories by revenue."""
    return category_df.nlargest(n, 'revenue')
def declining_categories(current_df, previous_df):
    """Categories whose revenue dropped period-over-period."""
    merged = current_df.merge(previous_df, on='category',
    suffixes=('_curr', '_prev'))
    merged['pct_change'] = (
    (merged['revenue_curr'] - merged['revenue_prev'])
    / merged['revenue_prev']
    )
    return merged[merged['pct_change'] < 0].sort_values('pct_change')
def best_states(state_df, n=5):
    """Top N states by revenue."""
    return state_df.nlargest(n, 'revenue')
def worst_states(state_df, n=5):
    """Bottom N states by revenue — improvement targets."""
    return state_df.nsmallest(n, 'revenue')
