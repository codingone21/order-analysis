from flask import Flask, render_template
from flask_mysqldb import MySQL
from setupDatabase import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, create_db_connection
from setupDatabase import create_and_populate_tables, create_solution_views
import pandas as pd

# MySQL configurations
app = Flask(__name__)
app.config['MYSQL_HOST'] = DATABASE_HOST
app.config['MYSQL_USER'] = DATABASE_USER
app.config['MYSQL_PASSWORD'] = DATABASE_PASSWORD
app.config['MYSQL_DB'] = DATABASE_NAME
mysql = MySQL(app)  

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/tables")
def tables():
    connection = create_db_connection()
    q1 = pd.read_sql(sql="SELECT * FROM q1_most_purchased_view", con=connection)
    q1.index += 1
    q2 = pd.read_sql(sql="SELECT * FROM q2_sales_view", con=connection)
    q2.index += 1
    return render_template('tables.html', \
                           tables=[q1.to_html(classes='q1'), q2.to_html(classes='q2')], \
                           titles=['#', 'Q1. Most Purchased Item', 'Q2. Sales View'])

if __name__ == "__main__":
    # Setup Database
    connection = create_db_connection()
    
    # Populate Table
    create_and_populate_tables(connection)
    
    # Solve
    create_solution_views(connection)
    
    # Run Web App Locally
    app.run(host=DATABASE_HOST, port=5000)



