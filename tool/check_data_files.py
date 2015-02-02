#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sys

def data_file_check(code):
    #print os.path.join('data', code + '.csv')
    return os.path.exists(os.path.join('../data', code + '.csv'))

i=0
try:
    f=file('../symbols.txt','r')
    lines=f.readlines()
    for l in lines:
        code = l[0:6]
        if not data_file_check(code):
            print '%s is not ready' % (code)
        i += 1
    f.close()
except Exception,e:
    print e
    sys.exit()
print 'total symbols: %d' % (i)