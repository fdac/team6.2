import subprocess
import time

# just your average declarations
f1 = open('RepoSize.csv', 'r')
f2 = open('divided', 'r')
sizes = f1.readlines()
divided = f2.readlines()
our_group = 6
proc = 0
core = 0

output = open('todo.csv', 'w')

# loop through the repo list, cloning each of our repos
for i in range(len(sizes)):
	# grab the size, group, version control system, and repo name info from the files
	size = int(sizes[i].split(';')[0].strip())
	group,vcs,repo = map(str.strip, divided[i].split(';'))
	group = int(group)
	team,name = repo.split('/')

	# check if the repo is our responsibility
	if group == our_group:
		output.write('{0},{1},{2},{3},{4}\n'.format(str(size),str(group),vcs,team,name))

# clean-up
f1.close()
f2.close()
output.close()
