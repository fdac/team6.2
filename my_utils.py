import subprocess

def get_disk_capacity():
	results = subprocess.check_output('df', shell=True)
	print results
