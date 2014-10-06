import subprocess
import time
import sys

# if storage is almost full or force is set to true, rsync
def check_and_sync_storage(force):
	threshold = 90 # corresponds to ~700 GB used on i2.xlarge
	try: results = subprocess.check_output('sudo df -kh /export', shell=True)
	except Exception: return
	used = int(results.split('\n')[1].split()[4].strip().rstrip('%')) # grab fifth element of 2nd line and toss pct symbol
	if used > threshold or force:
		try:
			subprocess.call('rsync -ae "ssh -p 2200" /export/repos jduggan1@da2.eecs.utk.edu:', shell=True)
			subprocess.call('sudo rm -r /export/repos', shell=True)
			subprocess.call('sudo mkdir /export/repos', shell=True)
		except Exception:
			return

# call the given command and return the time it took to finish
def call_and_time(cmd):
	start = time.time()
	try: subprocess.call(cmd, shell=True)
	except Exception: pass
	return time.time() - start

# just your average declarations
our_group = 6 # team 6 rulez!!1!!eleven!!!
git_time = 0
hg_time = 0

f1 = open('todo.csv', 'r')
output = open('output.txt', 'w')
lines = f1.readlines()

start_time = time.time()
# loop through the repo list, cloning each of our repos
for line in lines:
	# grab the size, group, version control system, and repo name info from the files
	tokens = map(str.strip, line.split(','))
	size = int(tokens[0])
	group = int(tokens[1])
	vcs = tokens[2]
	team = tokens[3]
	name = tokens[4]

	# check if the repo is our responsibility
	if group == our_group:
		# check the current amount of storage used, rsync if too much
		check_and_sync_storage(False)

		# clone the repo
		if vcs == 'hg':
			cmd = 'sudo hg clone -U https://bitbucket.org/{0}/{1} '.format(team, name) + '/export/repos/{0}_{1}'.format(team, name)
			elapsed = call_and_time(cmd)
			hg_time += elapsed
		elif vcs == 'git':
			cmd = 'sudo git clone --mirror https://bitbucket.org/{0}/{1} '.format(team, name) + '/export/repos/{0}_{1}'.format(team, name)
			elapsed = call_and_time(cmd)
			git_time += elapsed

# sync last pulls to storage
check_and_sync_storage(True)

# output timing results
output.write('wall time: ' + str(time.time() - start_time) + '\n')
output.write('hg time: ' + str(hg_time) + '\n')
output.write('git time: ' + str(git_time) + '\n')

# clean-up
f1.close()
output.close()
