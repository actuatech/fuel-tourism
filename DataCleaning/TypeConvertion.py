def convert_to_integer_df_columns(stock_and_mileage_df):
    """
    Convert to integer activity statistics columns of the stock and mileage dataframe and check for nans
    """
    try:
        stock_and_mileage_df['Mean_Activity'] = stock_and_mileage_df['Mean_Activity'].fillna(0).astype(int)
    except ValueError:
        print('Check for nan values in the stock_and_mileage dataframe: Mean activity')

    try:
        stock_and_mileage_df['Min_Activity'] = stock_and_mileage_df['Min_Activity'].fillna(0).astype(int)
    except ValueError:
        print('Check for nan values in the stock_and_mileage dataframe: Min activity')

    try:
        stock_and_mileage_df['Max_Activity'] = stock_and_mileage_df['Max_Activity'].fillna(0).astype(int)
    except ValueError:
        print('Check for nan values in the stock_and_mileage dataframe: Max activity')

    try:
        stock_and_mileage_df['Std_Activity'] = stock_and_mileage_df['Std_Activity'].fillna(0).astype(int)
    except ValueError:
        print('Check for nan values in the stock_and_mileage dataframe: Standard deviation activity')
