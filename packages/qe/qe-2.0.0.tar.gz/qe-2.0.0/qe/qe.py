import os
import pandas as pd
from tempfile import gettempdir
from uuid import uuid4


def qe(df, applyTable=True):
    # Generate a unique filename, optionally prefixed with df.name
    prefix = (df.name + "_") if hasattr(df, 'name') and df.name else ""
    suffix = '.xlsx'
    temp_dir = gettempdir()
    unique_filename = str(uuid4())  # Generate a unique component to ensure the filename is unique
    abs_path = os.path.join(temp_dir, prefix + unique_filename + suffix)

    # Check for and handle MultiIndex in columns
    if isinstance(df.columns, pd.MultiIndex):
        # Flatten the MultiIndex columns
        df.columns = [' '.join(col).strip() for col in df.columns.values]

    # Convert timezone-aware columns to timezone-naive
    for col in df.select_dtypes(include=['datetime64[ns, UTC]']).columns:
        df[col] = df[col].dt.tz_localize(None)

    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    if applyTable:
        with pd.ExcelWriter(abs_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)  # Set index=False to ensure proper table formatting
            worksheet = writer.sheets['Sheet1']

            # Create column headers for the Excel table
            c = [{'header': str(x)} for x in df.columns]

            # Add an Excel table with adjusted dimensions to include all DataFrame columns
            worksheet.add_table(0, 0, len(df), len(df.columns) - 1, {'columns': c})
    else:
        df.to_excel(abs_path)

    os.system(f"start Excel \"{abs_path}\"")
    return True


if __name__ == '__main__':
    # Example DataFrame with a name
    df_name = 'SampleData'
    arrays = [['A', 'A', 'B', 'B'], ['one', 'two', 'one', 'two']]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
    d = pd.DataFrame([[1, 2, 3, 4], [5, 6, 7, 8]], columns=index)
    d.name = df_name  # Setting the DataFrame's name
    qe(d)
