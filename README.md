# Build ETL pipeline from YFinance to Apache Kafka and Beam
The plan of this project is to get data from Yahoo Finance and send it to Apache Kafka. Then, we will use Apache Beam to process the data and send it to a database like Apache Spark for OLAP uses.
## Background
I've built a python package [yfinance-extended](https://pypi.org/project/yfinance-extended/) on top of [yfinance](https://pypi.org/project/yfinance/) by Ran Aroussi. The original `yfinance` package outputs multi-ticker data in a nested dataframe format, and did not have extensive support for pre/post-market data and/or simultaneous data retreival of multiple tickers.<br/>

With `yfinance-extended`, I hoped to handle those issues by downloading intra-day multi-ticker price/volume to a long-format dataframe, and make it possible to store those data in `parquet` format locally.<br/>

However, it might be more sensible to get the data into a pipeline, from `yfinance -> Apache Kafka -> Apache Beam -> Apache Spark`. So in this repo, I'll try to refactor and use Java SDKs of Kafka and Beam.
