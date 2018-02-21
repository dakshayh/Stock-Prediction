import numpy as np
import normalize as scale

'''
historical- list of historical prices and Volumes
opening- list of daily opening prices from the historical data

function to get historical data raw format
'''

def get_unscaled_opening(historical):

    opening = [] 
    
    for i in range(len(historical)):
        x = float(historical[i]['Open'])
        opening.append(x)        
    return opening

'''

historical - list containing historical prices, and volumes
opening, scaled_opening - list containing daily opening prices from the historical data
scaler-returns scaled opening stock

function to get historical data in scaled format
'''

def get_historical_opening(historical, scaler):

    opening = [] 
    
    for i in range(len(historical)):
        x = float(historical[i]['Open'])
        opening.append(x)

    scaled_opening = scale.scale(opening, scaler)
        
    return opening, scaled_opening

'''
historical - list containing historical prices, and volumes
days_high - list containing daily high prices from the historical data
scaler-returns scaled opening stock

function to return scaled high price for a particular day
'''

def get_historical_high(historical, scaler):

    days_high = []

    for i in range(len(historical)):
        x = float(historical[i]['High'])
        days_high.append(x)

    scaled_high = scale.scale(days_high, scaler)
        
    return days_high, scaled_high

'''
historical - list containing historical prices, and volumes
days_low - list containing daily low prices from the historical data
scaler-returns scaled opening stock

function to return low price of the day in scaled format
'''

def get_historical_low(historical, scaler):
    days_low = [] 

    for i in range(len(historical)):
        x = float(historical[i]['Low'])
        days_low.append(x)

    scaled_low = scale.scale(days_low, scaler)
        
    return days_low, scaled_low


'''
historical - list containing historical prices, and volumes
closing - list containing daily closing prices from the historical data
scaler-returns scaled opening stock

function to get closing prices in raw and scaled format
'''

def get_historical_closing(historical, scaler):

    closing = [] 
    
    for i in range(len(historical)):
        x = float(historical[i]['Adj_Close'])
        closing.append(x)
        
    scaled_closing = scale.scale(closing, scaler)

    return closing, scaled_closing


'''
historical - list containing historical prices, and volumes
company - Share object
historical_volume - list containing daily volume from the historical data
average_volume - list containing average volume for the sample data

function to get historical and average volumes in scaled and raw format
'''
def get_historical_volume(historical, company, scaler):
    historical_volume = [] #is a dynamic array (list) for python
    average_volume = []

    for i in range(len(historical)):
        x = float(historical[i]['Volume'])
        historical_volume.append(x)
        average_volume.append(float(company.get_avg_daily_volume()))

    scaled_historical_volume = scale.scale(historical_volume, scaler)

    scaled_average_volume = scale.scale(average_volume, scaler)

    return historical_volume, average_volume, scaled_historical_volume, scaled_average_volume

'''
historical - list containing historical prices, and volumes
change - price change for the day
scaled_change - price change scaled for -1 to 1

function to get change in price and scaled change in price
'''
def get_change(historical, scaler):
        change = []
        change.append(0)
        for i in range(len(historical)-1):
            x = float(historical[i+1]["Close"]) - float(historical[i]['Close'])
            change.append(x)
        scaled_change = scale.scale(change, scaler)

        return change, scaled_change


'''
Method to stack training data together including opening , volume , high, low average volume 
training data - consists of the all variables
target-closing

useSpread-boolean to find change
useVolume-boolean to use volume
data - training data
closing - target data
'''
def training_data(historical, company, scaler, useSpread, useVolume):

	historical_opening, scaled_opening = get_historical_opening(historical, scaler)
	historical_closing, scaled_closing = get_historical_closing(historical, scaler)
	historical_high, scaled_high = get_historical_high(historical, scaler)
	historical_low, scaled_low = get_historical_low(historical, scaler)
	historical_volume, average_volume, scaled_volume, scaled_avg_vol = get_historical_volume(historical, company, scaler)
        change, scaled_change = get_change(historical, scaler)

	opening =  np.array(historical_opening)
	_scaled_opening =  np.array(scaled_opening)

	volume = np.array(historical_volume)
	_scaled_volume = np.array(scaled_volume)

	high = np.array(historical_high)
	_scaled_high = np.array(scaled_high)

	low = np.array(historical_low)
	_scaled_low = np.array(scaled_low)

	avg_vol = np.array(average_volume)
	_scaled_avg_vol = np.array(scaled_avg_vol)

	closing = np.array(historical_closing)
	_scaled_closing = np.array(scaled_closing)

        _change = np.array(change)
        _scaled_change = np.array(scaled_change)
	
	if useSpread is False and useVolume is False:
		data = np.vstack((opening, high, low))
		scaled_data = np.vstack((_scaled_opening, _scaled_high, _scaled_low))
	elif useSpread is True and useVolume is False:
		data = np.vstack((opening, high, low, _change))
		scaled_data = np.vstack((_scaled_opening, _scaled_high, _scaled_low, _scaled_change))
	elif useSpread is False and useVolume is True:
		data = np.vstack((opening, high, low, volume))
		scaled_data = np.vstack((_scaled_opening, _scaled_high, _scaled_low, _scaled_volume))
	else:
		data = np.vstack((opening, high, low, _change, volume))
		scaled_data = np.vstack((_scaled_opening, _scaled_high, _scaled_low, _scaled_change, _scaled_volume))
	

	shape1, shape2 = data.shape
	data = data.reshape(shape2, shape1)

	shape1, shape2 = scaled_data.shape
	scaled_data = scaled_data.reshape(shape2, shape1)

return data, closing, scaled_data, _scaled_closing
