# socialtoolkit
Toolkit for the simulation of models of social contagion and cultural dissemination in multilayered systems.

## Install Dependencies
> pip install networkx


## Running
Example
> python stk.py --traits=10 --features=10 --gridsize=10


====== SPARK USE ======
1. Configure spark
    Install spark with a default folder path
    Mount the common folder in all computers
    1.2 Configure Python version using virtualenv (this way all dependencies will be the same)
        http://www.cloudera.com/documentation/enterprise/5-5-x/topics/spark_python.html
        Example:
            virtualenv stk_env
            source ./stk_env/bin/activate
            pip install numpy
            pip install networkx
        Put the created folder on the common directory (in my case /userdata/vroth)
    1.3 Configure the needed dependencies for the running machine
        pip install py4j
2. Before running
    export SPARK_HOME=/clusterdata/spark/spark-1.6.0-bin-hadoop2.6
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
    export PYSPARK_PYTHON=/userdata/vroth/stk_env/bin/python
3. Running
    ./stk.py --spark

====== HOW WAS DONE ======
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

