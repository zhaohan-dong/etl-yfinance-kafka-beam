# Build ETL pipeline from YFinance to Apache Kafka and Beam
The plan of this project is to get data from Yahoo Finance and send it to Apache Kafka. Then, we will use Apache Beam to process the data and send it to a database like Apache Spark for OLAP uses.
## Background
I've built a python package [yfinance-extended](https://pypi.org/project/yfinance-extended/) on top of [yfinance](https://pypi.org/project/yfinance/) by Ran Aroussi. The original `yfinance` package outputs multi-ticker data in a nested dataframe format, and did not have extensive support for pre/post-market data and/or simultaneous data retreival of multiple tickers.<br/>

With `yfinance-extended`, I hoped to handle those issues by downloading intra-day multi-ticker price/volume to a long-format dataframe, and make it possible to store those data in `parquet` format locally.<br/>

However, it might be more sensible to get the data into a pipeline, as we can let Apache Beam and Spark handle the data transformation and storage.<br/>

Here are two directions it could go:<br/>
- `yfinance-extended` -> parquet files -> Apache Spark (which is already here, but the transformation step is performed by `pandas` in Python); or,
- `yfinance` -> Apache Kafka -> Apache Beam -> Apache Spark.

With the first approach, we can run a daily cron job to get the data into parquet files, and then run a Spark job to transform the data and store it in HDFS.<br/>

With the second approach, we can get the data into Kafka, and then use Beam to transform the data and send it to Spark for storage. The second approach is more scalable, and we can also use Beam to send the data to other databases like BigQuery or Cassandra.<br/>

## Structure
This repo is structured as follows at the moment:
```
|-- README.md
|-- python-yfiance-extended/ (What we're refactoring)
 -- kafka/ (Kafka Producer to get yfinance data into streaming messages)
```
We'll add `beam` and `spark` folders later.
