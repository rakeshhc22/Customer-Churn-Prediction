import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from data_preprocessing import load_and_clean_data

def encode_and_split_data(df):
    # Encode categorical features
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Separate features (X) and target (y)
    X = df.drop('Churn', axis=1)
    y = df['Churn']

    # Split into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, label_encoders

# Run this file to test the function
if __name__ == "__main__":
    df = load_and_clean_data("data/telco_customer_churn.csv")
    X_train, X_test, y_train, y_test, encoders = encode_and_split_data(df)

    print("Training set size:", X_train.shape)
    print("Test set size:", X_test.shape)
