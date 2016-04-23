import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import itertools 
import math as math
import numpy as np

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

def plot_DotPlot(file_name):
	mat = read_File(file_name)
	#contient 4 lignes: qstart qend sstart send
	#Ordonne selon q_start

	#N colonnes dans le fichier (1 start/1end = 1 ligne)
	N = len(mat[0])
	#matrice filtree = sans bruit
	matf=[[] for i in range(4)]


	#plt.plot([mat[0], mat[1]],[mat[2], mat[3]], color = 'green')
	#plt.xlabel('Q')
	#plt.ylabel('S')
	#plt.savefig("Unfiltered")
	#plt.close()
	
	for i in range(N-1):
		#si suffisemment grand pour pas etre considere comme bruit pour paralogues = ceux dans la diago
		if math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 13000:
			#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'red')
			matf[0].append(mat[0][i])
			matf[1].append(mat[1][i])
			matf[2].append(mat[2][i])
			matf[3].append(mat[3][i])

		#filtre orthologues
		if abs(mat[0][i]-mat[1][i+1]) > 1000:
			if abs(mat[2][i]-mat[3][i+1]) < 1000:
				#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'green')
				matf[0].append(mat[0][i])
				matf[1].append(mat[1][i])
				matf[2].append(mat[2][i])
				matf[3].append(mat[3][i])
		#else:
			#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'blue')


	plt.xlabel('Q')
	plt.ylabel('S')
	plt.savefig("Filtered")
	plt.close()
	return matf


def search_blocks(mat):
	N = len(mat[0])
	i = 0
	blocks_Q_start = []
	blocks_Q_end = []
	blocks_S_start = []
	blocks_S_end = []
	blocks_type = []
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


	i = 0
	while i < N-1:
		if math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 100000:
			blocks_Q_start.append(mat[0][i])
			blocks_S_start.append(mat[2][i])
			while math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 100000 and (i < N-2) and (abs(mat[3][i+1] - mat[3][i]) < 300000):
				i = i+1
			blocks_Q_end.append(mat[1][i])
			blocks_S_end.append(mat[3][i])
			blocks_type.append(0)
		i = i +1


	blocks = np.array([blocks_Q_start,blocks_Q_end,blocks_S_start, blocks_S_end])
	for i in range(len(blocks[0])):
		plt.plot([blocks[0][i], blocks[1][i]],[blocks[2][i], blocks[3][i]], color = 'red')
	plt.show()
	return blocks
	#### blocks contient:
	# - les quatres premières lignes sont respectivements Q_start, Q_end, S_start, S_end
	# - la dernière ligne décrit le type de bloc : 0 pour les paralogues et 1 pour les orthologues

m=plot_DotPlot('Alignment.txt')
search_blocks(m)