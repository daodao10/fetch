# Fetch

##Fetch &amp; Generate stock data of China Market for Metastock

1. get today's market daily data after market closed: 

	```bash
	python fetch_today_data.py
	```

2. get market daily data in period:

	```bash
	python fetch_data.py [-s {start_date}] [-e {end_date}]
    python format_data.py
	```
	
##NOTE:

1. date format: yyyyMMdd

 >in generally, use it when use this tool first time or when you forget to get data after market closed

2. different data source

 >- retrieve today's data form <http://quotes.money.163.com/hs/service/diyrank.php>

 >- retrieve historical data from <http://quotes.money.163.com/service/chddata.html>
