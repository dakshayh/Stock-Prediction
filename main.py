from yahoo_finance import Share
from matplotlib import pyplot as plt
import numpy as np
import get_historical as gh
from datetime import date as dt
from datetime import timedelta
import normalize as scale
import trading_day as td
from sklearn import svm

ticker = raw_input("Enter company ticker: ")
num_days = int(input("Enter number of days: "))
company = Share(ticker)
day1, day2 = get_dates(num_days)
historical = company.get_historical(day1, day2)
historical.reverse()
print len(historical)

#fetching training data

opening = gh.get_unscaled_opening(historical)
scaler = scale.get_scaler(opening)
opening, scaled_opening = gh.get_historical_opening(historical, scaler)
closing, scaled_closing = gh.get_historical_closing(historical, scaler)
high, scaled_high = gh.get_historical_high(historical, scaler)
low, scaled_low = gh.get_historical_low(historical, scaler)
change, scaled_change = gh.get_change(historical, scaler)
volume, avg_vol, scaled_volume, scaled_avg_vol = gh.get_historical_volume(historical, company, scaler)
average_volume = avg_vol[0]
