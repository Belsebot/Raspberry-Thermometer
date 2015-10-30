import datetime
import time
import socket

host = '192.168.0.100'                                                #server address
port = 10000                                                          #server port

def send_server(str):                                                 #sending temp to server
	clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		clientsocket.connect((host,port))
		clientsocket.send(str)
	except Exception, e:
		print 'connection failed'

	clientsocket.close()
	return

temp_sensor = '/sys/bus/w1/devices/28-031561cf2dff/w1_slave'  #devicefile for DS18B20 temperature sensor

def temp_raw():                                               #opens devicefile and reads it
	f=open(temp_sensor,'r')
	lines=f.readlines()
	f.close()
	return lines

def read_temp():                                              #grepping temperature from lines
	lines=temp_raw()
	while lines[0].strip() [-3:] != 'YES':
		time.sleep(0.2)
		lines=temp_raw()
	temp_output=lines[1].find('t=')                             
	if temp_output != -1:
		temp_string = lines[1].strip() [temp_output+2:]           #getting temperature
		temp_c = float(temp_string) / 1000.0                      
		return temp_c


deg_c=read_temp()

now=datetime.datetime.now()
hour=now.strftime("%H")
min=now.strftime("%M")
temp_time=hour
temp_max=deg_c
temp_min=deg_c

print "Paina CTRL+C lopettaaksesi"
try:
	print "Waiting keypress"
	while True:                               #loop
		now = datetime.datetime.now()
		hour = now.strftime("%H")
		deg_c=read_temp()

		if deg_c>temp_max:                #if current temperature is higher than max temperature
			temp_max=deg_c                  #then make it new max temperature
		if deg_c<temp_min:                #if current temperature is lower than low temperature
			temp_min=deg_c                  #then make it new min temperature

		time.sleep(60)
		if hour!=temp_time:                 #if hour changes
			if hour=="00":                    #if day changes
				print "-------Paiva:",now.strftime("%d-%m"),"-------"
			print "Kello:",now.strftime("%H:%M"),"Lampotila:",deg_c,"Max:",temp_max,"Min:",temp_min

			lampotila='Kello:' + now.strftime("%H:%M") + ' Lampotila:'+ str(deg_c) + ' Max:'+ str(temp_max) + ' Min:'+ str(temp_min)

			send_server(lampotila)                                        #sending temperature to server
	
			temp_min=deg_c                                                #setting current temperature to min value
			temp_max=deg_c                                                #setting current temperature to max value
		temp_time=hour

except KeyboardInterrupt:
	print "Ohjelma lopetetaan"

print "Ohjelma loppui"
