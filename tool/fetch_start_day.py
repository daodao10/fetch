# 
# this file is for fetching the start day of the stock
# after fetch start day store it to the symbol file
# in generally, run it when you use fetch_data first time
#
import bs4,lxml
import urllib2
import dao_toolkit
import thread
import time


mylock = thread.allocate_lock()
rows = []
handled = 0

class SymbolData():
	def __init__(self, symbolfile):
		self.symbolfile = symbolfile

	def _get_date(self, code):
		try:
			request = urllib2.Request('http://quotes.money.163.com/trade/lsjysj_{0}.html'.format(code))
			content = urllib2.urlopen(request).read()
			soup = bs4.BeautifulSoup(content,'lxml')
			start_day = self._get_values_by_name(soup,'date_start_type')[1]
			return dao_toolkit.Helper.format_date_string(start_day)

		except Exception,e:
			print '%s(%s) occurs error: [%s]' % ('get_date',code, e)
			return None

	def _get_values_by_name(self,soup, name):
		if isinstance(soup, bs4.BeautifulSoup):
			return map(lambda x: x['value'], soup.find_all('input', {'name': name}))
		else:
			return None

	def run(self, lines):
		global handled
		global mylock
		local_rows = []
		for l in lines:
			cells = str.split(l, ',')
			if cells[0] == '999999' or cells[0] == '399001': # specially handle index, because index is handled differently from stock
				if cells[0] == '999999': 
					cells.insert(1, '19901219')
				else:
					cells.insert(1, '19910403')
			else:
				# get start day from 163 quotes
				start_day = self._get_date(cells[0])
				if start_day:
					cells.insert(1, start_day)
				else:
					print 'failed to fetch the start day for [%s]' % (cells[0])

			print 'done for [%s]' % (cells[0])
			local_rows.append(','.join(cells))

		mylock.acquire()
		handled += len(lines)
		rows.extend(local_rows) # append list to list
		mylock.release()

	def fetch(self):
		global handled
		global rows
		try:
			f = file(self.symbolfile,'r')
			lines = f.readlines()
			f.close()

			print 'start to fetch data from 163'

			total = len(lines)
			thread_no = 20
			handle_no_per_thread = total / thread_no
			if handle_no_per_thread < 1:
				handle_no_per_thread = 1

			for i in range(thread_no):
				start_index = i * handle_no_per_thread
				if start_index > total:
					break
				if i == thread_no - 1:
					end_index = total
				else:
					end_index = start_index + handle_no_per_thread

				thread.start_new_thread(self.run, (lines[start_index:end_index],))

			while total > handled:
				time.sleep(10)

			print 'start to write to file'
			f = file(self.symbolfile, 'w')
			f.writelines(rows)
			f.close()

			print 'has %d symbol(s), handled %d' % (total, handled)
		except Exception,e:
			print e


def main():
	SymbolData('symbols.txt').fetch()

if __name__ == '__main__':
	main()
