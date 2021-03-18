from LaunchControls import InitialVariables
from os.path import isdir
from Interface import InterfaceControl,FrSqlTools
import Interface
import LanguageControls
import os
import DirControls

def getDefaultPath(path):
	cwd = os.getcwd()
	if path:
		if isdir(path):
			return path
		return cwd
	return cwd

def preInit():
	InitialVariables.read()

def init(mode,cwd):
	CWD = getDefaultPath(cwd)
	DirControls.updateCWDVars(CWD)
	# LanguageControls.VARIABLES["CWD"][1] = CWD
	# CWD = CWD.replace(os.path.expanduser("~"),"~")
	# LanguageControls.VARIABLES["SCWD"] = ["s",CWD]
	InterfaceControl.RegisterInterface(mode,FrSqlTools.FrSqlTools)
	Interface.MODE=mode

def launch():
	preInit()
	init("prompt",LanguageControls.VARIABLES["CWD"][1])

	#Launch Interface
	Interface.display()

def launchWithMode(mode):
	pass

def launchWithScript(filename):
	pass
