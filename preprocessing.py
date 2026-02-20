import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_data(filepath):
    df = pd.read_csv(filepath, sep=';')

    # Convert target
    df['y'] = df['y'].map({'yes': 1, 'no': 0})

    return df


def create_preprocessor(df):

    X = df.drop("y", axis=1)

    categorical_cols = X.select_dtypes(include=['object']).columns
    numerical_cols = X.select_dtypes(exclude=['object']).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ]
    )

    return preprocessor
