#!/user/bin/python
# Author=Zhen Shi
# Student number=014565117
import random
import math
import sys
import thread
import socket
import time
import pickle

#--Class node hold all functionalities of vector clock
class Node:

#initialize of class node

	def __init__ (self,lineNumber):
		
		self.val=0
		self.ID =0
		self.vector={}
		self.index=[]
		self.port=0
		self.hostname=0
		self.portlist=[]
		self.lineNumber=lineNumber

#increment function for increment self when reciving and sending the event	
	def increment (self):
		
		self.val+=1
		self.vector[self.ID]=self.val
		
		return self.val
#increase function for self event
	def increase(self,num):
		

		self.val+=num

		print "l",num

		self.vector[self.ID]=self.val

		return self.val
#receiver function for dealing with received msg
	def receiver(self,vector_rec):

		for key in self.vector:
			
			if key in vector_rec:
				
				new_val=max(self.vector[key],vector_rec[key])
				vector_rec[key]=new_val;
				
				
		self.vector.update(vector_rec)
		self.vector[self.ID]+=1
		
	def  sender(self):
		self.increment()
#randomly pick event the sending and local events		
	def random_pick(self):

		flag=random.randint(1,2)

		num_val= random.randint(1,5)
		
		if flag==1:

			self.sender()
			self.msgSender()
			
		else:

			self.increase(num_val)
			
#read the configuration_file
	def readConfigFile(self,filename):
		config=open(filename,"r")
		self.index=[line.strip() for line in config]
		
		return self.index
#read line number from configuration file	
	def readLineNumber(self,line):
		
		texts=self.index
		
		for text in texts:
			IDlist=text.split()
			
			if int(IDlist[0])== int(line):
				self.ID=IDlist[0]
				self.vector={self.ID:0}

#according to the configuration file get the port number		
	def readSelfPort(self):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[0]==self.ID:
				self.port=IDlist[2]
				break
		
		return self.port
	
	def readHostName(self):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[0]==self.ID:
				self.hostname=IDlist[1]

				break
		return self.hostname
		
#read other port number
	def readOtherPorts(self,ID):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[0]!=self.ID:
				self.portlist.append(IDlist[2])
				break
		
#get other host
	def getOtherHost(self,port):

		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[2]==port:
				
				hostname=IDlist[1]

		return hostname
#get other host id
	def getOtherID(self,port):
		
		texts=self.index
		for text in texts:
			IDlist=text.split()
			if IDlist[2]==port:
				
				hostID=IDlist[0]

		return hostID
#sending the msg to different host
	def msgSender(self):
	
	
		while 1:
			randomSender=random.randint(1,len(self.portlist))
			if (randomSender!=self.lineNumber):
				
				targetPort=self.portlist[randomSender-1]
				break

		
		targetHost=self.getOtherHost(targetPort)
		targetId=self.getOtherID(targetPort)
		socketconn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# testport=3500

		remote_ip = socket.gethostbyname(targetHost)
		socketconn.connect((remote_ip,int(targetPort)))

		print "s", self.ID, self.vector.values()
		
		msg=[str(self.ID),self.vector]
		data_string = pickle.dumps(msg)

		socketconn.send(data_string)
		socketconn.close();
#listening the msg from different hosts

	def startSocketListener(self,port):

		#create an AF_INET, STREAM socket (TCP)
		socketSelf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		remote_ip = socket.gethostbyname(self.hostname)
		socketSelf.bind((remote_ip, int(port)))
		socketSelf.listen(10)
		
		while 1:
			#wait to accept a connection - blocking call
			conn, addr = socketSelf.accept()
			#print "Address is",addr
			msg=conn.recv(1024)
			data_arr = pickle.loads(msg)
			
			senderId=data_arr[0]
			self.receiver(data_arr[1])			
			print 'r',senderId,data_arr[1].values(),self.vector.values()
		conn.close()

#----Here is the main function----------

if(len(sys.argv)<3) :
	print "Please enter this format:[program] [configuration_file] [line]"
	sys.exit()
#reading the configuration_file
getFileName=str(sys.argv[1])
lineNumber=int(sys.argv[2])

event=Node(lineNumber)
event.readConfigFile(getFileName)
event.readLineNumber(lineNumber)

selfport=event.readSelfPort()
selfhost=event.readHostName()
event.readOtherPorts(event.ID)
time.sleep(15)

numberOfevent=0
#create the new thread to listen
thread.start_new_thread(event.startSocketListener,(selfport,))
while numberOfevent<100:

	event.random_pick()
	numberOfevent+=1
time.sleep(20)