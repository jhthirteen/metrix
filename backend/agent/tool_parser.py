import pandas as pd

def parse_data_frame(df: pd.DataFrame, relevant_cols: dict[str, str]) -> dict[str, str]:
    '''
    filter out column names we don't care about to reduce context, map to a dictionary
    '''
    col_mask = [col for col in relevant_cols]
    df = df[col_mask].rename(columns=relevant_cols).to_dict(orient="records")
    return df