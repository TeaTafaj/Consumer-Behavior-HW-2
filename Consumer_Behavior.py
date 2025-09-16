# Consumer_Behavior.py
# Hypothesis: Mobile Users have a higher engagement with ads

from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

ENGAGEMENT_MAP = {"None": 0, "Low": 1, "Medium": 2, "High": 3}


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_engagement(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Engagement_with_Ads"] = (
        df["Engagement_with_Ads"]
        .astype("string")  # keeps true NA as <NA>
        .str.strip()
        .str.title()
    )
    df["Engagement_with_Ads_Score"] = df["Engagement_with_Ads"].map(ENGAGEMENT_MAP)
    return df


def filter_smartphone_users(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["Device_Used_for_Shopping"] == "Smartphone"]


def group_device_ads_mean(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("Device_Used_for_Shopping")["Engagement_with_Ads_Score"]
        .mean()
        .sort_values(ascending=False)
    )


def plot_device_ads(device_ads: pd.Series, out_path: str = "ads_by_device.png") -> None:
    import matplotlib.pyplot as plt  # import inside function

    ax = device_ads.plot(kind="bar")
    ax.set_title("Average Engagement with Ads by Device (0=None, 3=High)")
    ax.set_ylabel("Average Engagement Score")
    ax.set_xlabel("Device")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def prepare_ml_frame(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    df_ml = df[df["Engagement_with_Ads"].notna()].copy()
    df_ml["Engagement_High"] = (df_ml["Engagement_with_Ads"] == "High").astype(int)
    X = pd.get_dummies(df_ml["Device_Used_for_Shopping"], drop_first=True)
    y = df_ml["Engagement_High"]
    return X, y


def train_and_eval_logreg(
    X: pd.DataFrame, y: pd.Series, random_state: int = 42
) -> Tuple[LogisticRegression, float]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return model, acc


def main() -> None:
    # 1) Load
    df = load_data("Ecommerce_Consumer_Behavior_Analysis_Data.csv")

    # 2) Basic inspect
    print("---- HEAD ----")
    print(df.head())
    print("---- INFO ----")
    print(df.info())
    print("---- DESCRIBE ----")
    print(df.describe())
    print("Missing Engagement (raw):", df["Engagement_with_Ads"].isna().sum())

    # 3) Clean
    df = clean_engagement(df)
    print("Unique devices:", df["Device_Used_for_Shopping"].unique())
    print("Unique engagement levels (cleaned):", df["Engagement_with_Ads"].unique())
    print(
        "Unmapped after mapping (should be true blanks only):",
        df["Engagement_with_Ads_Score"].isna().sum(),
    )

    # 4) Filter example
    smartphone_users = filter_smartphone_users(df)
    print("---- FILTER: Smartphone Users ----")
    print(smartphone_users.head())
    print("Number of smartphone users:", len(smartphone_users))

    # 5) Groupby + 6) Plot
    device_ads = group_device_ads_mean(df)
    print("---- GROUPBY: Avg Engagement (0=None, 3=High) by Device ----")
    print(device_ads)
    plot_device_ads(device_ads, out_path="ads_by_device.png")

    # 7) ML
    X, y = prepare_ml_frame(df)
    model, acc = train_and_eval_logreg(X, y)
    print("---- ML Experiment ----")
    print("Accuracy of predicting High engagement from Device:", acc)
    print("Model coefficients:", model.coef_)
    print("Intercept:", model.intercept_)
    print("Feature columns:", X.columns.tolist())


if __name__ == "__main__":
    main()
