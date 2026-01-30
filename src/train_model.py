import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib

df = pd.read_csv("data/model_data.csv")

X = df.drop("salary_lpa", axis=1)
y = df["salary_lpa"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=200)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("R2 Score:", r2_score(y_test, preds))

joblib.dump(model, "salary_model.pkl")
joblib.dump(X.columns.tolist(), "skills.pkl")
