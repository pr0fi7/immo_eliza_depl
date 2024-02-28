import joblib
import pandas as pd

def predict(file_path):
    data = pd.read_csv(file_path)

    artifacts = joblib.load("src/artifacts.joblib")

    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]
    model = artifacts["model"]

    # Extract the used data
    data = data[num_features + fl_features + cat_features]

    # Apply imputer and encoder on data
    data[num_features] = imputer.transform(data[num_features])
    data_cat = enc.transform(data[cat_features]).toarray()

    # Combine the numerical and one-hot encoded categorical columns
    data = pd.concat(
        [
            data[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(data_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    # Make predictions
    predictions = model.predict(data)
    
    return predictions.tolist()   
