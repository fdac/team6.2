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
			subprocess.call('rsync -ae "ssh -p 2200" ' + dirname + ' jduggan1@da2.eecs.utk.edu:repos', shell=True)
			subprocess.call('sudo rm -r ' + dirname + 'repos', shell=True)
			subprocess.call('sudo mkdir ' + dirname + 'repos', shell=True)
		except Exception:
			return

# call the given command and return the time it took to finish
def call_and_time(cmd):
	start = time.time()
	try:
		runner = subprocess.Popen(cmd, shell=True)
		runner.communicate()
	except Exception:
		pass
	return time.time() - start

def write_timing(fout, prefix):
	fout.write(prefix + ' wall time: ' + str(time.time() - start_time) + '\n')
	fout.write(prefix + ' hg time: ' + str(hg_time) + '\n')
	fout.write(prefix + ' git time: ' + str(git_time) + '\n')

# just your average declarations
git_time = 0
hg_time = 0
dirname = sys.argv[1]
process = dirname[-2]
todo = open(dirname + 'todo.csv', 'r')
output = open('timing_' + process + '.txt', 'w')
lines = todo.readlines()

start_time = time.time()
# loop through the repo list, cloning each of our repos
for line in lines:
	# grab the size, group, version control system, and repo name info from the files
	tokens = map(str.strip, line.split(','))
	size = int(tokens[0])
	vcs = tokens[1]
	team = tokens[2]
	name = tokens[3]

	# check the current amount of storage used, rsync if too much
	check_and_sync_storage(False)

	# clone the repo
	if vcs == 'hg':
		cmd = 'sudo hg clone -U https://bitbucket.org/{0}/{1} '.format(team, name) + dirname + 'repos/{0}_{1}'.format(team, name)
		elapsed = call_and_time(cmd)
		hg_time += elapsed
		write_timing(output, 'checkpoint')
	elif vcs == 'git':
		cmd = 'sudo git clone --mirror https://bitbucket.org/{0}/{1} '.format(team, name) + dirname + 'repos/{0}_{1}'.format(team, name)
		elapsed = call_and_time(cmd)
		git_time += elapsed
		write_timing(output, 'checkpoint')

# sync last pulls to storage
check_and_sync_storage(True)

# output final timing results
write_timing(output, 'final')

# clean-up
todo.close()
output.close()
