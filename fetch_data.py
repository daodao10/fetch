#
# fetch data in the range
# can do it anytime
#
import threading
from Queue import Queue
import time
import sys, getopt
import dao_toolkit


class History(threading.Thread):
	def __init__(self, thread_name, queue):
		threading.Thread.__init__(self, name= thread_name)
		self.queue = queue

	def run(self):
		while True:
			data = self.queue.get()
			self.download_history(data['code'], data['start_day'], data['end_day'])
			self.queue.task_done()

	def download_history(self, code, start_day, end_day):
		try:
			filename = None
			if len(code) > 6: # for index
				if code == '0000001': # correct SH index symbol
					filename = '999999.csv'
			else:
				code = '%s%s' % (dao_toolkit.Helper.iif(str.startswith(code, '6'), '0', '1'), code)

			url = 'http://quotes.money.163.com/service/chddata.html?code={0}&start={1}&end={2}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;VOTURNOVER'\
			.format(code, start_day, end_day)

			dao_toolkit.Helper.download(url, filename)
		except Exception,e:
			print "download %s occurs error: [%s]" % (code, e)


def fetch_history(start_day, end_day):
	queue = Queue()

	if not end_day:
		end_day = dao_toolkit.Helper.format_date(time.gmtime())

	#get symbol data from file
	# codes = []
	try:
		f = file('symbols.txt','r')
		lines = f.readlines()
		f.close()
		for l in lines:
			c = l[0:6]
			if not start_day: 
				start_day = l[7:15]
				#print start_day
			if c == '999999' or c == '399001': # specially handle index, because index is handled differently from stock
				queue.put({'code': dao_toolkit.Helper.iif(c == '999999','0000001', '1399001'), 'start_day': start_day, 'end_day': end_day })
				continue
			queue.put({'code': c, 'start_day': start_day,'end_day': end_day })
		print 'has %d symbol(s)' % (len(lines))
	except Exception,e:
		print e
		sys.exit()

	print 'start to download'
	for i in range(10):
		consumer  = History('download.thread.' + str(i), queue)
		#consumer.daemon = True
		consumer.start()
		#consumer.join()
		
def main(argv):
	start_day = None
	end_day = None
	if argv and len(argv) > 0:
		try:
			opts, args = getopt.getopt(argv, "hs:e:")
		except getopt.GetoptError:
			print 'fetch_data [-s start_day] [-e end_day]'

		for opt, arg in opts:
			if opt == '-h':
				print 'fetch_data -s start_day -e end_day'
				print 'e.g.'
				print 'fetch_data -s 20130905 -e 20130907'
				print 'fetch_data -s start_day'
				print 'fetch_data -e end_day'
				sys.exit()
			elif opt == '-s':
				start_day = arg
			elif opt == '-e':
				end_day = arg

		print 'going to fetch data from [%s] to [%s]' % (start_day, end_day)

	else:
		print 'going to fetch data till today'

	fetch_history(start_day, end_day)

if __name__ == '__main__':
	main(sys.argv[1:])
