# socialtoolkit
Toolkit for the simulation of models of social contagion and cultural dissemination in multilayered systems.

## Install Dependencies
> pip install networkx


## Running
Example
> python stk.py --traits=10 --features=10 --gridsize=10


## Spark use
### Configure spark
1. Install spark with a default folder path
2. Mount the common folder in all computers
3. Configure Python version using virtualenv (this way all dependencies will be the same)
  * Example: [(source)](http://www.cloudera.com/documentation/enterprise/5-5-x/topics/spark_python.html)
```
virtualenv stk_env
source ./stk_env/bin/activate
pip install numpy
pip install networkx
```
4. Put the created folder on the common directory (in my case /userdata/vroth)
5. Configure the needed dependencies for the running machine
  > pip install py4j

### Before running
 ```
export SPARK_HOME=/clusterdata/spark/spark-1.6.0-bin-hadoop2.6
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
export PYSPARK_PYTHON=/userdata/vroth/stk_env/bin/python
```

### Running with Spark
  > ./stk.py --spark

### How was done 
 ```
def work(x):
    return x*x
all_P = [1, 2, 3, 4, 5] # is the work list

from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("workname").setMaster("spark://10.1.1.28:7077") #work name and master location 
sc = SparkContext(conf=conf) # connect!
sc.addPyFile("util/socialtoolkit.zip") # this is for an internal library
ratios_RDD = sc.parallelize(all_P, 10000) # divide the work on 10000 (changes on the run)
prepared_work = ratios_RDD.map(work) # work is the function
result = prepared_work.collect() #get the result as a list
```

# TODO
  [ ] range for layer range
  [ ] change spark directory (optional argument)
  [ ] document code
  [ ] size of the largest cultural group
  [ ] fix methods name on util / graph_util
  [ ] mean value for tests
