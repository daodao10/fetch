#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
import codecs
import dao_toolkit

def parse_data_row(code, name):
	try:
		with codecs.open(code + '.txt', mode='w') as w:
			with codecs.open(os.path.join('data', code + '.csv'), mode='r') as r:
				lines = r.readlines()
				firstline = True
				for l in lines:
					if firstline:
						firstline = False
						w.write(dao_toolkit.MetastockHelper.FILE_HEADER) #<DTYYYYMMDD>,<TICKER>,<NAME>,<CLOSE>,<HIGH>,<LOW>,<OPEN>,<VOL>
						continue
					row = str.split(l, ',')
					#date,ticker,name,close,high,low,open,previous close,change,vol(lots)
					row[0] = row[0].replace('-','')
					row[1] = code
					row[2] = name
					del row[7:9] # delete previous close & change
					#print row
					w.write(','.join(row))
	except Exception,e:
		print 'parse [%s] occurs error: %s' % (code, e)

def patch_non_trading_day_data(code):
	r = codecs.open(code + '.txt', mode='r')
	lines = r.readlines()
	r.close()

	for i in range(len(lines)-1, 0, -1):
		row = str.split(lines[i], ',')
		if row[3] == '0.0': # close == 0: today is non-trading day, 2 way to handle it
			# #1)get the previous day's close price
			# pre_row = str.split(lines[i+1], ',')
			# row[3] = pre_row[3]
			# row[4] = pre_row[3]
			# row[5] = pre_row[3]
			# row[6] = pre_row[3]
			# lines[i] = ','.join(row)
			#2)remove this day's data
			del lines[i]

	w = codecs.open(code + '.txt', mode='w')
	w.writelines(lines)


def main():
	i=0
	try:
		f=codecs.open('symbols.txt',mode='r')
		lines=f.readlines()
		for l in lines:
			# cannot work well for unicode string
			#code = l[0:6]
			#name = l[8:-1]
			splits = str.split(l,',')
			code = splits[0]
			name = splits[2][:-2]
			parse_data_row(code, name)
			patch_non_trading_day_data(code)
			i += 1
		f.close()
	except Exception,e:
		print e
		sys.exit()
	print 'total symbols: %d' % (i)

if __name__ == '__main__':
	main()