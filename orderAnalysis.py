from databaseSetup import execute_query, connection

""" MOST PURCHASED """
q1_most_purchased = """
SELECT s.product_id, product_name, COUNT(s.product_id) num_purchase
FROM sales s LEFT JOIN menu m ON s.product_id = m.product_id
GROUP BY s.product_id
ORDER BY num_purchase DESC
LIMIT 1;
"""

execute_query(connection, q1_most_purchased)

q2_sales_view = """
SELECT 
	sales.customer_id, sales.order_date, menu.product_name, menu.price,
	(CASE WHEN (members.join_date IS NULL OR members.join_date > sales.order_date) THEN 'N' ELSE 'Y' END) AS is_member,
	DENSE_RANK() OVER (partition by sales.customer_id ORDER BY sales.order_date ASC) AS ranking
FROM sales LEFT JOIN menu ON sales.product_id = menu.product_id 
LEFT JOIN members ON sales.customer_id = members.customer_id
ORDER BY customer_id ASC, order_date ASC;
"""

execute_query(connection, q2_sales_view)