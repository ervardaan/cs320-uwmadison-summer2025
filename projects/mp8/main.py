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
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer

class UserPredictor:
    def __init__(self):
        # Will hold the sklearn pipeline
        self.model: Pipeline = None
        # Columns used for predictions (after feature engineering)
        self.feature_columns: list = []

    def add_log_features(self, users_df: pd.DataFrame, logs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate per-user statistics from logs and merge into users_df.
        Adds columns like total_time, visit_count, laptop_visits.
        """
        # Compute aggregates
        grp = logs_df.groupby('user_id')
        agg = grp['minutes'].agg([
            ('total_time', 'sum'),
            ('avg_time', 'mean'),
            ('visit_count', 'count')
        ]).reset_index()
        # Count visits to laptop.html specifically
        laptop_visits = logs_df[logs_df['url'].str.contains('laptop', na=False)] \
                        .groupby('user_id').size().reset_index(name='laptop_visits')
        # Merge all
        features = agg.merge(laptop_visits, on='user_id', how='left')
        features['laptop_visits'] = features['laptop_visits'].fillna(0)
        # Merge into users
        df = users_df.merge(features, on='user_id', how='left')
        # Fill NaNs for users with no logs
        for col in ['total_time', 'avg_time', 'visit_count', 'laptop_visits']:
            df[col] = df[col].fillna(0)
        return df

    def fit(self, users_df: pd.DataFrame, logs_df: pd.DataFrame, y_df: pd.DataFrame):
        """
        Fit the classifier on training data.
        users_df: DataFrame of user features
        logs_df: DataFrame of user logs
        y_df: DataFrame with columns ['user_id', 'y']
        """
        # Build features
        df = self.add_log_features(users_df.copy(), logs_df)
        # Align target
        y = y_df.set_index('user_id').loc[df['user_id'], 'y']

        # Drop identifier
        X = df.drop(columns=['user_id'])

        # Remember feature columns
        self.feature_columns = X.columns.tolist()

        # Identify numeric and categorical columns
        numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

        # Preprocessing for numeric data: impute and scale
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        # Preprocessing for categorical data: impute and one-hot encode
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )

        # Final pipeline: preprocessing + classifier
        self.model = Pipeline(steps=[
            ('preproc', preprocessor),
            ('clf', LogisticRegression(max_iter=1000))
        ])

        # Fit the pipeline
        self.model.fit(X, y)

    def predict(self, users_df: pd.DataFrame, logs_df: pd.DataFrame) -> np.ndarray:
        """
        Predict clicks for new users.
        Returns a boolean numpy array of predictions.
        """
        # Build features in the same way as in fit
        df = self.add_log_features(users_df.copy(), logs_df)
        X = df[['user_id'] + self.feature_columns].drop(columns=['user_id'])

        # Predict probabilities and threshold at 0.5
        probs = self.model.predict_proba(X)[:, 1]
        return (probs >= 0.5)


