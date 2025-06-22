import pandas as pd

def preprocess_data(df):
    df = df.copy()
    if df.duplicated().any():
        print("Warning: Data contains duplicate rows. Removing duplicates.")
        df = df.drop_duplicates()
    df["Resolution"].fillna("No resolution documented", inplace=True)
    median_all = df["Time to Resolution"].median()
    df["Time to Resolution"].fillna(median_all, inplace=True)
    mean_rating = df["Customer Satisfaction Rating"].mean()
    df["Customer Satisfaction Rating"].fillna(mean_rating, inplace=True)
    df = df[df["First Response Time"].notna()]
    df["First Response Hrs"] = (
        df["First Response Time"].dt.hour
        + df["First Response Time"].dt.minute  / 60
        + df["First Response Time"].dt.second  / 3600
    )

    df["Resolution Hrs"] = (
        df["Time to Resolution"].dt.hour
        + df["Time to Resolution"].dt.minute  / 60
        + df["Time to Resolution"].dt.second  / 3600
    )
    return df