import sys
import LanguageControls
from Interface.FrSqlTools.Events import keyEvent
from ColorStr import parse

@keyEvent("Enter")
def Enter(ctx):
	print("")
	if ctx.command.strip():
		ctx.appendHistory(ctx.command,False)
	else:
		ctx.commandHistory.resetIndex()
	if (ctx.flags["mode"] == "sql"):
		ctx.sqlCache += ("\n" if ctx.sqlCache else "")
		ctx.sqlCache += ctx.command
		ctx.checkSqlCache()
	elif (ctx.flags["mode"] == "multi-sql"):
		ctx.multiSqlCache += ("\n" if ctx.multiSqlCache else "")
		ctx.multiSqlCache += ctx.command
		ctx.checkMultiSqlCache()
	else:
		ctx.execCmd(ctx.command)
	ctx.command = ""
	ctx.commandCarrot = 0

@keyEvent("Backspace")
def Backspace(ctx):
	ctx.clearCommandArea()
	sys.stdout.flush()
	if ctx.commandCarrot:
		ctx.command = ctx.command[:ctx.commandCarrot-1] + ctx.command[ctx.commandCarrot:]
		ctx.commandCarrot -= 1

@keyEvent("Ctrl_C")
def Ctrl_C(ctx):
	if ctx.command.strip():
		ctx.appendHistory(ctx.command,True)
	sys.stdout.write(parse(f"ƒw§k^C§0\n"))
	sys.stdout.flush()
	ctx.command = ""
	ctx.commandCarrot = 0

@keyEvent("Up")
def Up(ctx):
	ctx.clearCommandArea()
	ctx.command = ctx.commandHistory.getPrevHistory(False)[0]

@keyEvent("Ctrl_Up")
def Ctrl_Up(ctx):
	ctx.clearCommandArea()
	ctx.command = ctx.commandHistory.getPrevHistory(True)[0]

@keyEvent("Down")
def Down(ctx):
	ctx.clearCommandArea()
	ctx.command = ctx.commandHistory.getNextHistory(False)[0]

@keyEvent("Ctrl_Down")
def Ctrl_Down(ctx):
	ctx.clearCommandArea()
	ctx.command = ctx.commandHistory.getNextHistory(True)[0]

@keyEvent("Left")
def Left(ctx):
	if ctx.commandCarrot > 0:
		ctx.commandCarrot -= 1

@keyEvent("Right")
def Right(ctx):
	if ctx.commandCarrot < len(ctx.command):
		ctx.commandCarrot += 1