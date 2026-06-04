from fastapi import FastAPI, HTTPException
import mysql.connector
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection
con = mysql.connector.connect(
    host=os.getenv("db_host"),
    port=int(os.getenv("db_port")),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_name"),
    ssl_disabled=False
)

cur = con.cursor(dictionary=True)

# Create Table
cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    exp_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

con.commit()

@app.get("/")
def home():
    return{
        "msg":"Backend Running Successfully"
    }

# Add Expense
@app.post("/add_exp")
def add_expense(new_data: dict):

    query = """
    INSERT INTO expenses(title, amount, category)
    VALUES (%s, %s, %s)
    """

    values = (
        new_data["t"],
        new_data["a"],
        new_data["c"]
    )

    cur.execute(query, values)
    con.commit()

    return {
        "msg": "Expense Added Successfully"
    }

# View All Expenses
@app.get("/view_exp")
def view_expenses():

    query = "SELECT * FROM expenses"

    cur.execute(query)
    data = cur.fetchall()

    for row in data:
        row["amount"] = float(row["amount"])

    return {
        "expenses": data
    }

# Get Expense By ID
@app.get("/get_exp/{exp_id}")
def get_expense(exp_id: int):

    query = "SELECT * FROM expenses WHERE exp_id = %s"

    cur.execute(query, (exp_id,))
    data = cur.fetchone()

    if data:
        data["amount"] = float(data["amount"])
        return {
            "expense": data
        }

    return {
        "expense": None
    }

# Update Expense
@app.put("/update_exp/{exp_id}")
def update_expense(exp_id: int, update_data: dict):

    query = """
    UPDATE expenses
    SET title = %s,
        amount = %s,
        category = %s
    WHERE exp_id = %s
    """

    values = (
        update_data["t"],
        update_data["a"],
        update_data["c"],
        exp_id
    )

    cur.execute(query, values)
    con.commit()

    return {
        "msg": "Expense Updated Successfully"
    }

# Delete Expense
@app.delete("/delete_exp/{exp_id}")
def delete_expense(exp_id: int):

    query = "DELETE FROM expenses WHERE exp_id = %s"

    cur.execute(query, (exp_id,))
    con.commit()

    return {
        "msg": "Expense Deleted Successfully"
    }

# Search Expense
@app.get("/search_exp/{text}")
def search_expense(text: str):

    query = """
    SELECT * FROM expenses
    WHERE title LIKE %s
    OR category LIKE %s
    """

    values = (
        f"%{text}%",
        f"%{text}%"
    )

    cur.execute(query, values)
    data = cur.fetchall()

    for row in data:
        row["amount"] = float(row["amount"])

    return {
        "search_result": data
    }

# Sort Expenses
@app.get("/sort_exp/{column}/{order}")
def sort_expenses(column: str, order: str):

    allowed_columns = ["title", "amount", "category", "exp_id"]
    allowed_orders = ["asc", "desc"]

    if column.lower() not in allowed_columns:
        raise HTTPException(status_code=400, detail="Invalid Column")

    if order.lower() not in allowed_orders:
        raise HTTPException(status_code=400, detail="Invalid Order")

    query = f"""
    SELECT * FROM expenses
    ORDER BY {column} {order}
    """

    cur.execute(query)
    data = cur.fetchall()

    for row in data:
        row["amount"] = float(row["amount"])

    return {
        "sorted_expenses": data
    }

# Filter Expenses
@app.get("/filter_exp/{category}")
def filter_expenses(category: str):

    query = "SELECT * FROM expenses WHERE category = %s"

    cur.execute(query, (category,))
    data = cur.fetchall()

    for row in data:
        row["amount"] = float(row["amount"])

    return {
        "filtered_expenses": data
    }

# Analyze Spending
@app.get("/analyze_spending")
def analyze_spending():

    cur.execute("SELECT SUM(amount) AS total FROM expenses")
    total = cur.fetchone()

    cur.execute("""
    SELECT category,
           SUM(amount) AS total
    FROM expenses
    GROUP BY category
    """)

    category_data = cur.fetchall()

    return {
        "total_spending": total,
        "category_spending": category_data
    }