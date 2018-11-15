import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_folder = "/Users/Fyxstkala/Desktop/FA18/PSYC_4559/raw_data/"
hr_file = data_folder + "Smartwatch_HeartRateDatum.csv"
acc_file = data_folder + "Sensus_Accelerometer.csv"

def import_hr_file():
    df = pd.read_csv(hr_file, header = 0, nrows = 10000)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'],
                                    origin="unix")
    df.set_index(['Timestamp'], inplace=True)
    df["HR"]= pd.to_numeric(df["HR"],errors='coerce',downcast="integer")
    return df[["HR"]]

def import_acc_file():
    df = pd.read_csv(acc_file, header = 0)
    df = df.loc[df['ParticipantId'] == 9]
    df['Timestamp'] = pd.to_datetime(df['Timestamp'],
                                    origin="unix")
    df.set_index(['Timestamp'], inplace=True)
    df[['X','Y','Z']] = df[['X','Y','Z']].apply(pd.to_numeric,
                                        errors='coerce',
                                        downcast="float")
    df.fillna(0)
    return df[['X','Y','Z']]

# resampel accelorometer by 1 second
def resample_acc(acc_df):
    grouped = acc_df.resample('S').mean()
    return grouped

# HELPER FUNCTION
# get s second time intervals given start time (day, hour, minute)
def get_interval(df, d, h, m, s):
    starttime = dt.datetime(2018, 11, d ,hour=h, minute=m)
    start = df.index.searchsorted(starttime)
    end = df.index.searchsorted(starttime+dt.timedelta(0,s))
    print(df.iloc[start-1:end+1])
    return start, end

# extrapolate an s second interval, linearly according to time
def extrapolate_hr(df, d, h, m, s):
    start, end = get_interval(df, d, h, m, s)

    df.iloc[start:end, df.columns.get_loc('HR')] = np.nan
    print(df.shape)
    df = df["HR"].interpolate(method = "time")
    print(df.iloc[start-1:end+1])
    return df.iloc[start:end]

def plot_data(hr_df):
    plt.figure()
    ax = hr_df.plot(y = 'HR')
    plt.show()

def main():
    hr_df = import_hr_file()
    print(hr_df.shape)

    extrapolate_hr(hr_df, 1, 20, 30, 10)

if __name__ == "__main__":
    main()