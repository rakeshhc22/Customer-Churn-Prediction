import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from feature_engineering import load_and_clean_data, encode_and_split_data

def train_and_save_model():
    df = load_and_clean_data("data/telco_customer_churn.csv")
    X_train, X_test, y_train, y_test, _ = encode_and_split_data(df)

    # Train the model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the trained model
    joblib.dump(model, "model/churn_model.pkl")
    print("Model saved to model/churn_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
