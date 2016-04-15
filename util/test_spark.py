#!/usr/bin/python

from __future__ import print_function

import sys
sys.path.append("/clusterdata/spark/spark-1.6.0-bin-hadoop2.6/python")
import os
os.environ['SPARK_HOME'] = "/clusterdata/spark/spark-1.6.0-bin-hadoop2.6"

from pyspark import SparkContext, SparkConf

import subprocess

import numpy as np

def job(x):
    proc = subprocess.Popen(["pip install numpy"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    
    #proc = subprocess.Popen(["who"], stdout=subprocess.PIPE, shell=True)
    #(out, err) = proc.communicate()
    
    #proc2 = subprocess.Popen(["uname -a"], stdout=subprocess.PIPE, shell=True)
    #(out2, err2) = proc2.communicate()
    
    proc3 = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE, shell=True)
    (out3, err3) = proc3.communicate()
    try:
        import networkx
    except ImportError as e:
        print(e)
    return (sys.version, os.system("who"), out, err, out3, err3)
    
def job2(x):
    #proc = subprocess.Popen(["pip install numpy --upgrade"], stdout=subprocess.PIPE, shell=True)
    #(out, err) = proc.communicate()
    os.environ["PYSPARK_PYTHON"] = "/userdata/vroth/stk_env/bin/python" ## TEM QUE COLOCAR POR FORA: export PYSPARK_PYTHON=...
    import numpy as np
    import networkx as nx
    return (np.random.random())
    
conf = SparkConf().setAppName("testing_python_versions").setMaster("spark://10.1.1.28:7077")

sc = SparkContext(conf=conf)

ratios_RDD = sc.parallelize(range(0, 36), 36)
prepared_work = ratios_RDD.map(job2)
result = prepared_work.collect()

print("begin results")
for i in result:
    print(i)
print("end results")
