# queries.py

queries = {
    "total_spent_per_category": """
        SELECT category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY category
        ORDER BY total_spent DESC;
    """,
    "total_spent_per_payment_mode": """
        SELECT payment_mode, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY payment_mode;
    """,
    "total_cashback_received": """
        SELECT SUM(cashback) AS total_cashback
        FROM expenses_data;
    """,
    "top_5_categories": """
        SELECT category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 5;
    """,
    "transportation_per_month_Using_diff_mode": """
        SELECT payment_mode, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category = 'Transportation'
        GROUP BY payment_mode;

    """,
    "cashback_transaction": """
        SELECT *
        FROM expenses_data
        WHERE cashback > 0;
    """,
    "spending_each_month": """
        SELECT MONTHNAME(date) AS month, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY MONTH(date)
        ORDER BY MONTH(date);
    """,
    "month_high_spend_specific_category": """
        SELECT MONTHNAME(date) AS month, category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category IN ('Travel', 'Entertainment', 'Gifts')
        GROUP BY MONTH(date), category
        ORDER BY total_spent DESC;
    """,
    "recurring_expense_specific_month": """
        SELECT MONTHNAME(date) AS month, category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category IN ('Insurance', 'Taxes')
        GROUP BY MONTH(date), category
        ORDER BY MONTH(date);
    """,
    "rewards_each_month": """
        SELECT MONTHNAME(date) AS month, SUM(cashback) AS total_cashback
        FROM expenses_data
        GROUP BY MONTH(date)
        ORDER BY MONTH(date);
    """,
    "spend_trend": """
        SELECT MONTHNAME(date) AS month, YEAR(date) AS year, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY YEAR(date), MONTH(date);
    """,
    "spend_associated_to_travel": """
        SELECT category, description, AVG(amount_paid) AS avg_spent
        FROM expenses_data
        WHERE category = 'Travel'
        GROUP BY description;
    """,
    "grocery_trend": """
        SELECT DAYNAME(date) AS day, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category = 'Groceries'
        GROUP BY DAY(date);   
    """,
    "high_low_priority_category": """
        SELECT category, SUM(amount_paid) AS total_spent,
               CASE 
                   WHEN SUM(amount_paid) > 10000 THEN 'High Priority'
                   ELSE 'Low Priority'
               END AS priority
        FROM expenses_data
        GROUP BY category;
    """,
    "max_spend_category":"""
        SELECT category, 
               SUM(amount_paid) AS total_spent,
               (SUM(amount_paid) / (SELECT SUM(amount_paid) FROM expenses_data)) * 100 AS percentage
        FROM expenses_data
        GROUP BY category
        ORDER BY percentage DESC
        LIMIT 1;
    """

}