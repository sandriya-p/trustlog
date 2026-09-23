import joblib
import pandas as pd


def test_model_loads_and_predicts():
    model = joblib.load("results/random_forest_model.joblib")
    test_df = pd.read_csv("data/processed/features_test.csv")
    X = test_df.drop(columns=["label"]).head(5)
    preds = model.predict(X)
    assert len(preds) == 5
    assert set(preds).issubset({0, 1})