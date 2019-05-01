#!/bin/python3.6
import subprocess,sys, logmsg
from ast import literal_eval as mtuple
from etcddel import etcddel as etcddel
from broadcast import broadcast as broadcast 
from broadcasttolocal import broadcasttolocal as broadcasttolocal
from etcdget import etcdget as get
from etcdgetlocal import etcdget as getlocal
from etcdput import etcdput as put 
import json
cmdline='cat /pacedata/perfmon'
perfmon=str(subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout)
if '1' in perfmon:
 cmdline=['/TopStor/queuethis.sh','remknown.py','start','system']
 result=subprocess.run(cmdline,stdout=subprocess.PIPE)
known=get('known','--prefix')
nextone=get('nextlead')
if str(nextone[0]).split('/')[0] not in  str(known):
 print('deleting nextlead')
 etcddel('nextlead')
 nextone=[]
if known != []:
 for kno in known:
  kn=kno 
  heart=getlocal(kn[1],'local','--prefix')
  print('heartbeat=',heart, kn[1])
  print(type(heart),heart)
  if( '-1' in str(heart) or len(heart) < 1) or (heart[0][1] not in kn[1]):
   print('the known ',kn[0].replace('known/',''),' is gone, notfound')
   etcddel(kn[0])
   if kn[1] in str(nextone):
    etcddel('nextlead')
   logmsg.sendlog('Partst02','warning','system', kn[0].replace('known/',''))
   etcddel('ready/'+kn[0].replace('known/',''))
   etcddel('old','--prefix')
   cmdline=['/pace/hostlost.sh',kn[0].replace('known/','')]
   subprocess.run(cmdline,stdout=subprocess.PIPE)
   etcddel('localrun/'+str(kn[0]))
   broadcast('broadcast','/pace/hostlostfromleader.sh',kn[0].replace('known/',''))
   broadcast('broadcast','/TopStor/pump.sh','zpooltoimport.py','all')
  else:
   if nextone == []:
    put('nextlead',kn[0].replace('known/','')+'/'+kn[1])
    broadcast('broadcast','/TopStor/pump.sh','syncnext.sh','nextlead','nextlead')
if '1' in perfmon:
 cmdline=['/TopStor/queuethis.sh','remknown.py','stop','system']
 result=subprocess.run(cmdline,stdout=subprocess.PIPE)
