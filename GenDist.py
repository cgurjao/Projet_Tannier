from collections import defaultdict
import fileinput
from os import system
 
def two_break_dist(P, Q):
    '''Returns the 2-Break Distance of Chromosomes P and Q.'''
 
    # Construct the break point graph of P and Q.
    graph = defaultdict(list)
    for perm_cycle in P+Q:
        L = len(perm_cycle)
        for i in xrange(len(perm_cycle)):
            # Add the edge between consecutive items.
            # Note: Modulo L in the higher index for the edge between the last and first elements.
            graph[perm_cycle[i]].append(-1*perm_cycle[(i+1) % L])
            graph[-1*perm_cycle[(i+1) % L]].append(perm_cycle[i])
 
    # BFS to find the number of connected components in the breakpoint graph.
    component_count = 0
    remaining = set(graph.keys())
    while len(remaining) > 0:
        component_count += 1
        queue = [remaining.pop()]
        while queue:
            current = queue.pop(0)
            queue += filter(lambda node: node in remaining, graph.get(current, []))
            remaining -= set(queue)
 
    # Theorem: d(P,Q) = blocks(P,Q) - cycles(P,Q)
    return sum(map(len,P)) - component_count
 
 
def main():
    '''Main call. Reads input and runs algorithm.'''
    # Creates input file from Blocks.py
    system('python Blocks.py')
    # Read the input data.
    f = open('input.txt','r')
    P, Q = [line.strip().lstrip('(').rstrip(')').split(')(') for line in f]
    P = [map(int, block.split()) for block in P]
    Q = [map(int, block.split()) for block in Q]
 
    # Get the 2-Break Distance.
    dist = two_break_dist(P, Q)
 
    # Print the answer.
    print 'Minimum number of inversions: '+str(dist)+'\n'
    f.close()
 
if __name__ == '__main__':
    main()