import gdown
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

print("Downloading data from Google Drive...")
url = "https://drive.google.com/uc?export=download&id=1Bhi8U7iCCCv_2Elm9My9WgjwI0ONeGkS"
gdown.download(url, "Portland_Crime_Data_Cleaned.csv", quiet=False)

print("Loading and preparing data...")
df = pd.read_csv("Portland_Crime_Data_Cleaned.csv")
df = df.sample(frac=0.3, random_state=42)

df["month"] = df["occur_month_year"].str.split("/").str[0].astype(int)
df = df.dropna(subset=["longitude", "latitude"])

features = ["hour", "neighborhood", "month", "longitude", "latitude"]
target = "crime_type"

X = df[features].copy()
y = df[target]

le_neighborhood = LabelEncoder()
X["neighborhood"] = le_neighborhood.fit_transform(X["neighborhood"].astype(str))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Applying SMOTE...")
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("Training model...")
rf_model = RandomForestClassifier(n_estimators=10, random_state=42)
rf_model.fit(X_train_resampled, y_train_resampled)

print("Saving model and encoder...")
joblib.dump(rf_model, "portland_crime_rf_model.pkl")
joblib.dump(le_neighborhood, "neighborhood_label_encoder.pkl")

print("Done! Model and encoder saved.")