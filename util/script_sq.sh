#!/bin/sh
mkdir -p /clusterdata/spark
cd /clusterdata/spark
wget http://d3kbcqa49mib13.cloudfront.net/spark-1.6.0-bin-hadoop2.6.tgz
tar -xvf spark-1.6.0-bin-hadoop2.6.tgz
apt-get install -y scala
/clusterdata/spark/spark-1.6.0-bin-hadoop2.6/sbin/start-slave.sh spark://10.1.1.28:7077
mv /etc/rc.local /etc/rc.local.bkp
head -n -1 /etc/rc.local.bkp > /etc/rc.local
echo "/clusterdata/spark/spark-1.6.0-bin-hadoop2.6/sbin/start-slave.sh spark://10.1.1.28:7077" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local
