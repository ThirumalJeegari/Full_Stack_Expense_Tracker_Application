# 💰 Full Stack Expense Tracker Application

A simple **Full Stack Expense Tracker** built using:

- ⚡ FastAPI (Backend API)
- 🗄️ MySQL (Database)
- 🎨 Streamlit (Frontend UI)
- 📊 Plotly (Data Visualization)

This project helps users **add, view, update, delete, search, filter, sort, and analyze expenses** in a simple dashboard.

---

# 🚀 Features

### 🧾 Expense Management
- Add new expenses
- View all expenses
- Update existing expenses
- Delete expenses

### 🔍 Smart Features
- Search expenses by title or category
- Filter by category
- Sort by columns (title, amount, category, id)

### 📊 Analytics Dashboard
- Total spending calculation
- Category-wise spending
- Bar chart visualization
- Pie chart distribution

---

# 🏗️ Tech Stack

| Layer      | Technology |
|------------|-----------|
| Frontend   | Streamlit |
| Backend    | FastAPI |
| Database   | MySQL |
| Visualization | Plotly |
| API Calls  | Requests |

---

# 📁 Project Structure


Full_Stack_Expense_Tracker/
│
├── backend/
│ └── main.py # FastAPI backend
│
├── frontend/
│ └── app.py # Streamlit frontend
│
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md


---

# ⚙️ Setup Instructions

## 1️⃣ Clone the Repository

```bash


git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker


2️⃣ Create Virtual Environment

python -m venv venv

Activate it:

Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Setup Environment Variables (.env)

Create a .env file in the backend folder:


db_host=your_mysql_host
db_port=3306
db_user=your_mysql_user
db_password=your_mysql_password
db_name=your_database_name

5️⃣ Run Backend (FastAPI)

uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000

6️⃣ Run Frontend (Streamlit)

streamlit run app.py

Frontend will open in browser:

http://localhost:8501

🔌 API Endpoints
➕ Add Expense

POST /add_exp

Body:
{
  "t": "Food",
  "a": 250,
  "c": "Food 🍛"
}

📄 View Expenses

GET /view_exp

🔍 Get Expense by ID

GET /get_exp/{exp_id}

✏️ Update Expense

PUT /update_exp/{exp_id}

❌ Delete Expense

DELETE /delete_exp/{exp_id}

🔎 Search Expense

GET /search_exp/{text}

📊 Sort Expenses

GET /sort_exp/{column}/{order}

Example:

/sort_exp/amount/asc

🧾 Filter Expenses

GET /filter_exp/{category}

📈 Analyze Spending

GET /analyze_spending

📊 Example Output

Total Spending

₹51449
Category-wise Chart
Food 🍛
Travel 🚌
Bills 📱
Shopping 👕
etc.


🧠 What You Learn from This Project

REST API development using FastAPI
Database operations with MySQL
Frontend development using Streamlit
API integration using Requests
Data visualization using Plotly
CRUD operations in real-world applications

🛠️ Future Improvements

User login system (Authentication)
Monthly budget tracking
Export data to Excel/PDF
Cloud database integration
Mobile responsive UI



👨‍💻 Author
Thirumal Jeegari