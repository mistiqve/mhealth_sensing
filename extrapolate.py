import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_folder = ""
hr_file = data_folder + "Smartwatch_HeartRateDatum.csv"
acc_file = data_folder + "Sensus_Accelerometer.csv"
loc_file = data_folder + "Sensus_Location.csv"

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
    return

if __name__ == "__main__":
    main()