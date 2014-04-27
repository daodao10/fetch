# Fetch
---

#### Fetch &amp; Generate stock data of China Market for Metastock

1. get today's market daily data after market closed: 

	```
	python fetch_today_data.py
	```

2. get market daily data in period:

	```
	python fetch_data.py [-s {start_date}] [-e {end_date}]
	```
	
	NOTE:
	date format: yyyyMMdd

	in generally, use it when use this tool first time or when you forget to get data after market closed

