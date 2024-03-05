import joblib
import numpy as np
import pandas as pd
from house_prices.preprocess import process_data


def make_predictions(data: pd.DataFrame) -> np.array:
    train_data = data.copy()
    train_data = process_data(train_data)
    model = joblib.load(
        "/Users/ericwindsor/Documents/EPITA_ERIC/"
        "Data_Scicence_Production/dsp-zihang-wang/models"
        "/lreg.model"
    )
    predictions = model.predict(train_data)
    return predictions
