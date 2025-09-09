# Data_Eng Assignment
# Hypothesis: Mobile Users have a higher engagement with ads

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1) Load
df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")

# 2) Inspect (basic)
print("---- HEAD ----")
print(df.head())
print("---- INFO ----")
print(df.info())
print("---- DESCRIBE ----")
print(df.describe())
print("Missing Engagement (raw):", df["Engagement_with_Ads"].isna().sum())

# 3) Clean (do NOT drop globally)
#    Standardize text, keep true blanks as NaN, and keep the string "None" as a valid category
df["Engagement_with_Ads"] = (
    df["Engagement_with_Ads"]
    .astype("string")              # preserves true missing as <NA>, not "nan"
    .str.strip()
    .str.title()
)

print("Unique devices:", df["Device_Used_for_Shopping"].unique())
print("Unique engagement levels (cleaned):", df["Engagement_with_Ads"].unique())

# Map engagement to numeric: None=0, Low=1, Medium=2, High=3
engagement_map = {"None": 0, "Low": 1, "Medium": 2, "High": 3}
df["Engagement_with_Ads_Score"] = df["Engagement_with_Ads"].map(engagement_map)
print("Unmapped after mapping (should be only true blanks):",
      df["Engagement_with_Ads_Score"].isna().sum())

# 4) Simple filter example (Smartphone users)
smartphone_users = df[df["Device_Used_for_Shopping"] == "Smartphone"]
print("---- FILTER: Smartphone Users ----")
print(smartphone_users.head())
print("Number of smartphone users:", len(smartphone_users))

# 5) Groupby: average engagement score by device
#    mean() ignores true NaN; "None" contributes as 0 (by design)
device_ads = (
    df.groupby("Device_Used_for_Shopping")["Engagement_with_Ads_Score"]
      .mean()
      .sort_values(ascending=False)
)
print("---- GROUPBY: Avg Engagement (0=None, 3=High) by Device ----")
print(device_ads)

# 6) Plot
device_ads.plot(kind="bar")
plt.title("Average Engagement with Ads by Device (0=None, 3=High)")
plt.ylabel("Average Engagement Score")
plt.xlabel("Device")
plt.tight_layout()
plt.savefig("ads_by_device.png")
plt.show()

# 7) Simple ML: predict High vs Not High from device type
#    Keep rows with a valid label; treat None/Low/Medium as NOT HIGH (0)
df_ml = df[df["Engagement_with_Ads"].notna()].copy()
df_ml["Engagement_High"] = (df_ml["Engagement_with_Ads"] == "High").astype(int)

# Features: one-hot encode device type
X = pd.get_dummies(df_ml["Device_Used_for_Shopping"], drop_first=True)
y = df_ml["Engagement_High"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train logistic regression
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict & evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("---- ML Experiment ----")
print("Accuracy of predicting High engagement from Device:", acc)
print("Model coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("Feature columns:", X.columns.tolist())
