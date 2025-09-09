# Data_Eng Assignment
# Hypothesis: Mobile Users have a higher engagement with ads


import pandas as pd
import matplotlib.pyplot as plt

# 1) Load
df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")

# 2) Inspect (basic)
print("---- HEAD ----")
print(df.head())
print("---- INFO ----")
print(df.info())
print("---- DESCRIBE ----")
print(df.describe())

# 3) Clean the columns
#    Drop rows with missing engagement, and standardize text
df = df.dropna(subset=["Engagement_with_Ads"])
df["Engagement_with_Ads"] = df["Engagement_with_Ads"].str.strip().str.title()

# Sanity checks
print("Unique devices:", df["Device_Used_for_Shopping"].unique())
print("Unique engagement levels:", df["Engagement_with_Ads"].unique())


# 4) Map engagement to numeric (1=Low, 2=Medium, 3=High)
engagement_map = {"Low": 1, "Medium": 2, "High": 3}
df["Engagement_with_Ads_Score"] = df["Engagement_with_Ads"].map(engagement_map)

# Check mapping worked
print("Unmapped after mapping:", df["Engagement_with_Ads_Score"].isna().sum())

# 4) Filter the dataset, Smartphone users
smartphone_users = df[df["Device_Used_for_Shopping"] == "Smartphone"]

print("---- FILTER: Smartphone Users ----")
print(smartphone_users.head())
print("Number of smartphone users:", len(smartphone_users))


# 5) Groupby: average engagement score by device
device_ads = (
    df.groupby("Device_Used_for_Shopping")["Engagement_with_Ads_Score"]
    .mean()
    .sort_values(ascending=False)
)
print("---- GROUPBY: Avg Engagement (1=Low,3=High) by Device ----")
print(device_ads)

# 6) Plot
device_ads.plot(kind="bar")
plt.title("Average Engagement with Ads by Device (1=Low, 3=High)")
plt.ylabel("Average Engagement Score")
plt.xlabel("Device")
plt.tight_layout()
plt.savefig("ads_by_device.png")
plt.show()


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 7) Simple ML: predict if engagement is High vs Not High using device type

# Target: 1 if High, 0 if Medium/Low
df["Engagement_High"] = (df["Engagement_with_Ads"] == "High").astype(int)

# Features: one-hot encode device type
X = pd.get_dummies(df["Device_Used_for_Shopping"], drop_first=True)
y = df["Engagement_High"]

# Split into train/test
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
