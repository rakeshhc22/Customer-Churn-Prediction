import pandas as pd

def load_and_clean_data(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)

    # Convert TotalCharges to numeric (some are empty strings)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Drop rows where TotalCharges is NaN
    df = df.dropna(subset=['TotalCharges'])

    # Drop customerID column (not useful for prediction)
    df = df.drop('customerID', axis=1)

    # Encode Churn: Yes → 1, No → 0
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

    return df

# Test the function (optional)
if __name__ == "__main__":
    df = load_and_clean_data("data/telco_customer_churn.csv")
    print(df.head())
    print(df.info())