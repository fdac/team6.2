import subprocess
import time

# if storage is almost full or force is set to true, rsync
def check_and_sync_storage(force):
	threshold = 90 # corresponds to over 720 GB used on i2.xlarge
	try: results = subprocess.check_output('df -kh .', shell=True)
	except Exception: return
	used = int(results.split('\n')[1].split()[4].strip().rstrip('%')) # grab fifth element of 2nd line and toss all but the pct
	if used > threshold or force:
		try:
			subprocess.call('rsync -ae \'ssh -p2200\' ~/repos jduggan1@da2.eecs.utk.edu:', shell=True)
			subprocess.call('rm -r ~/repos', shell=True)
			subprocess.call('mkdir ~/repos', shell=True)
		except Exception:
			return

# call the given command and return the time it took to finish
def call_and_time(cmd):
	start = time.time()
	try: subprocess.call(cmd, shell=True)
	except Exception: pass
	return time.time() - start

# just your average declarations
f1 = open('RepoSize.csv')
f2 = open('divided')
sizes = f1.readlines()
divided = f2.readlines()
our_group = 6 # team 6 rulez!!1!!eleven!!!
git_time = 0
hg_time = 0

# some input error checking
if len(sizes) != len(divided):
	print 'the two input files don\'t have the same number of lines!'
	exit(1)

# loop through the repo list, cloning each of our repos
for i in range(len(sizes)):
	print i
	# grab the size, group, version control system, and repo name info from the files
	size = int(sizes[i].split(';')[0].strip())
	group,vcs,repo = map(str.strip, divided[i].split(';'))
	group = int(group)
	team,name = repo.split('/')

	if group == our_group:
		# check the current amount of storage used, rsync if too much
		check_and_sync_storage(False)

		if vcs == 'hg':
			cmd = 'hg clone -U https://bitbucket.org/{0}/{1} ~/repos/{0}_{1}'.format(team, name)
			elapsed = call_and_time(cmd)
			hg_time += elapsed
		elif vcs == 'git':
			cmd = 'git clone --mirror https://bitbucket.org/{0}/{1} ~/repos/{0}_{1}'.format(team, name)
			elapsed = call_and_time(cmd)
			git_time += elapsed

# sync last pulls to storage
check_and_sync_storage(True)

# output timing results
print 'hg time: ' + str(hg_time)
print 'git time: ' + str(git_time)

# clean-up
f1.close()
f2.close()
