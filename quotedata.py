from json import loads
from datetime import datetime
from urllib.request import urlopen
from sys import exit
from os.path import isfile

# get historical ticker price (time series data)

symbols = input("Please enter your symbol or list of comma-delimited symbols:").upper() #eg. SCTY,TSLA,AAPL

user_ticker_list = list(set(symbols.replace (' ', '').split(',')))

ticker_list = [x for x in user_ticker_list if x != '']

if not ticker_list:
	print("Nothing to run. Aborting...")
	exit(-1)

print("\nRunning...press [^C] or equivalent to cancel\n")

stock_ts = {}
ts = []

for ticker in ticker_list:
	url = "https://www.google.com/async/finance_chart_data?async=q:{},x:{},p:3M,i:60,_fmt:json".format(ticker,'NASDAQ')

	if not loads(loads(urlopen(url).readlines()[1].decode('utf-8'))["tnv"]["value"])["t"]:
		url = "https://www.google.com/async/finance_chart_data?async=q:{},x:{},p:3M,i:60,_fmt:json".format(ticker, 'NYSE')	
		if not loads(loads(urlopen(url).readlines()[1].decode('utf-8'))["tnv"]["value"])["t"]:
			print("Stock symbol", ticker, "doesn't exist in NASDAQ or NYSE. Skipping...")
			continue

	with urlopen(url) as response:
		#2nd line in file is a dictionary
		price_info = loads(response.readlines()[1].decode('utf-8'))["tnv"]["value"] #list of dates

		ts = list(zip( list(map(lambda x: x.replace('T',' ').replace('Z',''), loads(price_info)["t"]))  ,   loads(price_info)["v"][0] ) ) 

		stock_ts[loads(price_info)["n"][0]] = ts

header_exists = True

# create header if file doesn't exist
if not isfile("quotedata.tsv"): #make sure path is correct
	header_exists = False
	header = "symbol\tprice\tdatetime\n"

# write to file
with open("quotedata.tsv", "a") as sq:
	if not header_exists:
		sq.write(header)
	for symbol,val in stock_ts.items():
		print("Writing to file for",symbol)
		for v in val:
			sq.write("{}\t{}\t{}\n".format(symbol,v[1],v[0]))
