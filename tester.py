#!/user/bin/python
# -*- coding: <encoding name> -*-
import random
import math
import sys
import thread
import socket
import time
import pickle

class Node:

	def __init__ (self,lineNumber):
		
		self.val=0
		self.ID =0
		self.vector={}
		self.index=[]
		self.port=0
		self.hostname=0
		self.portlist=[]
		self.lineNumber=lineNumber

		# print self.ID

		# print "ID and values", self.vector.values()

		# print "Initialize sucessed! "

	def increment (self):
		
		self.val+=1
		self.vector[self.ID]=self.val
		
		# print "after self value increment:", self.val

		return self.val

	def increase(self,num):
		

		self.val+=num

		self.vector[self.ID]=self.val

		# print "after self value increase", self.val
		
		return self.val

	def receiver(self,vector_rec):

		for key in self.vector:
			
			if key in vector_rec:
				
				new_val=max(self.vector[key],vector_rec[key])
				vector_rec[key]=new_val;
				
				print new_val

		# print "Self vector dictonary before update",self.vector
		self.vector.update(vector_rec)
		self.vector[self.ID]+=1
		print "Self vector dictonary after update", self.vector
	

		# print "NODE 1 value",node1.vector
		# print "NODE 2 value",node2.vector
		# print "NODE 3 value",node3.vector
		
	def  sender(self):
		self.increment()
		# print "Sender has been called"

	def random_pick(self):

		flag=random.randint(1,2)

		num_val= random.randint(1,5)
		# print "flag is :", flag
		# print "number vallue is:",num_val

		if flag==1:

			self.sender()
			self.msgSender()
			# print "self increment has been called"
		else:

			self.increase(num_val)
			# print"self increase has been called"

	def readConfigFile(self,filename):
		config=open(filename,"r")
		self.index=[line.strip() for line in config]
		# print "Read Config File sucessed!!!", self.index
		return self.index
	
	def readLineNumber(self,line):
		# print "The line number read from command line",line
		texts=self.index
		# print "The index for check",texts
		for text in texts:
			IDlist=text.split()
			# print "After text split",IDlist
			# print "The id in the list",IDlist[0]
			if int(IDlist[0])== int(line):
				self.ID=IDlist[0]
				self.vector={self.ID:0}

		# 		print "sucessed assign as",self.vector
		
				
		# print "read Line Number sucessed!", self.ID
	
	def readSelfPort(self):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[0]==self.ID:
				self.port=IDlist[2]
				break
		# print "read Port Number sucessed!", self.port
		return self.port
	
	def readHostName(self):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[0]==self.ID:
				self.hostname=IDlist[1]

				break
		return self.hostname
		# print "read hostname sucessed!", self.hostname

	def readOtherPorts(self,ID):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[0]!=self.ID:
				self.portlist.append(IDlist[2])
				break
		# print "read other Ports Number sucessed!", self.portlist

	def getOtherHost(self,port):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[2]==port:
				
				hostname=IDlist[1]

		return hostname

	def getOtherID(self,port):
		
		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[2]==port:
				
				hostID=IDlist[0]

		# print "read other id sucessed!", hostID
		return hostID

	def msgSender(self):
	
	
		while 1:
			randomSender=random.randint(1,len(self.portlist))
			if (randomSender!=self.lineNumber):
				
				targetPort=self.portlist[randomSender-1]
				break

		# print "target port",targetPort
		targetHost=self.getOtherHost(targetPort)
		# print "target targetHost",targetHost
		targetId=self.getOtherID(targetPort)
		# print "target ID",targetId
		socketconn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		testtargethost="localhost"
		# testport=3500

		remote_ip = socket.gethostbyname(testtargethost)
		socketconn.connect((remote_ip,int(targetPort)))

		print "s", targetId, self.vector
		#msg=str(targetId)+"."+self.vector
		msg=[str(targetId),self.vector]
		data_string = pickle.dumps(msg)

		socketconn.send(data_string)
		socketconn.close();


	def startSocketListener(self,port):

		#create an AF_INET, STREAM socket (TCP)
		socketSelf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# print "Socket Create",self.hostname,port
		hostname="localhost"
		
		remote_ip = socket.gethostbyname(hostname)
		socketSelf.bind((remote_ip, int(port)))
		socketSelf.listen(10)
		# print "Socket Now listening on",port

		while 1:
			#wait to accept a connection - blocking call
			conn, addr = socketSelf.accept()
			print "Address is",addr
			msg=conn.recv(1024)
			data_arr = pickle.loads(msg)
			
			senderId=data_arr[0]
			self.receiver(data_arr[1])			
			print 'r',senderId,msg[1],self.vector
		conn.close()



		





if(len(sys.argv)<3) :
	print "usage:[program] [configuration_file] [line]"
	sys.exit()

getFileName=str(sys.argv[1])
# print "The file name read from command line", getFileName
lineNumber=int(sys.argv[2])

event=Node(lineNumber)

# print "The line number read from command line",lineNumber
event.readConfigFile(getFileName)
# print "This is main program read file name"
event.readLineNumber(lineNumber)
# print "This is main program read linenumber"
selfport=event.readSelfPort()
# print "This is main program read event", selfport
selfhost=event.readHostName()
# print "This is main prgram read host name"
event.readOtherPorts(event.ID)


# print "after create'a thread!"
time.sleep(15)

numberOfevent=0
# print "number of event 0"

thread.start_new_thread(event.startSocketListener,(selfport,))
while numberOfevent<100:

	event.random_pick()
	# print "number of event:",numberOfevent
	numberOfevent+=1
time.sleep(20)



