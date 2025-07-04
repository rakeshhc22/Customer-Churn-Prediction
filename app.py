from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import joblib
import pandas as pd
import csv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    gender = db.Column(db.String(10))
    SeniorCitizen = db.Column(db.Integer)
    Partner = db.Column(db.String(5))
    Dependents = db.Column(db.String(5))
    
    tenure = db.Column(db.Integer)
    
    PhoneService = db.Column(db.String(5))
    MultipleLines = db.Column(db.String(20))
    
    InternetService = db.Column(db.String(20))
    OnlineSecurity = db.Column(db.String(20))
    OnlineBackup = db.Column(db.String(20))
    DeviceProtection = db.Column(db.String(20))
    TechSupport = db.Column(db.String(20))
    StreamingTV = db.Column(db.String(20))
    StreamingMovies = db.Column(db.String(20))
    
    Contract = db.Column(db.String(20))
    PaperlessBilling = db.Column(db.String(5))
    PaymentMethod = db.Column(db.String(50))
    
    MonthlyCharges = db.Column(db.Float)
    TotalCharges = db.Column(db.Float)
    
    prediction = db.Column(db.String(10))  # to store "Yes" or "No"

with app.app_context():
    db.create_all()


app.secret_key = 'your_secret_key'  # Used for sessions

# Load the trained model
model = joblib.load("model/churn_model.pkl")


# Manual mappings (must match the training phase encoding)
mappings = {
    "gender": {"Male": 1, "Female": 0},
    "Partner": {"Yes": 1, "No": 0},
    "Dependents": {"Yes": 1, "No": 0},
    "PhoneService": {"Yes": 1, "No": 0},
    "MultipleLines": {"Yes": 1, "No": 0, "No phone service": 2},
    "InternetService": {"DSL": 1, "Fiber optic": 2, "No": 0},
    "OnlineSecurity": {"Yes": 1, "No": 0, "No internet service": 2},
    "OnlineBackup": {"Yes": 1, "No": 0, "No internet service": 2},
    "DeviceProtection": {"Yes": 1, "No": 0, "No internet service": 2},
    "TechSupport": {"Yes": 1, "No": 0, "No internet service": 2},
    "StreamingTV": {"Yes": 1, "No": 0, "No internet service": 2},
    "StreamingMovies": {"Yes": 1, "No": 0, "No internet service": 2},
    "Contract": {"Month-to-month": 0, "One year": 1, "Two year": 2},
    "PaperlessBilling": {"Yes": 1, "No": 0},
    "PaymentMethod": {
        "Electronic check": 0,
        "Mailed check": 1,
        "Bank transfer (automatic)": 2,
        "Credit card (automatic)": 3
    }
}

# Sample credentials
USER_CREDENTIALS = {'admin': 'admin123'}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    password = request.form['password']

    if user_id in USER_CREDENTIALS and USER_CREDENTIALS[user_id] == password:
        session['user'] = user_id
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))

    # Raw counts
    churn_counts_raw = {"Customer will churn": 0, "Customer will stay": 0}
    for entry in Prediction.query.all():
        churn_counts_raw[entry.prediction] += 1

    
    all_predictions = Prediction.query.all()
    churn = sum(1 for p in all_predictions if p.prediction == "Customer will churn")
    stay = sum(1 for p in all_predictions if p.prediction == "Customer will stay")
    total = churn + stay
    churn_rate = round((churn / total) * 100, 2) if total > 0 else 0
    # Map verbose to simplified
    churn_counts = {
        "Churn": churn_counts_raw.get("Customer will churn", 0),
        "Stay": churn_counts_raw.get("Customer will stay", 0)
    }


    return render_template("dashboard.html", churn_data=churn_counts,total=total,
        churn=churn,
        stay=stay,
        churn_rate=churn_rate,)



@app.route("/predict_form")
def predict_form():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template("predict.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.form.to_dict()

        # Apply mappings
        for col, mapping in mappings.items():
            if col in data:
                data[col] = mapping.get(data[col], 0)

        input_df = pd.DataFrame([data])

        for col in ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

        prediction = model.predict(input_df)
        result = "Customer will churn" if prediction[0] == 1 else "Customer will stay"

        new_entry = Prediction(
            gender=request.form['gender'],
            SeniorCitizen=int(request.form['SeniorCitizen']),
            Partner=request.form['Partner'],
            Dependents=request.form['Dependents'],
            tenure=int(request.form['tenure']),
            PhoneService=request.form['PhoneService'],
            MultipleLines=request.form['MultipleLines'],
            InternetService=request.form['InternetService'],
            OnlineSecurity=request.form['OnlineSecurity'],
            OnlineBackup=request.form['OnlineBackup'],
            DeviceProtection=request.form['DeviceProtection'],
            TechSupport=request.form['TechSupport'],
            StreamingTV=request.form['StreamingTV'],
            StreamingMovies=request.form['StreamingMovies'],
            Contract=request.form['Contract'],
            PaperlessBilling=request.form['PaperlessBilling'],
            PaymentMethod=request.form['PaymentMethod'],
            MonthlyCharges=float(request.form['MonthlyCharges']),
            TotalCharges=float(request.form['TotalCharges']),
            prediction=result  # the prediction result from your model
        )

        db.session.add(new_entry)
        db.session.commit()

        return render_template("predict.html", prediction_text=result)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/view_entries')
def view_entries():
    entries = Prediction.query.all()
    output = ""

    for e in entries:
        output += f"""
        <b>Entry ID:</b> {e.id}<br>
        Gender: {e.gender}<br>
        SeniorCitizen: {e.SeniorCitizen}<br>
        Partner: {e.Partner}<br>
        Dependents: {e.Dependents}<br>
        Tenure: {e.tenure}<br>
        PhoneService: {e.PhoneService}<br>
        MultipleLines: {e.MultipleLines}<br>
        InternetService: {e.InternetService}<br>
        OnlineSecurity: {e.OnlineSecurity}<br>
        OnlineBackup: {e.OnlineBackup}<br>
        DeviceProtection: {e.DeviceProtection}<br>
        TechSupport: {e.TechSupport}<br>
        StreamingTV: {e.StreamingTV}<br>
        StreamingMovies: {e.StreamingMovies}<br>
        Contract: {e.Contract}<br>
        PaperlessBilling: {e.PaperlessBilling}<br>
        PaymentMethod: {e.PaymentMethod}<br>
        MonthlyCharges: {e.MonthlyCharges}<br>
        TotalCharges: {e.TotalCharges}<br>
        <b>Prediction:</b> {e.prediction}<br>
        <hr>
        """

    return output


if __name__ == "__main__":
    app.run(debug=True)
