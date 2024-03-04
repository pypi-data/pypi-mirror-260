# TPCDS PySpark
Tools for your Apache Spark Performance Lab.

TPCDS_PySpark is a TPC-DS workload generator written in Python and designed to run at scale using Apache Spark.  
A key feature of this tool is that it collects and reports performance metrics by integrating [sparkMeasure](https://github.com/LucaCanali/sparkMeasure),
a performance monitoring library for Apache Spark.  

## Motivations and goals
- Provide tooling for a Spark performance lab 
  - Run TPC-DS workloads at scale and study Spark performance
  - Learn about collecting and analyzing Spark performance data, including timing and metrics measurements
  - Learn about Spark performance and optimization
- Compare performance across different Spark configurations and system configurations

Author and contact: Luca.Canali@cern.ch - Feb 2024
[TPCDS-PySpark on Pypi](https://pypi.org/project/TPCDS_PySpark)

### Key Features

- **Comprehensive Benchmarking:** Execute the full suite of TPC-DS queries, in local mode ot against your Spark cluster,
providing standardized metrics for comparing configurations, hardware, or deployment strategies.  
- **Learning Lab:** A practical environment to experiment with Spark concepts,
notably with the [Spark task metrics](https://spark.apache.org/docs/latest/monitoring.html#executor-task-metrics) and by using the integrated [sparkMeasure](https://github.com/LucaCanali/sparkMeasure) library to gather fine-grained performance metrics
(execution time, task metrics, etc.).  
Use this together with instrumentation as: the [Spark Web UI](https://spark.apache.org/docs/latest/web-ui.html) and the [Spark-Dashboard](https://github.com/cerndb/spark-dashboard)  view of performance.

### Real-World Applications

- **Capacity Planning:** Evaluate how new hardware or Spark versions will perform before making changes in production.
- **Configuration Tuning:** Identify optimal Spark configurations (executor memory, parallelism, etc.) for your specific dataset and workload characteristics.
- **Bottleneck Detection:** Uncover inefficiencies within SQL queries or the Spark execution plans, and code optimizations in general.
- **Skill Development:** Deepen your understanding of Spark internals and best practices for high-performance distributed computing.


## Getting started
You can start using TPCDS_PySpark by running the tool as a standalone Python script, from the command line, or by using the TPCDS class to run TPCDS workloads from your Python code.
The tool runs also on notebooks, for example Colab.

1. **Get started Python script:** [getstarted.py](Labs/getstarted.py)
2. **Get started Notebooks:**  
[<img src="https://raw.githubusercontent.com/googlecolab/open_in_colab/master/images/icon128.png" height="50"> TPCDS_PySpark get-started on Colab](https://colab.research.google.com/github/LucaCanali/Miscellaneous/blob/master/Performance_Testing/TPCDS_PySpark/Labs/TPCDS_PySpark_getstarted.ipynb)  
[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/250px-Jupyter_logo.svg.png" height="50"> TPCDS_PySpark get-started](Labs/TPCDS_PySpark_getstarted.ipynb)


**Command line:**
```
# Get the tool
# pip install tpcds_pyspark 

# Download the test data
wget https://sparkdltrigger.web.cern.ch/sparkdltrigger/TPCDS/tpcds_10.zip
unzip -q tpcds_10.zip

# 1. Run the tool for a minimal test
tpcds_pyspark_run.py -d tpcds_10 -n 1 -r 1 --queries q1,q2

# 2. run all queries with default options
./tpcds_pyspark_run.py -d tpcds_10 

# 3. run all queries on a YARN cluster and save the metrics to a file
TPCDS_PYSPARK=`which tpcds_pyspark_run.py`
spark-submit --master yarn --conf spark.log.level=error  --conf spark.executor.cores=8 \
             --conf spark.executor.memory=32g --conf spark.driver.memory=4g \
             --conf spark.driver.extraClassPath=tpcds_pyspark/spark-measure_2.12-0.23.jar \ 
             --conf spark.dynamicAllocation.enabled=false --conf spark.executor.instances=4 \
              $TPCDS_PYSPARK -d <HDFS_PATH>/tpcds_10 -o ./tpcds_10_out.cvs

# 4. Scale up..
wget https://sparkdltrigger.web.cern.ch/sparkdltrigger/TPCDS/tpcds_100.zip
```
** API mode:**
```
# Get the tool
# pip install tpcds_pyspark 

# Download the test data
wget https://sparkdltrigger.web.cern.ch/sparkdltrigger/TPCDS/tpcds_10.zip
unzip -q tpcds_10.zip

from tpcds_pyspark import TPCDS

tpcds = TPCDS(num_runs=1, queries_repeat_times=1, queries=['q1','q2'])
tpcds.map_tables()

tpcds.run_TPCDS()
tpcds.print_test_results()
```

## Spark Performance Labs with TPCDS_PySpark 

3. **TPCDS at scale 10000 G and analysis:**
  - [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/250px-Jupyter_logo.svg.png" height="50"> TPCDS performance metrics analysis](Labs/TPCDS_analysis_10000.ipynb)

---
## Installation:
A few steps to set up your Python environment for testing with TPCDS_PySpark:
```
python3 -m venv tpcds
source tpcds/bin/activate

pip install tpcds_pyspark
pip install pyspark
pip install sparkmeasure
pip install pandas
```


## One tool, two modes of operation:
- **Script mode**: run the tool as a standalone Python script, from the command line. Example:
  - `./tpcds_pyspark_run.py`
- **API mode:** use the tool as a library from your Python code.

### 1.How to run TPCDS PySpark as a standalone script:
```
tpcds_pyspark_run.py --help

options:
  -h, --help            show this help message and exit
  --data_path DATA_PATH, -d DATA_PATH
                        Path to the data folder with TPCDS data used for testing. Default: tpcds_10
  --data_format DATA_FORMAT
                        Data format of the data used for testing. Default: parquet
  --num_runs NUM_RUNS, -n NUM_RUNS
                        Number of runs, the TPCS workload will be run this number of times. Default: 2
  --queries_repeat_times QUERIES_REPEAT_TIMES, -r QUERIES_REPEAT_TIMES
                        Number of repetitions, each query will be run this number of times for each run. Default: 3
  --sleep_time SLEEP_TIME, -s SLEEP_TIME
                        Time in seconds to sleep before each query execution. Default: 1
  --queries QUERIES, -q QUERIES
                        List of TPCDS queries to run. Default: all
  --queries_exclude QUERIES_EXCLUDE, -x QUERIES_EXCLUDE
                        List of queries to exclude from the running loop. Default: None
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
                        Optional output file, this will contain the collected metrics details in csv format
  --cluster_output_file CLUSTER_OUTPUT_FILE, -c CLUSTER_OUTPUT_FILE
                        Optional, save the collected metrics to a csv file using Spark, use this to save to HDFS or S3
  --run_using_metastore
                        Run TPCDS using tables defined in metastore tables instead of temporary views. See also --create_metastore_tables to define the tables.
                        Default: False
  --create_metastore_tables
                        Create metastore tables instead of using temporary views. Default: False
  --create_metastore_tables_and_compute_statistics
                        Create metastore tables and compute table statistics to use with Spark CBO. Default: False
```

### Examples:
- Run the tool for a minimal test  
  `./tpcds_pyspark_run.py -d tpcds_10 -n 1 -r 1 --queries q1,q2
- Run all queries with default options  
  `./tpcds_pyspark_run.py -d tpcds_10` 
- Run all queries on a YARN cluster and save the metrics to a file  
  ```
  spark-submit --master yarn --conf spark.log.level=error  --conf spark.executor.cores=8 \
               --conf spark.executor.memory=32g --conf spark.driver.memory=4g \
               --conf spark.driver.extraClassPath=tpcds_pyspark/spark-measure_2.12-0.23.jar \ 
               --conf spark.dynamicAllocation.enabled=false --conf spark.executor.instances=4 \
               tpcds_pyspark_run.py -d tpcds_10 -o ./tpcds_10_out.cvs -n 1 -r 1 
   ```
  
### 2. How to use TPCDS PySpark from your Python code 
- Use the TPCDS class to run TPCDS workloads from your Python code:
  - `pip install tpcds_pyspark`
  - `from tpcds_pyspark import TPCDS`

**API description: TPCDS**
- **TPCDS(data_path, data_format, num_runs=2, queries_repeat_times, queries, sleep_time)**
  - Defaults: data_path="./tpcds_10", data_format="parquet", num_runs=2, queries_repeat_times=3,
              queries=tpcds_queries, queries_exclude=[], sleep_time=1
- data_path: path to the Parquet folder with TPCDS data used for testing
- data_format: format of the TPCDS data, default: "parquet"
- num_runs: number of runs, the TPCS workload will be run this number of times. Default: 2
- queries_repeat_times: number of repetitions, each query will be run this number of times for each run. Default: 3
- queries: list of TPCDS queries to run
- queries_exclude: list of queries to exclude from the running loop
- sleep_time: time in seconds to sleep before each query execution. Default: 1
- Example: tpcds = TPCDS(data_path="tpcds_10", queries=['q1', 'q2'])

**TPCDS main class methods:**
- **map_tables:** map the TPCDS tables to the Spark catalog
  - map_tables(self, define_temporary_views=True, define_catalog_tables=False): 
  - this is a required step before running the TPCDS workload
  - Example: tpcds.map_tables()
- **run_TPCDS:** run the TPCDS workload
  - as side effect it populates the following class attributes: self.metadata, self.grouped, self.aggregated
  - Example: results = tpcds.run_TPCDS() 
- print_test_results(output_file=None): print the collected and aggregated metrics to stdout or to a file on the local filesystem
    containing the metadata, metrics grouped by query name and agregated metrics
- save_with_spark: save the collected metrics to a cluster filesystem (HDFS, S3) using Spark
  - save_with_spark(file_path): 
  - Example: tpcds.save_with_spark("HDFS_or_S3_path/my_test_metrics.csv") 
- compute_table_statistics: compute table statistics for the TPCDS tables (optional)
  - compute_table_statistics(collect_column_statistics=True)
  - use only when mapping tables to the Spark catalog (metastore) and when the statistics are not available
  - Example: tpcds.compute_table_statistics()


## Download TPCDS Data
The tool requires TPCDS benchmark data in parquet or other format. 
For convenience the TPCDS benchmark data at scale 10G can be downloaded:
```
# TPCDS scale 10G
wget https://sparkdltrigger.web.cern.ch/sparkdltrigger/TPCDS/tpcds_10.zip
unzip -q tpcds_10.zip

# TPCDS scale 100G
wget https://sparkdltrigger.web.cern.ch/sparkdltrigger/TPCDS/tpcds_100.zip
unzip tpcds_100.zip
```

## Generate TPCDS data with a configurable scale factor

- You can generate Spark TPCDS benchmark data at any scale using the following steps:
  - Download and build the Spark package from https://github.com/databricks/spark-sql-perf
  - Download and build tpcds-kit for generating data from https://github.com/databricks/tpcds-kit

See instructions at the [spark-sql-perf](https://github.com/databricks/spark-sql-perf) for additional info here some pointers/examples:
```
// 1. Generate schema
bin/spark-shell --master yarn --num-executors 25 --driver-memory 12g --executor-memory 12g --executor-cores 4 --jars <path_here>/spark-sql-perf_2.12-0.5.1-SNAPSHOT.jar

NOTES:
  - Each executor will spawn dsdgen to create data, using the parameters for size (e.g. 10000) and number of partitions (e.g. 1000)
  - Example: bash -c cd /home/luca/tpcds-kit/tools && ./dsdgen -table catalog_sales -filter Y -scale 10000 -RNGSEED 100 -parallel 1000 -child 107
  - Each "core" in the executor spawns one dsdgen
  - This workloads is memory hungry, to avoid excessive GC activity, allocate abundant memory per executor core

// Scale 10000 partitioned
val tables = new com.databricks.spark.sql.perf.tpcds.TPCDSTables(spark.sqlContext, "/home/luca/tpcds-kit/tools", "10000")
tables.genData("/user/luca/TPCDS/tpcds_10000", "parquet", true, true, true, false, "", 100)

// Optionally, generate a smaller dataset for testing and development (scale 10 non-partitioned)
val tables = new com.databricks.spark.sql.perf.tpcds.TPCDSTables(spark.sqlContext, "/home/luca/tpcds-kit/tools", "10")
tables.genData("/user/luca/TPCDS/tpcds_10_non_partiitoned", "parquet", true, false, false, false, "", 10)

```

----
## TPCDS PySpark tests output
- The tool will print to stdout the collected metrics, including timing and metrics measurements.
- It will also print metadata, metrics grouped by query name and aggregated metrics
- Save the collected metrics to a local csv files: `-o my_test_metrics.csv`
   - this will save 4 files: the raw metrics, metadata, metrics grouped by query name, and aggregated metrics
- Optionally, save the collected metrics to a cluster filesystem (HDFS, S3) using Spark: `--cluster_output_file PATH/my_test_metrics.csv` 

## Example output, TPCDS scale 10000 G:
```
****************************************************************************************
TPCDS with PySpark - workload configuration and metadata summary
****************************************************************************************

Queries list = q1.sql, q2.sql, q3.sql, q4.sql, q5.sql, q5a.sql, q6.sql, q7.sql, q8.sql, q9.sql, q10.sql, q10a.sql, q11.sql, q12.sql, q13.sql, q14a.sql, q14b.sql, q14.sql, q15.sql, q16.sql, q17.sql, q18.sql, q18a.sql, q19.sql, q20.sql, q21.sql, q22.sql, q22a.sql, q23a.sql, q23b.sql, q24.sql, q24a.sql, q24b.sql, q25.sql, q26.sql, q27.sql, q27a.sql, q28.sql, q29.sql, q30.sql, q31.sql, q32.sql, q33.sql, q34.sql, q35.sql, q35a.sql, q36.sql, q36a.sql, q37.sql, q38.sql, q39a.sql, q39b.sql, q40.sql, q41.sql, q42.sql, q43.sql, q44.sql, q45.sql, q46.sql, q47.sql, q48.sql, q49.sql, q50.sql, q51.sql, q51a.sql, q52.sql, q53.sql, q54.sql, q55.sql, q56.sql, q57.sql, q58.sql, q59.sql, q60.sql, q61.sql, q62.sql, q63.sql, q64.sql, q65.sql, q66.sql, q67.sql, q67a.sql, q68.sql, q69.sql, q70.sql, q70a.sql, q71.sql, q72.sql, q73.sql, q74.sql, q75.sql, q76.sql, q77.sql, q77a.sql, q78.sql, q79.sql, q80.sql, q80a.sql, q81.sql, q82.sql, q83.sql, q84.sql, q85.sql, q86.sql, q86a.sql, q87.sql, q88.sql, q89.sql, q90.sql, q91.sql, q92.sql, q93.sql, q94.sql, q95.sql, q96.sql, q97.sql, q98.sql, q99.sql
Number of runs = 1
Query execution repeat times = 2
Total number of executed queries = 236
Sleep time (sec) between queries = 1
Queries path = ./TPCDS_queries
Data path = /project/spark/TPCDS/tpcds_10000_parquet_1.13.1
Start time = Tue Feb 13 22:26:17 2024
End time = Wed Feb 14 04:04:53 2024

Spark version = 3.5.0
Spark master = yarn
Executor memory: 64g
Executor cores: 8
Dynamic allocation: false
Number of executors: 30
Cost Based Optimization (CBO): false
Histogram statistics: false

****************************************************************************************
Queries execution metrics
****************************************************************************************
ID,run_id,query,query_rerun_id,numStages,numTasks,elapsedTime,stageDuration,executorRunTime,executorCpuTime,executorDeserializeTime,executorDeserializeCpuTime,resultSerializationTime,jvmGCTime,shuffleFetchWaitTime,shuffleWriteTime,resultSize,diskBytesSpilled,memoryBytesSpilled,peakExecutionMemory,recordsRead,bytesRead,recordsWritten,bytesWritten,shuffleRecordsRead,shuffleTotalBlocksFetched,shuffleLocalBlocksFetched,shuffleRemoteBlocksFetched,shuffleTotalBytesRead,shuffleLocalBytesRead,shuffleRemoteBytesRead,shuffleRemoteBytesReadToDisk,shuffleBytesWritten,shuffleRecordsWritten,avg_active_tasks,elapsed_time_seconds
0,0,q1,0,13,1598,27049,42981,2603890,1421829,169738,86021,286,112985,41,7183,5470446,0,0,285051324536,1181741562,10915255971,0,0,545915189,151283,15608,135675,4977986479,584912806,4393073673,0,4977986479,545915189,96.265666013531,27.049
1,0,q1,1,13,1598,16084,26808,1184740,929524,25449,10596,11,26048,56,5177,5470532,0,0,285051324536,1181741562,10915255971,0,0,545915189,151283,16417,134866,4977983727,618596768,4359386959,0,4977983727,545915189,73.65953742850037,16.084
2,0,q2,0,14,25648,37239,64869,7047301,3444273,91026,93910,247,115833,2,243,100150384,0,0,375391768520,43052456356,172943040022,0,0,11632,8225,529,7696,318834,33672,285162,0,212507,8453,189.2451730712425,37.239
3,0,q2,1,14,25648,22888,36537,3815539,3185287,82310,87150,199,73040,39,251,100079047,0,0,375391768520,43052456356,172943040022,0,0,11632,8225,488,7737,318834,33356,285478,0,212507,8453,166.7047797972737,22.888
4,0,q3,0,5,1746,10112,9966,1030415,228990,9854,5856,11,2616,0,1459,10509414,0,0,117782197616,4411258078,35209704583,0,0,390811,37686,3050,34636,23267768,1866101,21401667,0,23267768,390811,101.90021756329114,10.112
5,0,q3,1,5,1746,8524,8456,327842,192544,9347,5040,13,3860,0,1820,10509801,0,0,117782197616,4411258078,35209704583,0,0,390811,37686,2981,34705,23267768,1844989,21422779,0,23267768,390811,38.46105114969498,8.524
6,0,q4,0,23,14354,229485,1310852,53316866,46011391,51444,33100,158,701936,10304,209178,11584164,0,0,5123530505792,19607435671,311747765391,0,0,20397715523,5883679,466508,5417171,321960323313,25415131624,296545191689,0,306864817793,20072715523,232.33268405342398,229.485
7,0,q4,1,23,14354,220132,1239817,49702656,44602221,39065,29822,51,509756,13078,207777,11584250,0,0,5123530505792,19607435671,311747765391,0,0,20397715523,5883679,466522,5417157,321960321336,25311407721,296648913615,0,306864815816,20072715523,225.785692221031,220.132
8,0,q5,0,11,5838,83810,156261,16102831,14451561,17812,11212,46,28376,13821,49520,10458989,0,0,1257451110736,7757286572,48148991652,0,0,7203624731,2068875,162699,1906176,66736580701,5235750051,61500830650,0,66736580701,7203624731,192.13496002863621,83.81
9,0,q5,1,11,5838,84803,130478,15067494,14368739,15804,10888,30,36578,2969,48492,10475071,0,0,1257451110736,7757286572,48148991652,0,0,7203624731,2068875,162606,1906269,66736581021,5235485732,61501095289,0,66736581021,7203624731,177.67642654151385,84.803
...
...
232,0,q98,0,8,538,15632,15818,365952,301835,4054,1459,52,740,715,1425,12941557,0,0,95030710528,261571517,2109867123,0,0,261510330,34282,3209,31073,1663002293,105130493,1557871800,0,1658028830,261450176,23.410440122824973,15.632
233,0,q98,1,8,538,13992,14279,281643,261937,3738,1267,45,371,920,1426,12941557,0,0,95030448384,261571517,2109867123,0,0,261510330,34282,2673,31609,1663002605,80730434,1582272171,0,1658028683,261450176,20.128859348198972,13.992
234,0,q99,0,7,9026,31334,31236,4577896,2396301,31069,25531,53,12388,22403,5465,58717364,0,0,355136647592,14399900462,38374031139,0,0,10043592,712331,55774,656557,444574133,34740764,409833369,0,444574133,10043592,146.09995532009958,31.334
235,0,q99,1,7,9026,22498,22421,3205913,2262629,29754,25055,53,10275,5148,5818,58713322,0,0,355136647592,14399900462,38374031139,0,0,10043592,712331,56563,655768,444574133,35371829,409202304,0,444574133,10043592,142.49768868343853,22.498

****************************************************************************************
Queries execution metrics")
****************************************************************************************
numStages,2857
numTasks,1827295
elapsedTime,20005523
stageDuration,36468759
executorRunTime,2704722153
executorCpuTime,2199621274
executorDeserializeTime,6803172
executorDeserializeCpuTime,4379737
resultSerializationTime,16590
jvmGCTime,18277689
shuffleFetchWaitTime,42186135
shuffleWriteTime,8963205
resultSize,3879544630
diskBytesSpilled,1366913731410
memoryBytesSpilled,4823738858584
peakExecutionMemory,303581396839536
recordsRead,3598288833438
bytesRead,23532365966930
recordsWritten,0
bytesWritten,0
shuffleRecordsRead,1317493814871
shuffleTotalBlocksFetched,475685960
shuffleLocalBlocksFetched,39371104
shuffleRemoteBlocksFetched,436314856
shuffleTotalBytesRead,10063827808349
shuffleLocalBytesRead,855205742152
shuffleRemoteBytesRead,9208622066197
shuffleRemoteBytesReadToDisk,0
shuffleBytesWritten,7853953732282
shuffleRecordsWritten,959912472985
avg_active_tasks,135
elapsed_time_seconds,20005
```

---
## Links and references

- [TPCDS-PySpark on Pypi](https://pypi.org/project/TPCDS-PySpark)
- TPCDS official website: [TPCDS](http://www.tpc.org/tpcds/)
- TPCDS queries: [TPCDS from Apache Spark tests](https://github.com/apache/spark/tree/master/sql/core/src/test/resources/tpcds)
and [TPCDS-v2.7.0 from Apache Spark tests](https://github.com/apache/spark/tree/master/sql/core/src/test/resources/tpcds-v2.7.0)
- See also [Databricks' spark-sql-perf](https://github.com/databricks/spark-sql-perf)
- TPCDS schema creation from: [TPCDS Kit](https://github.com/databricks/tpcds-kit)
- [sparkMeasure](https://github.com/LucaCanali/sparkMeasure)
- [Performance Troubleshooting Using Apache Spark Metrics](http://canali.web.cern.ch/docs/Spark_Performance_Troubleshooting_Metrics_SAISEU2019_Luca_Canali_CERN.pdf)
  Spark Summit Europe 2019
