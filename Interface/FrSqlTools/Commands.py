from Interface.FrSqlTools.Utils import log
from ColorStr import parse

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

@command("USE")
def use(client,args):
	client.execCmd(f"use {' '.join(args)}")

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

@command("```")
def cd(client,args):
	if not client.meta["dbName"]:
		log("Please select a database before query.")
		return
	client.flags["mode"] = "sql"
		

