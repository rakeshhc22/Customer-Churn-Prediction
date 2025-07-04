📊 Customer Churn Prediction System
A robust machine learning-powered web application designed to predict telecom customer churn and visualize insights through dynamic charts and a user-friendly dashboard.

🧠 Objective
The aim of this project is to help telecom companies predict customer churn using historical data. It enables better customer retention strategies by analyzing customer behavior and providing predictive insights in an interactive dashboard.

⚙️ Technologies Used
🔹 Frontend
HTML/CSS: For styling and structure

JavaScript & Chart.js: For dynamic charts and data visualizations

🔹 Backend
Python (Flask): Backend framework to handle API logic and web routing

Pandas, NumPy, Scikit-learn: For preprocessing and machine learning

SQLAlchemy: ORM for database integration and queries

🔹 Database
SQLite (via SQLAlchemy): Stores prediction results and user inputs

🔑 Key Features
✅ User Authentication

Secure login system to access the prediction dashboard

✅ Churn Prediction Module

Input telecom customer data through a form

Predict whether the customer will churn or stay

Save predictions into the database

✅ Interactive Dashboard

Pie chart showing churn vs stay ratio

Line graph representing churn trend over time

Summary cards showing total predictions, churn rate, and more

✅ Data Storage

Each prediction is saved in the database with full customer details and result

📁 Folder Structure
bash
Copy
Edit
customer-churn-prediction/
├── data/
│   └── telco_customer_churn.csv         # Dataset used for training/testing
├── model/
│   └── churn_model.pkl                  # Trained machine learning model
├── src/
│   ├── app.py                           # Main Flask application
│   ├── data_preprocessing.py           # Data cleaning and preprocessing
│   ├── feature_engineering.py          # Feature transformation logic
│   ├── model_inference.py              # Model loading and prediction logic
│   ├── model_training.py               # Script to train and save the model
│   └── __pycache__/                    # Cached Python files
├── templates/
│   ├── index.html                      # Landing or login page
│   └── dashboard.html                  # Admin dashboard with graphs
├── venv/                               # Python virtual environment(you need to create yours)
└── README.md                           # Project documentation (this file)
🛠️ How to Run the Project
🔧 Prerequisites
Python 3.x installed

Virtual environment (recommended)

▶️ Setup & Run
bash
Copy
Edit
# 1. Clone the repository
git clone https://github.com/yourusername/customer-churn-prediction.git
cd customer-churn-prediction

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask server
cd src
python app.py
🌐 Access the Web App
Once the server is running, open your browser and visit:

cpp
Copy
Edit
http://127.0.0.1:5000/
Login to access the prediction form and dashboard.

📊 Sample Visualizations
Pie Chart: Percentage of customers predicted to churn vs stay

Line Chart: Zigzag graph showing trend of each prediction over time

Summary Cards: At-a-glance metrics on churn stats

🙋‍♀️ Author
Rakesh H C
rakeshchandru21@gmail.com

Feel free to ⭐ the repo and contribute!
