#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import time, re

class MetastockHelper:
    FILE_HEADER = '<DTYYYYMMDD>,<TICKER>,<NAME>,<CLOSE>,<HIGH>,<LOW>,<OPEN>,<VOL>\r\n'
    FILE_HEADER2 = '<DTYYYYMMDD>,<TICKER>,<NAME>,<CLOSE>,<HIGH>,<LOW>,<OPEN>,<VOL>,<CHG>,<PCT>,<TURNOVER>\r\n'


class Helper:
    @staticmethod
    # format date string 
    # by default from %Y-%m-%d to %Y%m%d
    def format_date_string(str_date, src_style = '%Y-%m-%d', dest_style = '%Y%m%d'):
        return time.strftime(dest_style, time.strptime(str_date, src_style))

    @staticmethod
    def format_date(d):
        return time.strftime('%Y%m%d', d)

    @staticmethod
    def iif(condition, true_part, false_part):
        if condition:
            return true_part
        else:
            return false_part
        #return (condition and true_part or false_part)[0]

    @staticmethod
    def download(url, filename):
        response = urllib2.urlopen(url)
        
        meta = response.info()
        #print meta
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all

        # get file name
        if not filename:
            # get from header
            meta_disposition = meta_func('Content-Disposition')
            if meta_disposition:            
                m = re.search(r'(?<=filename=).+', meta_disposition[0])
                if m:
                    filename = m.group()

            # get from url part
            if not filename:
                scheme, domain, path, query, fragment = urlparse.urlsplit(url)
                filename = os.path.basename(path)
                # set default file name
                if not filename:
                    filename = 'download.file'
            #print 'file name: ' + filename

        # get file size
        file_size = None
        meta_length = meta_func('Content-Length')
        if meta_length and meta_length[0]:
            file_size = int(meta_length[0])

        with open(filename, 'wb') as f:
            read_size = 0
            block_size = 8192
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                
                f.write(buffer)

                # show status
                if file_size:
                    read_size += len(buffer)
                    status = '{0} [{1:6.2f}%]'.format(filename, read_size * 100 / file_size)
                    print status
