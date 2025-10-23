import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

data = pd.read_csv("CollegePlacement.csv")
df = pd.DataFrame(data)

label_col = df[["Internship_Experience", "Placement"]]

for col in label_col:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

x = df[["IQ", "Prev_Sem_Result", "CGPA",
        "Academic_Performance", "Internship_Experience",
        "Extra_Curricular_Score", "Communication_Skills", "Projects_Completed"]]
y = df["Placement"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(x_train.values, y_train.values)

# Save model
joblib.dump(model, "placement_model.pkl")
print("Model saved successfully!")
