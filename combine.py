import subprocess
import time

# just your average declarations
f1 = open('RepoSize.csv', 'r')
f2 = open('divided', 'r')
sizes = f1.readlines()
divided = f2.readlines()
our_group = 6
process = 0
outs = []

for i in range(4):
	outs.append(open('/export/repos/' + str(i) + '/todo.csv', 'w'))

# loop through the repo list, grabbing each of our repos
for i in range(len(sizes)):
	# grab the size, group, version control system, and repo name info from the files
	size = int(sizes[i].split(';')[0].strip())
	group,vcs,repo = map(str.strip, divided[i].split(';'))
	group = int(group)
	team,name = repo.split('/')

	# check if the repo is our responsibility
	if group == our_group:
		outs[process].write('{0},{1},{2},{3}\n'.format(str(size),vcs,team,name))
		process = (process + 1) % 4

# clean-up
f1.close()
f2.close()
fout.close()
