from LaunchControls.InitialVariables import read
from Interface.FrSqlTools.Utils import log
from Interface.GetKeyPress import listen
from ColorStr import parse
import sys

COMMANDS = {}

def command(name):
	def wrapper(func):
		COMMANDS[name] = func
	return wrapper

@command("exit")
def exit(client,args):
	client.stop()

@command("ld")
def ld(client,args):
	result = client.fetchDatabases()
	outputs = ""
	for i in result:
		if i in ("information_schema","mysql","performance_schema","phpmyadmin"):
			outputs += f"§G{i}§0    "
		else:
			outputs += f"{i}    "
	print(parse(outputs))

@command("lt")
def lt(client,args):
	try:
		result = client.fetchTables()
		outputs = ""
		for i in result:
			outputs += f"{i}    "
		print(parse(outputs))
	except Exception as e:
		log(e,isError=True)

@command("ls")
def ls(client,args):
	if client.flags["layer"]:
		client.execCmd("lt")
	else:
		client.execCmd("ld")

@command("use")
def use(client,args):
	if not args:
		log("Please specify the name of the database.",isError=True)
		return
	try:
		client.execSql(f"USE {args[0]}")
		client.meta["dbName"] = args[0]
		client.flags["layer"] = 1
	except Exception as e:
		log(e,isError=True)

@command("cd")
def cd(client,args):
	if (not client.meta["dbName"]) and (not args):
		print("You do not have any database selected.")
		return
	elif (args):
		client.execCmd(f"use {args[0]}")
		return
	if client.flags["layer"]:
		client.flags["layer"] = 0
	else:
		client.flags["layer"] = 1

@command("mkdb")
def lt(client,args):
	if not args:
		log("MKDB takes in 1 argument: Database Name", isError=True)
	try:
		client.execSql(f"CREATE DATABASE {args[0]}")
	except Exception as e:
		log(e,isError=True)

@command("rmdb")
def lt(client,args):
	if not args:
		log("RMDB takes in 1 argument: Database Name", isError=True)
	try:
		while True:
			sys.stdout.write(f"Are you sure to REMOVE DATABASE `{args[0]}`? [y/n]")
			sys.stdout.flush()
			key = listen()
			if key in ("y","Y"):
				print("")
				break
			if key in ("n", "N"):
				print("")
				return
			log(f"Unknown option: {key}",front="\n",isError=True)
		client.execSql(f"DROP DATABASE {args[0]}")
	except Exception as e:
		log(e,isError=True)

@command("`")
def cd(client,args):
	client.flags["mode"] = "sql"

@command("```")
def cd(client,args):
	client.flags["mode"] = "multi-sql"