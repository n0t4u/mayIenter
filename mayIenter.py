#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Version 0.8.0

#TODO
"""
Add Auth header support
Add comparative table
"""

#Imports
import argparse
from termcolor import colored
import logging
import os
import sys
import time

#Variables and classes
users={}
pathsFile=""
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
	header()
	if args.verbose:
		logging.basicConfig(level=logging.INFO)
	#logging.info(colored("[*] %s" %args.url[0],"green"))
	if args.data and args.file:
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
	else:
		hashname=True
		print("Introduce username and session cookies.\nIf you do not want to add more, leave the name empty.")
		try:
			while hashname:
				user= str(input(colored("[»] Username: ","cyan"))).strip(" ")
				if user and user != "Anonymous":
					cookie= str(input(colored("[»] Cookie: ","cyan"))).strip(" ")
					try:
						users[user]= cookie
						print(colored("[+] User %s with cookie %s sucessfully imported" %(user,cookie),"green"))
					except Exception as e:
						logging.info(colored("[!] %s" %e,"red"))
				else:
					hashname=False
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


	users["Anonymous"]=""
	logging.info(users)



	executionTime = time.time()- startTime
	if executionTime/60 > 1:
		print("--- %d segundos --- (%d minutos) ---" %(round(executionTime,3), round(executionTime/60,3)))
	else:
		print("--- %d segundos ---" %round(executionTime,3))
