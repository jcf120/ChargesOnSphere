from math import *

# 3-fold symmetry tetrahedron potenial
def pot1(a,E):
	tot = 0.0
	tot += sqrt(3)/sin(a)
	tot += 3.0/sqrt(2.0-2.0*cos(a))
	tot += 3.0*E*(1.0-cos(a))
	return tot

# 2-fold symmetry tetrahedron potenial
def pot2(a,b,E):
	tot = 0.0
	tot += 2.0*sqrt(2.0)/sqrt(1-cos(a)*cos(b))
	tot += 0.5*((1.0/sin(a))+(1.0/sin(b)))
	tot += 2.0*E*(2.0-cos(a)-cos(b))
	return tot
	
# 4-fold symmetry square potenial
def pot3(a,E):
	tot = 0.0
	tot += (2.0*sqrt(2)+1.0)/sin(a)
	tot += 4.0*E*(1-cos(a))
	return tot


def min_index(data):
	m = 0
	for i in range(len(data)):
		if data[i] < data[m]:
			m = i
	return m


# function can search both pot1 and pot3 as they use one angle
def find_min_pot1or3(pot_func,E,n,d):
# n*n resolution
# d iteration depth
	
	a1 = 0.0001 # small, but not 0 to avoid divide by sin(0)
	a2 = pi - 0.0001 # avoid divide by sin(pi)
	
	for z in range(d):
		# determine range to search based on last search
		angles = [a1+(a2-a1)*(float(i)/float(n)) for i in range(0,n)]
		# find corresponding potentials
		pots = [pot_func(a,E) for a in angles]
		# find angle for lowest potential
		min_ang = min_index(pots)
		# store lowest and closest point
		low = pots[min_ang]
		# set new search range
		a1 = angles[min_ang]-(a2-a1)/n
		a2 = angles[min_ang]+(a2-a1)/n
	
	return low


def find_min_pot2(E,n,d):
# n*n resolution
# d iteration depth
	
	a1 = 0.0001 # small, but not 0 to avoid infinity
	a2 = pi - 0.0001 # avoid divide by sin(pi)
	b1 = 0.0001
	b2 = pi - 0.0001
	
	for z in range(d):
		# determine range to search based on last search
		alphas = [a1+(a2-a1)*(float(i)/float(n)) for i in range(0,n)]
		betas = [b1+(b2-b1)*(float(i)/float(n)) for i in range(0,n)]
		# find corresponding potentials
		pots = [[pot2(a,b,E) for a in alphas] for b in betas]
		# find angles for lowest potential
		min_a = 0
		min_b = 0
		for i in range(len(pots)):
			for j in range(len(pots[i])):
				if pots[i][j] < pots[min_b][min_a]:
					min_b = i
					min_a = j
		# store lowest
		low = pots[min_b][min_a]
		# set new search range
		a1 = alphas[min_a]-(a2-a1)/n
		a2 = alphas[min_a]+(a2-a1)/n
		b1 = betas[min_b]-(b2-b1)/n
		b2 = betas[min_b]+(b2-b1)/n
		
	return low

# find min pot1 pot2 intersect
def crossover12(acc,s,d):
	# set initial search range
	low = 0.0
	high = 1.5
	# repeat test until accuracy is reached
	while (high-low>acc):
		# check between known limits
		E = (low+high)/2
		p1 = find_min_pot1or3(pot1,E,s,d)
		p2 = find_min_pot2(E,s,d)
		# check for tranisition
		if p1<p2:
			low = E
		else:
			high = E
	return (low+high)/2

# find min pot2 pot3 intersect
def crossover23(acc,s,d):
	# set initial search range
	low = 0.0
	high = 1.5
	# repeat test until accuracy is reached
	while (high-low>acc):
		# check between known limits
		E = (low+high)/2
		p2 = find_min_pot2(E,s,d)
		p3 = find_min_pot1or3(pot3,E,s,d)
		# check for tranisition
		if p2<p3:
			low = E
		else:
			high = E
	return (low+high)/2

# find when min pot2 pot3 are indistinguishable
def indisting23(Eacc,Pacc,s,d):
	low = 0.0
	high = 1.5
	# repeat test until accuracy is reached
	while (high-low>Eacc):
		# check between known limits
		E = (low+high)/2
		p2 = find_min_pot2(E,s,d)
		p3 = find_min_pot1or3(pot3,E,s,d)
		# check indistinguishable
		if p3-p2>Pacc:
			low = E
		else:
			high = E
	return (low+high)/2