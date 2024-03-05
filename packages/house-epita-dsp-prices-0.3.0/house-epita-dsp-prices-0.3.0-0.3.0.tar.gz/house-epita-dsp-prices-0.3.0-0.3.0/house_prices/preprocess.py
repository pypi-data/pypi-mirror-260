import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import joblib
from sklearn.model_selection import train_test_split


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = encode_categorical(df)
    df = fillna_continuous(df)
    df = fillna_categorical(df)
    return df


def split_data(
    data_train: pd.DataFrame,
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    X, y = (data_train.loc[:, data_train.columns != "SalePrice"],
            data_train["SalePrice"])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )
    for data in [X_train, X_test, y_train, y_test]:
        data.reset_index(drop=True, inplace=True)
    return X_train, X_test, y_train, y_test


# get_continuous_columns from the dataframe
def get_continuous_columns(df: pd.DataFrame) -> pd.Series:
    return df.select_dtypes(include="number").columns


# fill the missing data
def fillna_continuous(df: pd.DataFrame) -> pd.DataFrame:
    columns = get_continuous_columns(df)
    [df[column].fillna(0, inplace=True) for column in columns]
    return df


# get_continuous_columns from the dataframe
def get_categorical_columns(df: pd.DataFrame) -> pd.Series:
    return df.select_dtypes(include="object").columns


# fill the missing data
def fillna_categorical(df: pd.DataFrame) -> pd.DataFrame:
    columns = get_categorical_columns(df)
    [df[column].fillna("Unknown", inplace=True) for column in columns]
    return df


# Create encoder
def make_encoder(df: pd.DataFrame) -> OneHotEncoder:
    encoder_path = ("/Users/ericwindsor/Documents/EPITA_ERIC/"
                    "Data_Scicence_Production/dsp-zihang-wang/models"
                    "/encoder.OneHotEncoder")
    categorical_columns = get_categorical_columns(df)
    encoder = OneHotEncoder(handle_unknown="ignore", dtype=int)
    encoder.fit(df[categorical_columns])
    joblib.dump(encoder, encoder_path)
    return encoder


# Encode the categorial columns
def encode_categorical(df: pd.DataFrame) -> pd.DataFrame:
    categorical_columns = get_categorical_columns(df)
    encoder_path = ("/Users/ericwindsor/Documents/EPITA_ERIC/"
                    "Data_Scicence_Production/dsp-zihang-wang/models"
                    "/encoder.OneHotEncoder")
    encoder = joblib.load(encoder_path)
    encoded_columns = encoder.transform(df[categorical_columns])
    encoded_df = pd.DataFrame(
        encoded_columns.toarray(),
        columns=encoder.get_feature_names_out(categorical_columns),
    )
    df = df.drop(categorical_columns, axis=1).join(encoded_df)
    return df
