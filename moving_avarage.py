import json
import numpy 
import matplotlib.pyplot as plt


def moving_average(array, window):
    return numpy.convolve(array, numpy.ones(window), 'valid') / window

symbol_list  = ["FLC","VNM"]
for symbol in symbol_list:
	with open('dat/'+symbol+'/' + symbol+'_five_year.json') as json_file:
		data = json.load(json_file)
		Open = numpy.array([float(i) for i in data["c"]])
		print(Open)
		moving_avarage_50 = moving_average(Open,50)
		moving_avarage_100 = moving_average(Open,100)

		moving_avarage_50.resize(Open.shape)
		moving_avarage_100.resize(Open.shape)
		print(moving_avarage_50.shape)
		print(moving_avarage_100.shape)
		print(Open.shape)
		plt.plot(moving_avarage_50)
		plt.plot(moving_avarage_100)
		plt.plot(Open)
		plt.show()


	
