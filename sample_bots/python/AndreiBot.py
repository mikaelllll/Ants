#!/usr/bin/env python
from ants import *
from random import shuffle

class AndreiBot:
	f = open("o.txt", "w")
	
	def dist(self, a, b):
		return abs(a[0]-b[0]) + abs(a[1]-b[1])
	
	def move(self, ants, listMove):
		destinos = {}
		for ant, to in listMove:
			while len(to) > 0:
				novo = ants.destination(ant[0], ant[1], to[0])
				if ants.unoccupied(novo[0], novo[1]) and novo not in destinos:
					ants.issue_order((ant[0], ant[1], to[0]))
					break
				else:
					to.pop(0)
			#definir outra pos
			if len(to) == 0:
				to = ['n', 's', 'e', 'w']
				shuffle(to)
				listMove.append((ant, to))
	
	def do_turn(self, ants):
		listMove = []
		listFood = ants.food()
		listAnts = ants.my_ants()
		
		for hill in ants.enemy_hills():
			listFood.append(hill[0])
		
		while len(listFood) > 0 and len(listAnts) > 0: 
			minimo = 10000000
			auxX = -1
			auxY = -1
			for i in range(len(listFood)):
				for j in range(len(listAnts)):
					aux = self.dist(listFood[i], listAnts[j])
					if aux < minimo:
						minimo = aux
						auxX = i
						auxY = j
			
			food = listFood.pop(auxX)
			ant = listAnts.pop(auxY)
			
			to = []
			a, b = food
			
			if(ant[0] < a):
				to.append('s')
			if(ant[0] > a):
				to.append('n')
			if(ant[1] > b):
				to.append('w')
			if(ant[1] < b):
				to.append('e')
			
			listMove.append((ant, to))
			#endfor
		#endwhile
		
		for ant in listAnts:
			directions = AIM.keys()
			shuffle(directions)
			to = []
			to.append(directions[0])
			listMove.append((ant, to))
		#endfor
		
		self.move(ants, listMove)
		
if __name__ == '__main__':
	try:
		import psyco
		psyco.full()
	except ImportError:
		pass
	try:
		Ants.run(AndreiBot())
	except KeyboardInterrupt:
		print('ctrl-c, leaving ...')
