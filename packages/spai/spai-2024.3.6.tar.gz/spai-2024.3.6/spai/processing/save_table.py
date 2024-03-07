import pandas as pd


def save_table(data, columns, table_name, date, storage):
    # columns number must be equal to data number of columns
    if len(columns) != len(data):
        raise ValueError("columns number must be equal to data number of columns")
    # check if table exists in storage
    if table_name in storage.list():
        # append data to table
        base_df = storage.read(table_name)
        if isinstance(base_df.index, pd.DatetimeIndex):
            # Handle pd.DateTimeIndex, converting index to string
            base_df.index = base_df.index.strftime("%Y-%m-%d")
        df = pd.concat(
            [pd.DataFrame([data], columns=columns, index=[date]), base_df.loc[:]]
        )
    else:
        # create table with data
        df = pd.DataFrame([data], columns=columns, index=[date])
    storage.create(data=df, name=table_name)
    return df
