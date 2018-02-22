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

def get_back_trading_day(historical, index, scaler):
    op = float(historical[-index]["Open"])
    h = float(historical[-index]['High'])
    l = float(historical[-index]['Low'])
    v = float(historical[-index]['Volume'])
    ch = h-l
    ths = np.array((op, h, l, v))
    
    sc_ths = scale.scale(ths, scaler)
    #print index, ". ", historical[-index]['Date']
    return sc_ths


  
#predictions

bt = 10
clf = svm.SVR(gamma=0.001,C=0.01, kernel='linear')
print clf
#print historical[-10]["Date"]
predict = []
full = []
for i in range(bt):
    index = bt-i
    array = []
    _this_day = get_back_trading_day(historical, index, scaler)
    #print len(scaled_training[:-index])
    #print len(scaled_training[i:len(scaled_training)-index])
    _predict = clf.fit(scaled_training[i:len(scaled_training)-index], scaled_target[i:len(scaled_target)-index]).predict(_this_day)
    
    pre = scaler.inverse_transform(_predict)
    array.append(pre[0])
    Date = historical[-index]['Date']
    array.append(Date)
    Open = float(historical[-index]["Open"])
    array.append(Open)
    Close = float(historical[-index]["Adj_Close"])
    array.append(Close)
    #array = np.array((pre[0], Date, Open, Close))
    predict.append(pre)
    full.append(array)
    
plt.plot(x_axis[:bt], closing[-bt:], label='Actual Closing')
plt.plot(x_axis[:bt], predict, label='Predicted Closing')
plt.plot(x_axis[:bt], opening[-bt:], label='Opening')
plt.xlabel("Day")
plt.ylabel("Price ($)")
plt.legend(loc='best')
plt.title("The Coca Cola Co. (KO)\n Default Features")
#plt.text(0, 0, "C=0.1, gamma=0.001, kernel = linear")
plt.show()

#applying svm to the model
clf = svm.SVR(gamma=0.1,C=10000,kernel='rbf')
fit = clf.fit(scaled_training, scaled_target)
predict = fit.predict(scaled_training)             
predict = scaler.inverse_transform(predict)

#plotting the graph
x_axis = np.arange(0+1, len(historical)+1)
plt.scatter(x_axis, opening, c='g', label='Opening')
plt.scatter(x_axis, closing, c='r', label='Closing')
plt.scatter(x_axis, high, c='b', label='High')
plt.scatter(x_axis, low, c='y', label='Low')
plt.legend(loc='best')
plt.xlabel('Days')
plt.xlim(0, )
plt.ylabel('Price ($)')
plt.title("Regression for stock price data")
plt.plot(x_axis, predict, c ='b', label = 'Predicted Closing')
plt.show()
