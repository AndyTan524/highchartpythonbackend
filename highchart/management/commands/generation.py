from django.core.management import BaseCommand
import tushare as ts
import os
import json

#!/usr/bin/env python
# coding=utf-8

# import matplotlib.pyplot as plt

# from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
# from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc,candlestick2_ochl,candlestick2_ohlc
import tushare as ts
import os

# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

# ticker = '600848'

# date1 = '2018-02-01'
# date2 = '2018-02-15'

def plo(filename,open, low, high, close):
	mondays = WeekdayLocator(MONDAY)           
	alldays = DayLocator()                      
	#weekFormatter = DateFormatter('%b %d')     
	mondayFormatter = DateFormatter('%m-%d-%Y') 
	dayFormatter = DateFormatter('%d')          

	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)

	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(mondayFormatter)

	candlestick2_ochl(ax, opens=open, lows=low, highs=high, closes=close, width=0.2, colorup='g', colordown='r', alpha=1)

	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

	ax.grid(False)
	plt.title(filename)
	#plt.show()

	fig.savefig(filename)
	plt.close('all')

def save_to_image(mode, quotes, period, company_name):
	print(len(quotes))
	if len(quotes) == 0:
		return
	for i in range(0, len(quotes['open'])/mode):
		open_mode = quotes['open'][i*mode: (i+1)*mode]
		close_mode = quotes['close'][i*mode: (i+1)*mode]
		high_mode = quotes['high'][i*mode: (i+1)*mode]
		low_mode = quotes['low'][i*mode: (i+1)*mode]

		image_path = './image/' + company_name + '/' + period + '/' + str(mode)
		
		if not os.path.exists(image_path):
			os.makedirs(image_path)

		filename =  str(i)
		# filename = 'quotes_'+quotes['date'][i*mode]
		# filename = filename.replace(' ','-')
		# filename = filename.replace(':','-')

		real_filename = image_path + '/' +  filename + '.svg'
		plo(real_filename, open_mode, low_mode, high_mode, close_mode)		

class Command(BaseCommand):
    """ 
    Handling JSON
    """
    def handle(self, *args, **options):
        # with open("1.json", 'wb') as output:
        #     jsoncontent = {
        #         "key1" : 'value1',
        #         "key2" : "value2"
        #     }
        #     json.dump(jsoncontent, output)
        # print("1")
        name_code = ts.get_industry_classified()
        date1 = '2018-02-01'
        date2 = '2018-02-15'
        name = name_code['name']
        code = name_code['code']

        
        periods = ['W', 'D', '60', '15']
        for ii in range(0, len(name_code)):
            jsoncontent = {}
            print(name[ii])
            basepath = './media/' + name[ii]
            if not os.path.exists(basepath):
                os.makedirs(basepath)
        
            with open(basepath+"/1.json", 'wb') as output:
                for period in periods:
                    jsoncontent[period] = {}
                    jsonarray = []
                    quotes = ts.get_hist_data(code[ii] ,start=date1, end=date2, ktype=period)
                    for idate in quotes.index:
                        print(idate, quotes['open'][idate])
                        temparray = []
                        temparray.append(idate)
                        temparray.append(quotes['open'][idate])
                        temparray.append(quotes['close'][idate])
                        temparray.append(quotes['low'][idate])
                        temparray.append(quotes['high'][idate])
                        jsonarray.append(temparray)
                    jsoncontent[period] = jsonarray
                json.dump(jsoncontent, output)
    # def handle(self, *args, **options):
    #     name_code = ts.get_industry_classified()
    #     name = name_code['name']
    #     code = name_code['code']

    #     periods = ['W', 'D', '60', '15']
    #     for ii in range(0, len(name)):
    #         print(name[ii])
    #         for period in periods:
    #             quotes = ts.get_hist_data(code[ii] ,start=date1, end=date2, ktype=period)
    #             if quotes is None or len(quotes) == 0:
    #                 continue
    #             for i in range(1, 6):
    #                 save_to_image(i, quotes, period, name[ii])
