#!/usr/bin/python3
import subprocess,sys, os
import json
from time import sleep

def etcdctl(etcd,key,prefix):
 cmdline=['etcdctl','--user=root:YN-Password_123','--endpoints=http://'+etcd+':2379','put',key,prefix]
 cmdline=['etcdctl','--endpoints=http://'+etcd+':2379','put',key,prefix]
 result=subprocess.run(cmdline,stdout=subprocess.PIPE, timeout=2)
 return result 




def etcdput(etcd, key,val):
 os.environ['ETCDCTL_API']= '3'
 etcdctl(etcd, key,val)
 return 1 


if __name__=='__main__':
 etcdput(*sys.argv[1:])
