import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):
    """Detect unusual expenses using Isolation Forest."""

    if len(df) < 10:
        return pd.DataFrame()

    data = df[["Amount"]].copy()

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    data["Anomaly"] = model.fit_predict(
        data[["Amount"]]
    )

    anomalies = df[
        data["Anomaly"] == -1
    ].copy()

    if not anomalies.empty:
        anomalies["Reason"] = (
            "Unusually high expense compared with "
            "other transactions"
        )

    return anomalies


if __name__ == "__main__":

    df = pd.read_csv("expenses.csv")

    anomalies = detect_anomalies(df)

    print("\n===== ANOMALY DETECTION =====")

    if anomalies.empty:

        print("No unusual expenses detected.")

    else:

        print("Unusual expenses detected:\n")

        print(
            anomalies[
                [
                    "Date",
                    "Category",
                    "Amount",
                    "Description",
                    "Reason"
                ]
            ].to_string(index=False)
        )