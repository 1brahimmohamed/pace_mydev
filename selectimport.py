#!/bin/python3.6
from etcdget import etcdget as get
from etcdput import etcdput as put 
from etcddel import etcddel as deli 
import socket, sys, subprocess,datetime
from sendhost import sendhost
from ast import literal_eval as mtuple
#from zpooltoimport import zpooltoimport as importables

def importpls(myhost,allinfo,*args):
	if(len(allinfo) < 0):
		return
	pools={}
	for host in allinfo:
		if 'nothing' in host[1]:
			continue
		for pool in mtuple(host[1]):
			pools[pool[0]]=[]
	for host in allinfo:
		if 'nothing' in host[1]:
			continue
		for pool in mtuple(host[1]):
			pools[pool[0]].append((host[0].split('/')[1],pool[1],pool[2]))
	hosts=[]
	importedpools=['hi']
	for pool in pools.keys():
		hosts.append((pool,max(pools[pool],key=lambda x:x[1])[0])) 
	for hostpair in hosts:
		if hostpair[0] == 'nothing':
			continue
		owner=hostpair[1]
		print('owner=',owner)
################# elect the host to import the pool ###############
		print('pool toimport',hostpair[0])
		timestamp=int(datetime.datetime.now().timestamp())+60
		print('timestamp',str(timestamp))
		locked=get('lockedpools','--prefix')
		ownerstatus=get('cannotimport/'+owner)
		print('owner',owner)
		if hostpair[0] in ownerstatus:
			print('in ownerstatus')
			continue
		#if hostpair[0] in importedpools:
		#	print('in importedpools')
		#	continue
		if hostpair[0] in locked:
			print('in locked')
			oldtimestamp=get('lockedpools/'+hostpair[0]).split('/')[1]
			if(int(timestamp) > int(oldtimestamp)):
				deli('lockedpools/'+hostpair[0])
			else:
				continue
		#importedpools.append(hostpair[0])
		ownerip=get('leader',owner)
		if ownerip[0]== -1:
			print('here')
			ownerip=get('known',owner)
			print('ownerip',ownerip[0])
			if str(ownerip[0])== '-1':
				print('here2lldkf')
				return
			else:
				print('willcontinue')
		print('putting into locked',hostpair[0]+'/'+owner)
		put('lockedpools/'+hostpair[0],owner+'/'+str(timestamp))
#################### end of election
		z=['/TopStor/pump.sh','Zpool','import','-c','/TopStordata/'+hostpair[0],'-am']

		msg={'req': 'Zpoolimport', 'reply':z}
		sendhost(ownerip[0][1], str(msg),'recvreply',myhost)
		#z=['/TopStor/pump.sh','ClearCache',hostpair[0][1:]]
		#msg={'req': 'ClearCache', 'reply':z}
		#sendhost(ownerip[0][1], str(msg),'recvreply',myhost)
		deli('toimport',hostpair[0])
	return

if __name__=='__main__':
	myhost=socket.gethostname()
	try:
		x=subprocess.check_output(['pgrep','-c', 'selectimport'])
		x=str(x).replace("b'","").replace("'","").split('\\n')
		if(x[0]!= '1'):
			print('process still running',str(x[0]))
		else:
			allinfo=get('to','--prefix')
			importpls(myhost,allinfo,*sys.argv[1:])
	except:
		pass 
 
