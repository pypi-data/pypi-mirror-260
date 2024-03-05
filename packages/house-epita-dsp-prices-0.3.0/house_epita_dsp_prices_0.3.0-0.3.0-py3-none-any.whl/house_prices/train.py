import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_log_error
from sklearn.linear_model import LinearRegression
from house_prices.preprocess import process_data, split_data


def build_model(data: pd.DataFrame) -> dict[str, str]:
    # Returns a dictionary with the model
    # performances (for example {'rmse': 0.18})
    data_train = data.copy()
    X_train, X_test, y_train, y_test = get_train_data(data_train)
    X_train = process_data(X_train)
    X_test = process_data(X_test)
    model = make_model(X_train, y_train)
    y_pred = abs(model.predict(X_test))
    rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))

    return {"rmsle": round(rmsle, 2)}


def get_train_data(data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    X_train, X_test, y_train, y_test = split_data(data)
    return X_train, X_test, y_train, y_test


def make_model(X_train: pd.DataFrame, y_train: pd.DataFrame) \
        -> LinearRegression:
    model_path = ("/Users/ericwindsor/Documents/EPITA_ERIC/"
                  "Data_Scicence_Production/dsp-zihang-wang/models"
                  "/lreg.model")
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, model_path)
    return model
