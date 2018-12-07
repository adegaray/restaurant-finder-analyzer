# -*- coding: utf-8 -*-
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd


class AnalyzeRestaurantItem(object):

	db_name = 'restaurantinfo'
	fields = ['rest_name', 'rest_addr', 'lat', 'lon', 'rest_location', 'rest_rating', \
				'rest_pos_count', 'rest_neg_count', 'rest_total_reviews', \
				'rest_price', 'rest_cuisines', 'rest_features', 'rest_meals']
	df = None

	def __init__(self):

		#Setup Client for MongoDB
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]


	def convert_addr_to_coord(self, addr):
		
		geolocator = Nominatim()
		location = geolocator.geocode(addr, timeout=3)
		if location:
			return location.latitude, location.longitude
		else:
			return 0,0

	def load_mongodb_to_pandas(self):

		rest_info = []
		for doc in self.db.restaurantreviews.find():
			lat, lon = self.convert_addr_to_coord(doc['rest_addr'])	
			if (lat != 0 and lon != 0):
				rest_info.append([doc['rest_name'], doc['rest_addr'], float(lat), float(lon), \
								doc['rest_location'], doc['rest_rating'], doc['rest_pos_count'], \
								doc['rest_neg_count'], doc['rest_total_reviews'], doc['rest_price'], \
								doc['rest_cuisines'], doc['rest_features'], doc['rest_meals']])
		self.df = pd.DataFrame(rest_info, columns=self.fields)
		print(self.df)	

if __name__ == '__main__':
	analyze = AnalyzeRestaurantItem()
	analyze.load_mongodb_to_pandas()
	
