USE van_deli;

SELECT * FROM van_deli.sales ORDER BY customer_id;
SELECT * FROM van_deli.menu;
SELECT * FROM van_deli.members;

-- QUESTION 1
SELECT s.product_id, product_name, COUNT(s.product_id) num_purchase
FROM sales s LEFT JOIN menu m ON s.product_id = m.product_id
GROUP BY s.product_id
ORDER BY num_purchase DESC
LIMIT 1;

-- QUESTION 2
DROP TABLE sales_expanded;
CREATE TABLE sales_expanded
SELECT 
	sales.customer_id, sales.order_date, menu.product_name, menu.price,
	(CASE WHEN (members.join_date IS NULL OR members.join_date > sales.order_date) THEN 'N' ELSE 'Y' END) AS is_member,
	DENSE_RANK() OVER (partition by sales.customer_id ORDER BY sales.order_date ASC) AS ranking
FROM sales LEFT JOIN menu ON sales.product_id = menu.product_id 
LEFT JOIN members ON sales.customer_id = members.customer_id
ORDER BY customer_id ASC, order_date ASC
;
TABLE sales_expanded;

-- ANSWER
DROP TABLE solution;
CREATE TABLE IF NOT EXISTS solution (
customer_id VARCHAR(10),
order_date DATE,
product_name VARCHAR(10),
price DECIMAL(10, 2),
member CHAR(1),
ranking INT
);
INSERT INTO solution VALUES
('A', 	'2021-01-01', 	'curry', 	15, 	'N', 	1),
('A', 	'2021-01-01', 	'sushi', 	10, 	'N', 	1),
('A', 	'2021-01-07', 	'curry', 	15, 	'Y', 	2),
('A', 	'2021-01-10', 	'ramen', 	12, 	'Y', 	3),
('A', 	'2021-01-11', 	'ramen', 	12, 	'Y', 	4),
('A', 	'2021-01-11', 	'ramen', 	12, 	'Y', 	4),
('B', 	'2021-01-01', 	'curry', 	15, 	'N', 	1),
('B', 	'2021-01-02', 	'curry', 	15, 	'N', 	2),
('B', 	'2021-01-04', 	'sushi', 	10, 	'N', 	3),
('B', 	'2021-01-11', 	'sushi',	10, 	'Y', 	4), 
('B', 	'2021-01-16', 	'ramen',	12,		'Y',	5),
('B',	'2021-02-01',	'ramen',	12,		'Y',	6),
('C',	'2021-01-01',	'ramen',	12, 	'N', 	1),
('C', 	'2021-01-01', 	'ramen', 	12, 	'N', 	1),
('C', 	'2021-01-07', 	'ramen', 	12,		'N', 	2);

-- COMPARE ANSER TO SOLUTION
SELECT * from solution
ORDER BY customer_id, order_date, product_name;