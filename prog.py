import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import itertools 
import math as math
import numpy as np


#Read alignment file and return a list with Q_start,Q_end, S_start and S_end
def read_File(file_name):
	Q_start = []
	Q_end = []
	S_start = []
	S_end = []
	with open(file_name) as inf:
		for line in inf:
			parts = line.split()
			li=line.strip()
			if not li.startswith("#"):
				if len(parts) > 1:
					Q_start.append(int(parts[6]))
					Q_end.append(int(parts[7]))
					S_start.append(int(parts[8]))
					S_end.append(int(parts[9]))
		a = np.array([Q_start,Q_end,S_start, S_end])
		a = a[:,a[1,:].argsort()]
	return a
	#table with four lines with Q_start,Q_end, S_start and S_end sorted according to Q_start


def plot_DotPlot(file_name):
	mat = read_File(file_name)
	N = len(mat[0])
	matf=[[] for i in range(4)]


	#To plot Unfiltered raw dot plot
	"""plt.plot([mat[0], mat[1]],[mat[2], mat[3]], color = 'green')
	plt.xlabel('Q')
	plt.ylabel('S')
	plt.savefig("Unfiltered") 
	plt.close()"""
	
	for i in range(N-1):
		#Look for paralogs
		if math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 13000:
			#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'red')
			matf[0].append(mat[0][i])
			matf[1].append(mat[1][i])
			matf[2].append(mat[2][i])
			matf[3].append(mat[3][i])

		#look for orthologs
		if abs(mat[0][i]-mat[1][i+1]) > 1000:
			if abs(mat[2][i]-mat[3][i+1]) < 1000:
				#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'green')
				matf[0].append(mat[0][i])
				matf[1].append(mat[1][i])
				matf[2].append(mat[2][i])
				matf[3].append(mat[3][i])

	#Plot filtered Dot plot without noise
	"""plt.xlabel('Q')
	plt.ylabel('S')
	plt.savefig("Filtered") 
	plt.close()"""
	return matf
	#table with four lines with Q_start,Q_end, S_start and S_end sorted according to Q_start

#Merge blocks 
def search_blocks(mat):
	N = len(mat[0])
	blocks_Q_start = []
	blocks_Q_end = []
	blocks_S_start = []
	blocks_S_end = []
	blocks_type = []

	#Merge neighboor paralogs into a single block
	i = 0
	while i < N-1:
		if abs(mat[0][i+1] - mat[0][i]) < 2000:
			blocks_Q_start.append(mat[0][i])
			blocks_S_start.append(mat[2][i])
			while (abs(mat[0][i+1] - mat[0][i]) < 15000)  and (abs(mat[3][i+1] - mat[3][i]) < 200000) and (i < N-2):
				i = i+1
			blocks_Q_end.append(mat[1][i])
			blocks_S_end.append(mat[3][i])
			blocks_type.append(0)
		i = i +1

	#Merge neighboor orthologs into a single block
	i = 0
	while i < N-1:
		if math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 100000:
			blocks_Q_start.append(mat[0][i])
			blocks_S_start.append(mat[2][i])
			while math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 100000 and (i < N-2) and (abs(mat[3][i+1] - mat[3][i]) < 300000):
				i = i+1
			blocks_Q_end.append(mat[1][i])
			blocks_S_end.append(mat[3][i])
			blocks_type.append(1)
		i = i +1


	blocks = np.array([blocks_Q_start,blocks_Q_end,blocks_S_start, blocks_S_end, blocks_type])

	f=open("filtered_merged_blocks.txt","w")

	#To plot blocks and save it in a file
	for i in range(len(blocks[0])):
		plt.plot([blocks[0][i], blocks[1][i]],[blocks[2][i], blocks[3][i]],  color = 'red')
		f.write("%d\t%d\t%d\t%d\n"%(blocks[0][i],blocks[1][i],blocks[2][i],blocks[3][i]))

	f.close()
	
	plt.xlabel('Q')
	plt.ylabel('S')
	plt.savefig("Filtered_merged_blocks") #Plot filtered Dot plot without noise
	plt.close()
	return blocks
	#### blocks is a table with:
	# - The four first lines are Q_start, Q_end, S_start, S_end
	# - the last line describe the type of block : 0 for paralogues and 1 for orthologs

m=plot_DotPlot('Alignment.txt')
search_blocks(m)
