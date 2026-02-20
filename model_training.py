import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_data(filepath):
    # Use dtype='object' to avoid StringDtype issues
    df = pd.read_csv(filepath, sep=';', dtype=object)
    
    # Safely convert target
    df['y'] = pd.to_numeric(df['y'].map({'yes': 1, 'no': 0}), errors='coerce').astype('int64')
    
    # Convert numeric columns to float, keeping as object for string columns
    numeric_cols = ['age', 'balance', 'day_of_week', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def create_preprocessor(df):

    X = df.drop("y", axis=1)

    # Identify numeric and categorical columns more carefully
    numeric_cols = X.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns
    categorical_cols = X.select_dtypes(include=['object']).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
        ],
        remainder='drop'
    )

    return preprocessor

# Load dataset
df = load_data("C:/ai/MarketMind/data/bank_marketing.csv")

X = df.drop("y", axis=1)
y = df["y"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create preprocessor
preprocessor = create_preprocessor(df)

# 🔥 Professional ML Pipeline
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        class_weight='balanced',
        max_iter=1000,
        random_state=42
    ))
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
preds = pipeline.predict(X_test)
print(classification_report(y_test, preds))

# Save full pipeline (IMPORTANT)
joblib.dump(pipeline, "C:/ai/MarketMind/backend/models/lead_model.pkl")

print("Professional ML pipeline trained and saved.")
