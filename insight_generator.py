def generate_insights(question, df):

    first_col = df.columns[0]
    second_col = df.columns[1]

    top_item = df.iloc[0][first_col]
    top_value = df.iloc[0][second_col]

    bottom_item = df.iloc[-1][first_col]
    bottom_value = df.iloc[-1][second_col]
# --------------------------------------
# Top Performer Detection
# --------------------------------------

    top_performer = top_item
    top_performer_value = top_value

    lowest_performer = bottom_item
    lowest_performer_value = bottom_value

    average_value = df[second_col].mean()
    total_value = df[second_col].sum()

    # --------------------------------------
    # Performance Classification
    # --------------------------------------

    if top_value > average_value * 1.5:
        performance = "Strong"

    elif top_value > average_value:
        performance = "Moderate"

    else:
        performance = "Stable"


    # --------------------------------------
    # Concentration Risk
    # --------------------------------------

    share = (top_value / total_value) * 100
    # --------------------------------------
    # Trend Detection
    # --------------------------------------

    if top_value > average_value * 2:
        trend = "Increasing"

    elif top_value > average_value:
        trend = "Stable"

    else:
        trend = "Declining"

    if share > 50:
        concentration_risk = "High"

    elif share > 30:
        concentration_risk = "Medium"

    else:
        concentration_risk = "Low"
    
    # --------------------------------------
    # Anomaly Detection
    # --------------------------------------

    difference = top_value - average_value

    if difference > average_value:
        anomaly = "High deviation detected"

    elif difference > average_value * 0.5:
        anomaly = "Moderate deviation detected"

    else:
        anomaly = "No significant anomaly detected"
    # --------------------------------------
    # Opportunity Score
    # --------------------------------------

    if share < 20:
        opportunity_score = "High"

    elif share < 40:
        opportunity_score = "Medium"

    else:
        opportunity_score = "Low"

    insights = f"""
# Executive Summary

The analysis for:

**"{question}"**

shows that **{top_item}** is the leading performer with a value of **{top_value:,.2f}**, while **{bottom_item}** records the lowest value at **{bottom_value:,.2f}**.

The combined total across all records equals **{total_value:,.2f}**, with an average value of **{average_value:,.2f}**.

---

# Key Findings

• Top performer: **{top_item}**

• Lowest performer: **{bottom_item}**

• Average value: **{average_value:,.2f}**

• Total value across the dataset: **{total_value:,.2f}**

---

# Business Impact

Performance is concentrated among the leading entities.

Strong performers contribute disproportionately to overall results and therefore have a significant influence on business growth and profitability.

Lower-performing segments may require additional investigation and optimization.

---

# Risks

• Revenue concentration risk level: **{concentration_risk}**

• Heavy dependence on top-performing segments.

• Possible underutilization of low-performing areas.

• Uneven business performance may reduce long-term resilience.

---

# Opportunities

• Expand successful strategies used by **{top_performer}**.

• Improve weaker segments represented by **{lowest_performer}**.

• Allocate resources toward high-growth areas.

• Identify growth opportunities in mid-performing segments.

---

# Top Performer Analysis

🏆 Top Performer

**{top_performer}**

Value:

**{top_performer_value:,.2f}**

---

📉 Lowest Performer

**{lowest_performer}**

Value:

**{lowest_performer_value:,.2f}**

---

⭐ Contribution to Total

Top performer contributes approximately:

**{share:.2f}%**

of the total value.

---

# Trend Analysis

Current Trend:

### 📈 {trend}

---

# Anomaly Detection

### 🚨 {anomaly}

The leading entity differs from the average by:

**{difference:,.2f}**

---

# Opportunity Score

### 🎯 {opportunity_score}

This indicates the potential for future growth and optimization.

---
# Recommendations

1. Continue investing in top-performing segments.

2. Improve lower-performing entities.

3. Monitor anomalies and unusual deviations.

4. Track trends continuously.

5. Reallocate resources toward high-opportunity areas.

6. Diversify revenue sources to reduce concentration risk.
---

# Performance Assessment

Current business performance is classified as:

### **{performance}**

Top performer contributes approximately:

### **{share:.2f}%**

of the total value.
---

# Priority Actions

✓ Protect existing high-performing segments.

✓ Develop action plans for weaker segments.

✓ Track KPIs continuously.

✓ Allocate resources strategically.
"""

    return insights