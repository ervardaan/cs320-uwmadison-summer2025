'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP8
Student 1: vardaan kapoor, vkapoor5
'''

# main.py

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

class UserPredictor:
    def __init__(self):
        self.pipeline = None
        self.xcols = None

    def _prepare_features(self, users_df: pd.DataFrame, logs_df: pd.DataFrame) -> pd.DataFrame:
        df = users_df.copy()
        logs_agg = (
            logs_df
            .groupby('user_id')
            .agg(
                total_seconds=('seconds', 'sum'),
                visit_count=('url', 'count'),
                avg_seconds=('seconds', 'mean'),
                laptop_visits=('url', lambda urls: urls.str.contains('laptop', case=False).sum())
            )
            .reset_index()
        )

        df = df.merge(logs_agg, on='user_id', how='left')
        for col in ['total_seconds', 'visit_count', 'avg_seconds', 'laptop_visits']:
            df[col] = df[col].fillna(0)

        return df

    def fit(self, users_df: pd.DataFrame, logs_df: pd.DataFrame, y_df: pd.DataFrame) -> None:
        data = self._prepare_features(users_df, logs_df)
        X = data.drop(columns=['user_id'])
        y = y_df['y']
        self.xcols = X.columns.tolist()
        numeric_features = X.select_dtypes(include=['number']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        numeric_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        categorical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer([
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(max_iter=1000))
        ])

        # Fit model
        self.pipeline.fit(X, y)

    def predict(self, users_df: pd.DataFrame, logs_df: pd.DataFrame) -> pd.Series:
        data = self._prepare_features(users_df, logs_df)
        X = data[self.xcols]
        preds = self.pipeline.predict(X)
        return pd.Series(preds.astype(bool), index=users_df.index)
