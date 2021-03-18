from Interface import GetKeyPress
from Interface.FrSqlTools import Events
from Interface.FrSqlTools.Events import KeyEvents
from Interface.FrSqlTools.HistoryRecorder import HistoryRecorder
from Interface.FrSqlTools.Utils import log
from Interface.FrSqlTools.Commands import COMMANDS
from sys import stdout
from ColorStr import parse
import mysql.connector
import LanguageControls
import DirControls
import readchar
import sys
import os
import getpass

class FrSqlTools:
	def __init__(self):
		self.commandHistory = HistoryRecorder()
		self.command = ""
		self.commandCarrot = 0
		self.db = None
		self.sqlCache = ""
		self.meta = {
			"host":"",
			"user":"",
			"dbName":""
		}
		self.flags = {
			"interpretBreak":False,
			"welcome":True,
			"layer":0,
			"mode":"normal"
		}
	def connect(self,host="",user="",password=""):
		self.db = mysql.connector.connect(host=host, user=user, password=password)
		self.meta = {"host":host, "user":user, "dbName": self.meta["dbName"]}
		log(f"Connected to {host} as {user}.")
	def appendHistory(self,cmd,hidden):
		if not cmd.strip() == "":
			self.commandHistory.append(cmd,hidden)
	def clearCommandArea(self):
		sys.stdout.write("\r"+(" " * len(f"{self.getPrompt()}{self.command}")))
		sys.stdout.flush()
	def stop(self):
		self.flags["interpretBreak"] = True
	def execCmd(self,cmd):
		if not cmd.strip():
			return
		parts = cmd.split(" ")
		if parts[0] in COMMANDS:
			COMMANDS[parts[0]](self,parts[1:])
		else:
			log(f"Unknown Command: {parts[0]}", isError=True)
	def execSql(self,sql):
		cur = self.db.cursor()
		cur.execute(sql)
		return cur
	def fetchDatabases(self):
		cursor = self.execSql("SHOW DATABASES")
		return [i[0] for i in cursor]
	def fetchTables(self):
		cursor = self.execSql("SHOW TABLES")
		return [i[0] for i in cursor]
	def useDb(self,name):
		if not name.strip():
			log("Invalid Database Name.",isError=True)
		name = name.split(" ")[0]
		self.execSql(f"USE {name}")
		self.meta["dbName"] = name
		self.flags["layer"] = 1
	def checkSqlCache(self):
		if ";" in self.sqlCache:
			try:
				result = self.execSql(self.sqlCache)
				for i in result:
					print(i)
			except Exception as e:
				log(e, isError=True)
			self.flags["mode"] = "normal"
			self.sqlCache = ""
	def getPrompt(self):
		if self.flags["mode"] == "sql":
			promptLength = len(self.meta["host"]) + len(self.meta["dbName"]) + 1
			return "\r"+(" " * (promptLength - 3)) + "SQL >>>"
		if self.flags["layer"]:
			return parse(f"\r{self.meta['host']}/§b{self.meta['dbName']}§0 >>>")
		else:
			if self.meta["dbName"]:
				return parse(f"§b\r{self.meta['host']}§0/{self.meta['dbName']} >>>")
			else:
				return parse(f"§b\r{self.meta['host']}§0 >>>")
	def setCarrot(self,index):
		stdout.write(f"{self.getPrompt()}{self.command}")
		stdout.flush()
		stdout.write(f"{self.getPrompt()}{self.command[:self.commandCarrot]}")
		stdout.flush()
	def execute(self):
		while True:
			if self.flags["welcome"]:
				print("frSqlTools v1.0, developed by Frankium, impelemnted using fr-sh.")
				self.flags["welcome"] = False
				continue
			if not self.db:
				try:
					host, user, password = input(parse("Host §y>>§0 ")), input(parse("Username §y>>§0 ")), getpass.getpass(parse("Password §y>>§0 "))
					if not host.strip():
						log("Host cannot be empty.",isError=True)
						continue
					self.connect(host.strip(),user.strip(),password)
				except Exception as e:
					log(e,isError=True)
				except KeyboardInterrupt as k:
					log("Aborted",front="\n")
					self.stop()
			else:
				self.setCarrot(self.commandCarrot)
				k = GetKeyPress.listen()
				if k in Events.KEYPRESS_EVENTS:
					Events.KEYPRESS_EVENTS[k](self)
				elif (k.isprintable()) and (len(k) == 1):
					self.command = self.command[:self.commandCarrot] + k + self.command[self.commandCarrot:]
					self.commandCarrot += 1
			if self.flags["interpretBreak"]:
				break