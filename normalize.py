from sklearn import preprocessing
import numpy as np

def get_scaler(opening):
	min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
	min_max_scaler.fit(opening)
	return min_max_scaler
	
def scale(data, scaler):
	data_train = scaler.transform(data)
	return data_train


def scale_today(data, scaler):	
	
	data_train = scaler.transform(data)
	return data_train, min_max_scaler
