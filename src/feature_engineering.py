from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

df = pd.read_csv("data/cleaned_jobs.csv")

df["skills_list"] = df["skills"].apply(lambda x: x.lower().split(","))

mlb = MultiLabelBinarizer()
skill_features = mlb.fit_transform(df["skills_list"])

skills_df = pd.DataFrame(skill_features, columns=mlb.classes_)
final_df = pd.concat([skills_df, df["salary_lpa"]], axis=1)

final_df.to_csv("data/model_data.csv", index=False)
