import pandas as pd
import pytz

def read_all_NL_2023():
    
    df1 = pd.read_csv('Entsoe_prices_NL/outfile_imb_15min_NL_20230101_to_20240101_reg2.csv', parse_dates=['time_stamp'])
    #df1 = pd.read_csv('Entsoe_prices_NL/outfile_imb_15min_NL_20240101_to_20250101_reg2.csv', parse_dates=['time_stamp'])

    

    df = df1.iloc[:, :2]
    df.columns = ['time_stamp', 'lbmp']
    
    # df = pd.concat(dfs)
    
    df.sort_values('time_stamp', inplace=True)
    df.reset_index(inplace=True, drop=True)
    df['hour'] = df.index



    # Ensure 'time_stamp' is in datetime format, and if it's timezone-aware, convert it to UTC first
    df['time_stamp'] = pd.to_datetime(df['time_stamp'], utc=True)

    # Convert to Amsterdam timezone
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    df['time_stamp'] = df['time_stamp'].dt.tz_convert(amsterdam_tz)

    return df