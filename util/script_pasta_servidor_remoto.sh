#!/bin/sh
apt-get install -y nfs-common autofs
mkdir /userdata
su -c "echo 'igapo.lis:/serverdata/userdata    /userdata  nfs rw,hard,intr 0 0' >> /etc/fstab"
service autofs start
mountall
