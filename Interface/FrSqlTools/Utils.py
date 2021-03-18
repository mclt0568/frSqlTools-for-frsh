from ColorStr import parse

def log(*msgs,isError=False,front="",back=""):
	msg = ""
	for i in msgs:
		msg += f" {i}"
	print(parse(f"{front}[{'§rERR§0' if isError else '§gLOG§0'}] {msg}{back}"))