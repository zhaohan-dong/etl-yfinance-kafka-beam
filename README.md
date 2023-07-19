# Build ETL pipeline from YFinance to Apache Kafka and Beam
The plan of this project is to get data from Yahoo Finance and send it to Apache Kafka. Then, we will use Apache Beam to process the data and send it to a database like Apache Spark for OLAP uses.
## Background
I've built a python package [yfinance-extended](https://pypi.org/project/yfinance-extended/) on top of [yfinance](https://pypi.org/project/yfinance/) by Ran Aroussi. The original `yfinance` package outputs multi-ticker data in a nested dataframe format, and did not have extensive support for pre/post-market data and/or simultaneous data retreival of multiple tickers.<br/>

With `yfinance-extended`, I hoped to handle those issues by downloading intra-day multi-ticker price/volume to a long-format dataframe, and make it possible to store those data in `parquet` format locally.<br/>

However, it might be more sensible to get the data into a pipeline, as we can let Apache Beam and Spark handle the data transformation and storage.<br/>
## Planning
Here are two directions it could go:<br/>
~~1. `yfinance-extended` -> parquet files -> Apache Spark (Need to refactor [yfinance-extended](https://github.com/zhaohan-dong/yfinance-extended) to use Spark DataFrame as soon as the data is downloaded using yfinance); or,~~
2. `yfinance` -> Apache Kafka -> Apache Beam -> Apache Spark.

~~With the first approach, we can run a daily cron job to get the data into parquet files, and then run a Spark job to transform the data and store it in HDFS.<br/>~~

With the second approach, we can get the data into Kafka, and then use Beam to transform the data and send it to Spark for storage. The second approach is more scalable, and we can also use Beam to send the data to other databases like BigQuery or Cassandra.<br/>

Because Spark gets data in `Row`, the first approach would need to download and transform the pandas dataframe with all the tickers available into Spark DataFrame. It'll be bottle-necked by the serial downloading of data.<br/>

|                | `yfinance-extended` pandas | `yfinance-extended` with Spark | `yfinance` to Kafka and Beam |
|----------------|:--------------------------:|:------------------------------:|:----------------------------:|
| Implementation |          Easiest           |             Harder             |           Hardest            |
| Faster with    |      Low data volume       |       Higher data volume       |       High data volume       |

**Apparently the `yfinance-extended` with Spark is the worst choice among all three**

## Structure
This repo is structured as follows at the moment:
```
|-- README.md
|-- python-yfiance-extended/ (What we're refactoring)
 -- yfinance_to_kafka/ (Kafka Producer to get yfinance data into streaming messages)
```
Steps:
Producing
