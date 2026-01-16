import pandas as pd
from typing import Any

def parse_data_frame(df: pd.DataFrame, relevant_cols: dict[str, str]) -> list[dict[str, str]]:
    '''
    filter out column names we don't care about to reduce context, map to a dictionary
    '''
    col_mask = [col for col in relevant_cols]
    df = df[col_mask].rename(columns=relevant_cols).to_dict(orient="records")
    return df

def parse_data_frame_exclude(df: pd.DataFrame, irrelevant_cols: set[str]) -> list[dict[str, Any]]:
    '''
    keep columns not explicitly filtered out to reduce context, map to a dictionary
    '''
    col_mask = [col for col in df.columns if col not in irrelevant_cols]
    df = df[col_mask].to_dict(orient="records")
    return df