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

	#N colonnes dans le fichier (1 start/1end = 1 ligne)
	N = len(mat[0])
	#matrice filtree = sans bruit
	matf=[[] for i in range(4)]


	#for i in range(N):
		#plt.plot([Q_start[i], Q_end[i]],[S_start[i], S_end[i]], color = 'blue')
		#plt.xlim()
		#plt.ylim()
	compt_bar_mont = 0
	compt_bar_desc = 0
	print mat
	for i in range(len(mat[0])-1):
		#si suffisemment grand pour pas etre considere comme bruit pour paralogues = ceux dans la diago
		if math.sqrt((mat[0][i]-mat[1][i])**2+(mat[2][i]-mat[3][i])**2) > 13000:
			#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'red')
			compt_bar_mont = compt_bar_mont +1

			matf[0].append(mat[0][i])
			matf[1].append(mat[1][i])
			matf[2].append(mat[2][i])
			matf[3].append(mat[3][i])

		#filtre orthologues
		if abs(mat[0][i]-mat[1][i+1]) > 1000:
			if abs(mat[2][i]-mat[3][i+1]) < 1000:
				#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'green')
				compt_bar_desc = compt_bar_desc +1

				matf[0].append(mat[0][i])
				matf[1].append(mat[1][i])
				matf[2].append(mat[2][i])
				matf[3].append(mat[3][i])
		#else:
			#plt.plot([mat[0][i], mat[1][i]],[mat[2][i], mat[3][i]], color = 'blue')


	# plt.xlabel('Q')
	# plt.ylabel('S')
	# plt.savefig("dotplot")
	#plt.show()
	print compt_bar_desc
	print compt_bar_mont
	return matf

plot_DotPlot('Alignment.txt')
