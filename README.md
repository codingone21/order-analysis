# van-deli-order-analysis

## Stack Overview
Database: MySQL
Web App Framework: Flask
Languages: Python 3.8, Html/Css
Python Packages: flask, flask_mysqldb, pandas

## Package Org
```
van-deli-order-analysis
|_ static
    |_ style.css: style guide for html table formatting
|_ templates
    |_ index.html: home page
    |_ tables.html: page to view order analysis tables
|_ setupDatabase.py : creates, populates, and analyzes DB
|_ webApp.py : runnable Python which queries from DB and starts Flask app
```

## How to Run
1. Ensure your system has MySQL and Python installed and configured. 
2. Run 'webApp.py', which contains the main runnable. This will create the db connection, populate tables, analyze orders, and start the local web app.
3. Go to http://localhost:5000/ on your local web page to view the results.