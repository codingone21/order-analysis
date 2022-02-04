import mysql.connector
from mysql.connector import Error

""" HELPER FUNCTIONS - SQL DATABASE """
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        queryLog = query.replace('\n',"").split("(")[0]
        queryType = ' '.join(queryLog.split(" ")[:2])
        if queryType not in ("CREATE DATABASE"):
            connection.commit()
        print(f"Query '{queryLog}' successful")
    except Error as err:
        print(f"Error: '{err}'")
    
def drop_all_tables(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS sales, menu, members;")
        print("Query DROP TABLE successful")
    except Error as err:
        print(f"Error: '{err}'")
        
def cleanup_db(connection):
    cursor = connection.cursor()
    cursor.close()
    connection.close()

""" SETUP SQL DATABASE """

# Setting up SQL Database
DATBASE_PASSWORD = "abcdefg"  
DATABASE_NAME = "van_deli"    

connection = create_db_connection("localhost", "root", DATBASE_PASSWORD, DATABASE_NAME) # Connect to the Database
if not connection: # This is needed for initial connection to the DB
    print(f"Connection was not established. Creating a new server connection wit DB '{DATABASE_NAME}'")
    connection = create_server_connection("localhost", "root", DATBASE_PASSWORD)
    create_database_query = "CREATE DATABASE van_deli"
    create_database(connection, create_database_query)

# Creating tables
# First, drop all tables
drop_all_tables(connection)

create_table_sales = """
CREATE TABLE sales (
    customer_id VARCHAR(10)         NOT NULL,
    order_date  DATE,
    product_id  INT                 NOT NULL
    );
"""
create_table_menu = """
CREATE TABLE menu (
    product_id      INT             PRIMARY KEY,
    product_name    VARCHAR(10),
    price           DECIMAL(10,2)   NOT NULL
    );
"""
create_table_members = """
CREATE TABLE members (
    customer_id     VARCHAR(10)     PRIMARY KEY,
    customer_name   VARCHAR(10)     NOT NULL,
    join_date       DATE
    );
"""

execute_query(connection, create_table_sales)
execute_query(connection, create_table_menu)
execute_query(connection, create_table_members)

populate_sales = """
INSERT INTO sales VALUES
('A', '2021-01-01', 1),
('A', '2021-01-01', 2),
('A', '2021-01-07', 2),
('A', '2021-01-10', 3),
('A', '2021-01-11', 3),
('A', '2021-01-11', 3),
('B', '2021-01-01', 2),
('B', '2021-01-02', 2),
('B', '2021-01-04', 1),
('B', '2021-01-11', 1),
('B', '2021-01-16', 3),
('B', '2021-02-01', 3),
('C', '2021-01-01', 3),
('C', '2021-01-01', 3),
('C', '2021-01-07', 3);
"""

populate_menu = """
INSERT IGNORE INTO menu VALUES
(1, 'sushi', 10),
(2, 'curry', 15),
(3, 'ramen', 12);

"""
populate_members = """
INSERT IGNORE INTO members VALUES
('A', 'Anne', '2021-01-07'),
('B', 'Bob' , '2021-01-09');
"""

execute_query(connection, populate_sales)
execute_query(connection, populate_menu)
execute_query(connection, populate_members)

"""  Q1 - MOST PURCHASED """
q1_most_purchased = """
CREATE TABLE IF NOT EXISTS q1 
    (SELECT s.product_id, product_name, COUNT(s.product_id) num_purchase
    FROM sales s LEFT JOIN menu m ON s.product_id = m.product_id
    GROUP BY s.product_id
    ORDER BY num_purchase DESC
    LIMIT 1);
"""

execute_query(connection, q1_most_purchased)

"""  Q2 - SALES VIEW """
q2_sales_view = """
CREATE TABLE IF NOT EXISTS q2
    (SELECT 
    	sales.customer_id, sales.order_date, menu.product_name, menu.price,
    	(CASE WHEN (members.join_date IS NULL OR members.join_date > sales.order_date) THEN 'N' ELSE 'Y' END) AS is_member,
    	DENSE_RANK() OVER (partition by sales.customer_id ORDER BY sales.order_date ASC) AS ranking
    FROM sales LEFT JOIN menu ON sales.product_id = menu.product_id 
    LEFT JOIN members ON sales.customer_id = members.customer_id
    ORDER BY customer_id ASC, order_date ASC);
"""

execute_query(connection, q2_sales_view)


