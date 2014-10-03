import subprocess
import my_utils as mu

# just your average declarations
f1 = open('RepoSize.csv')
f2 = open('divided')
sizes = f1.readlines()
divided = f2.readlines()
our_group = 6 # team 6 rulez!!1!!eleven!!!

disk_used = 0
git_time = 0
hg_time = 0

mu.get_disk_capacity()

if len(sizes) != len(divided):
	print 'the two input files don\'t have the same number of lines!'
	exit(1)

for i in range(len(sizes)):
	# grab the size, group, version control system, and repo name info from the files
	size = int(sizes[i].split(';')[0].strip())
	group,vcs,repo = map(str.strip, divided[i].split(';'))
	group = int(group)
	team,name = repo.split('/')

	# if the repo is our responsibility, let's grab it
	if group == our_group:
		if vcs == 'git':
			cmd = 'git clone --mirror https://bitbucket.org/' + team + '/' + name
		elif vcs == 'hg':
			cmd = 'hg clone -U https://bitbucket.org/' + team + '/' + name
		#subprocess.call(cmd, shell=True)

# clean-up
f1.close()
f2.close()
