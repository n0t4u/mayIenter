#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Version 0.8.3

#TODO
"""
Add Auth header support

Check if similar cookie

"""

#Imports
import argparse
from termcolor import colored
import logging
import os
import requests
import sys
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Variables and classes
users={}
pathsFile=""
results=[]

status={
	"200":"green",
	"202":"green",
	"301":"yellow",
	"302":"yellow",
	"401":"red",
	"403":"red",
	"404":"yellow",
	"500":"red",
	"ERROR":"red"
}
#Functions

def header():
	print("""
	                           _____                _             ___  
	                          |_   _|              | |           |__ \ 
	 _ __ ___    __ _  _   _    | |     ___  _ __  | |_  ___  _ __  ) |
	| '_ ` _ \  / _` || | | |   | |    / _ \| '_ \ | __|/ _ \| '__|/ / 
	| | | | | || (_| || |_| |   | |   |  __/| | | || |_|  __/| |  |_|  
	|_| |_| |_| \__,_| \__, |   | |    \___||_| |_| \__|\___||_|  (_)  
	                    __/ |  _| |_                                   
	                   |___/  |_____|  """+colored("This is n0t4u","cyan")+"""                    
	
	""")

#Performs a get Request to a route with the given cookies
def getRequest(route,cookie):
	logging.info("Route: %s\nCookie: %s" %(route,cookie))
	try:
		response = requests.get(route, headers={"Cookie":cookie}, allow_redirects=False,timeout=10, verify=False)
	except Exception as e:
		logging.info(e)
		return "ERROR"
	else:
		return str(response.status_code)

def argumentsData():
	global pathsFile
	logging.info(args.data[0])
	for data in args.data[0].split(","):
		logging.info(colored("[*]","blue")+" Data %s" %data)
		#user,cookie = data.split(':')
		#users[user].append[cookie]
		try:
			user,cookie = data.split(":")
			logging.info(colored("[*]","blue")+" User %s, Cookie %s" %(user,cookie))
		except:
			print(colored("[!] User %s has no cookie assigned. Use ':' to separate user and cookie" %data,"red"))
		else:
			users[user]= cookie
	logging.info(args.file[0])
	if os.path.isfile(args.file[0]):
		pathsFile= args.file[0]
	elif os.path.isfile(os.getcwd()+"/"+args.file[0]):
		pathsFile= os.getcwd()+"/"+args.file[0]
	else:
		print(colored("[!] Unable to find the file %s" %args.file[0],"red"))
	return

def interactiveData():
	global pathsFile
	print("Introduce username and session cookies.\nIf you do not want to add more, leave the name empty.")
	try:
		n = 0 
		while n < 2:
			user= str(input(colored("[»] Username: ","cyan"))).strip(" ")
			if user and user != "Anonymous":
				cookie= str(input(colored("[»] Cookie: ","cyan"))).strip(" ")
				try:
					users[user]= cookie
					print(colored("[+] User %s with cookie %s sucessfully imported" %(user,cookie),"green"))
					n+=1
				except Exception as e:
					logging.info(colored("[!] %s" %e,"red"))
			else:
				n = 2
		print("Introduce the file with the paths to be tested.")
		file = str(input(colored("[»] Filepath: ","cyan")))
		if os.path.isfile(file):
			pathsFile= file
		elif os.path.isfile(os.getcwd()+"/"+file):
			pathsFile= os.getcwd()+"/"+file
		else:
			print(colored("[!] Unable to find the file %s" %file,"red"))
	except KeyboardInterrupt:
		#CTRL+C
		sys.exit(0)


#Argument Parser
parser= argparse.ArgumentParser(description="Authomatic tool to determine authorization privileges between several users.")

#parser.add_argument("url",help="URL to crawl and check authorization", nargs=1)
parser.add_argument("-d","--data",dest="data",help="Data in dictionary format. Example: 'Admin:CookieAdmin,User:CookieUser'",nargs=1)
parser.add_argument("-f","--file",dest="file",help="File with routes to check.",nargs=1)
parser.add_argument("-v","--verbose",dest="verbose", help="Muestra por pantalla tramas de la ejecución.", action="store_true")

args = parser.parse_args()


#Main
if __name__ == '__main__':
	startTime = time.time()
	#header()
	if args.verbose:
		logging.basicConfig(level=logging.INFO)
	#logging.info(colored("[*] %s" %args.url[0],"green"))
	if args.data and args.file:
		argumentsData()
	else:
		interactiveData()

	users["Anonymous"]=""
	logging.info(users)
	logging.info("File %s" %pathsFile)
	keys = list(users.keys())
	tableHeader = "Route".ljust(50," ")+str(keys[0]).center(13," ")+str(keys[1]).center(12," ")+str(keys[2]).center(12," ")
	print(colored(tableHeader,"blue")) #16 --> 24,25,25
	#print(aux.ljust(35," "),colored(hasKey,'red'))
	try:

		with open(pathsFile,"r", encoding="iso-8859-1") as file:
			for line in file:
				#logging.info(line)
				statusCodes=[]
				for user,cookie in users.items():
					statusCodes.append(getRequest(route=line.strip("\n"),cookie=cookie.strip("\n")))
				url = line.lstrip("https://").rstrip("\n")
				#print(url[0:15]+"..."+url[-21:-1])
				if len(url)<51:
					col1 =url
				else:
					col1 =url[0:15]+"..."+url[-31:]
				col2 = colored(statusCodes[0],status[statusCodes[0]])
				col3 = colored(statusCodes[1],status[statusCodes[1]])
				col4 = colored(statusCodes[2],status[statusCodes[2]])
				print(col1.ljust(50," "),col2.center(20," "),col3.center(20," "),col4.center(20," "))
				#print(line.rsplit("/",1).strip("\n"),statusCodes)
				res = [line.strip("\n"),statusCodes]
				#print(res)
				results.append(res)
	except KeyboardInterrupt:
		#CTRL+C
		sys.exit(0)
	except Exception as e:
		print(e)
	finally:
		with open("mayIenter_results.txt","w+",encoding="iso-8859-1") as file:
			for res in results:
				resStatus =",".join(res[1])
				#resStatus =",".join([str(s) for s in res[1]])
				line = res[0]+","+resStatus+"\n"
				file.write(line)
		executionTime = time.time()- startTime
		if executionTime/60 > 1:
			print(colored("--- %d segundos --- (%d minutos) ---" %(round(executionTime,3), round(executionTime/60,3)),"green"))
		else:
			print(colored("--- %d segundos ---" %round(executionTime,3),"green"))
