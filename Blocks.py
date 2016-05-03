import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import itertools 
import math as math
import numpy as np
import os



 
def read_File(alignment_file_name):
	''' Take the alignment file as input 
		and return a np.array with four lines 
		for each line of the alignment file: 
		Q_start, Q_end, S_start, S_end
	'''
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



def getBlocksTable(file_name,unfiltered=False,filtered=False):
	''' Take the alignment file as input, applies the read_File() fonction to get a matrix
		and then take out the noise (considered as noise when the length is too small)
	'''
	mat = read_File(file_name)
	#contient 4 lignes: qstart qend sstart send
	#Ordonne selon q_start

	#N colonnes dans le fichier (1 start/1end = 1 ligne)
	N = len(mat[0])
	#matrice filtree = sans bruit
	matf=[[] for i in range(4)]


	# plt.plot([mat[0], mat[1]],[mat[2], mat[3]], color = 'green')
	# plt.xlabel('Q')
	# plt.ylabel('S')
	# plt.savefig("Unfiltered")
	# plt.close()
	
	for i in range(N-1):
		#si suffisemment grand pour pas etre considere comme bruit pour paralogues = ceux dans la diago
		if math.sqrt(float((mat[0][i]-mat[1][i]))**2+float((mat[2][i]-mat[3][i]))**2) > 13000:
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


	# plt.xlabel('Q')
	# plt.ylabel('S')
	# plt.savefig("Filtered")
	# plt.close()
	return matf


def search_blocks(mat):
	''' Take the filtered matrix as input (without noise)
		and concatenate the alignment to make blocks
		Return an np.array with 5 lines : Q_start,Q_end,S_start, S_end, 
		and the type of the block (0 for paralogues, 1 for orthologues)
	'''
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
		if math.sqrt(float(mat[0][i]-mat[1][i])**2+float(mat[2][i]-mat[3][i])**2) > 100000:
			blocks_Q_start.append(mat[0][i])
			blocks_S_start.append(mat[2][i])
			while math.sqrt(float(mat[0][i]-mat[1][i])**2+float(mat[2][i]-mat[3][i])**2) > 100000 and (i < N-2) and (abs(mat[3][i+1] - mat[3][i]) < 300000):
					i = i+1
			blocks_Q_end.append(mat[1][i])
			blocks_S_end.append(mat[3][i])
			blocks_type.append(1)
		i = i +1


	blocks = np.array([blocks_Q_start,blocks_Q_end,blocks_S_start, blocks_S_end, blocks_type])
	for i in range(len(blocks[0])):
			plt.plot([blocks[0][i], blocks[1][i]],[blocks[2][i], blocks[3][i]],  color = 'red')
	#plt.show()
	return blocks

	


def isItInverted(blocks):
	''' Takes the blocks list as argument
		and returns a list of 'True' or 'False'
		depending on whether the block is inversed or not
	'''
	b = []
	nb_blocks = len(blocks[0])
	y1 = blocks[2]
	y2 = blocks[3]
	for i in xrange(nb_blocks):
		dy = y2[i]-y1[i]
		if dy<0:
			b.append(True)
		else:
			b.append(False)
	return b

def findNewOrder(blocks):
	''' Finds genes order in second chromosome
		and returns it as a list of indexes
	'''
	y1 = np.array(blocks[2])
	order = np.argsort(y1)
	return order


def geneList(blocks):
	''' Generates new list of genes (their original indexes)
		with their sign (- if inverted)
	'''
	genes = []
	inv = isItInverted(blocks)
	newList = findNewOrder(blocks)
	for i,b in enumerate(inv):
		if b==True:
			newList[i] = -newList[i]
	return newList


def save(blocks):
	''' Generates input file used for the calculation
		of the genomic distance
	'''
	f = open('input.txt','w')
	L0 = []
	L1 = (str(g) for g in geneList(blocks))
	for i in xrange(len(blocks[0])):
		L0.append('+'+str(i))
	f.write('('+' '.join(L0)+')\n')
	f.write('('+' '.join(L1)+')\n')
	f.close()
	print '\nInput file created.'


def main():
	'''Main call. Reads input and runs algorithm.'''

	B = getBlocksTable('Alignment.txt')
	blocks = search_blocks(B)

	save(blocks)
	print '...\n'


if __name__ == '__main__':
    main()


a=read_File('Alignment.txt')
print "a",a