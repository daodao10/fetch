#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys
import codecs

from tool import dao_toolkit

def parse_data_row(code, name):
    try:
        with codecs.open(get_output_file(code), mode='w') as w:
            with codecs.open(os.path.join('data', code + '.csv'), mode='r') as r:
                lines = r.readlines()
                firstline = True
                for l in lines:
                    if firstline:
                        firstline = False
                        # style 1:
                        #<DTYYYYMMDD>,<TICKER>,<NAME>,<CLOSE>,<HIGH>,<LOW>,<OPEN>,<VOL>
                        # w.write(dao_toolkit.MetastockHelper.FILE_HEADER)
                        # style 2:
                        w.write(dao_toolkit.MetastockHelper.FILE_HEADER2)
                        continue
                    row = str.split(l, ',')
                    #date,ticker,name,close,high,low,open,previous close,vol(lots),change,chg %, turnover
                    row[0] = row[0].replace('-','')
                    row[1] = code
                    row[2] = name
                    del row[7] # delete previous close
                    #print row
                    w.write(','.join(row))
    except Exception,e:
        print 'parse [%s] occurs error: %s' % (code, e)

def patch_non_trading_day_data(code):
    r = codecs.open(get_output_file(code), mode='r')
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

    w = codecs.open(get_output_file(code), mode='w')
    w.writelines(lines)

def get_output_file(code):
    return 'output/' + code + '.txt'

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
            name = splits[2][:-1]# pay attention to the difference of line-feed between linus/unix & windows
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