
import requests
import datetime
import json
import os

class URL_BUILDER:
	def __init__ (self, symbol = "VNM", start_time = datetime.datetime.today() - datetime.timedelta(days = 1), end_time = datetime.datetime.today()):
		self.symbol = symbol
		self.start_time = str(datetime.datetime.timestamp(start_time))
		self.end_time = str(datetime.datetime.timestamp(end_time))
		self.base_url = 'https://iboard.ssi.com.vn/dchart/api/history?resolution=D&symbol=%s&from=%s&to=%s&fbclid=IwAR2kvqdF2LNLFwtmGsgut8QlniwyrUOV6KnCMqMCm1yHuxsvfzFmkHRTj84'
	
	def set_start_time(self, start_time):
		self.start_time = str(datetime.datetime.timestamp(start_time))
	
	def set_end_time (self, end_time):
		self.end_time = str(datetime.datetime.timestamp(end_time))
	
	def get_URL(self):
		return self.base_url % (self.symbol, self.start_time, self.end_time)

class STONK_HOADER:
	def __init__ (self, symbol = "VNM"):
		self.symbol = symbol
		self.time_interval = {
			"yesterday" : datetime.timedelta(days = 1), 
			"last_month": datetime.timedelta(days = 30),
			"last_year" : datetime.timedelta(days = 365),
			"five_year" : datetime.timedelta(days = 365*5)
			}
		self.log_path = 'dat/' + self.symbol + "/"
		self.url_builder = URL_BUILDER(symbol=self.symbol)
	
	def collecting(self):
		for interval in self.time_interval.keys():
			start_time = datetime.datetime.now() - self.time_interval[interval] 
			self.url_builder.set_start_time(start_time)
			r = requests.get(self.url_builder.get_URL())
			json_return = r.json()
			f = open( self.log_path + self.symbol+"_"+interval+".json", "w")
			f.write(json.dumps(json_return))
			f.close()


	def get_URL(self):
		return self.base_url % (self.symbol, self.start_time, self.end_time)


if __name__ == '__main__':
	try:
		os.mkdir('dat')
	except FileExistsError:	
		print("Directory " , 'dat' ,  " already exists")

	symbol_list = ['VNM', 'BHT', 'FLC', 'SSI', 'CTD', 'HBC']

	for symbol in symbol_list:
		try:
			os.mkdir('dat/' + symbol)
		except FileExistsError:
			print("Directory " , 'dat/' + symbol,  " already exists")

		S = STONK_HOADER(symbol)
		S.collecting()