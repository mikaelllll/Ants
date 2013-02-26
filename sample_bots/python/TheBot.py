#!/usr/bin/env python
from ants import *
from random import shuffle

class Ant:
	pos = None
	new_pos = None
	direction = None
	group = None
	
	def __init__(self, ant):
		aux = None
		if ant not in self.ant_data:
			aux = self.define_group()
			#self.list_move.append((ant, AIM.keys()))
		else:
			aux = self.ant_data[ant]
		self.ant_data[ant] = aux
	
	def define_group(self):
		return ("collector",)
	
	
	

class TheBot:
	#nosso debugador temporario
	f = open("o.txt", "w")
	#chave = posicao atual, valor = tupla <classe ant, tupla de dados>
	ant_data = {}
	#(ant, target) para move as formigas
	list_move = []
	#formigas livres, sem movimento no turno
	free_ants = []
	#referencia a engine do jogo
	ants = None
	ants_list = {}
	
	def get_collectors(self):
		ants = []
		for ant in self.free_ants:
			if self.ant_data[ant][0] == "collector":
				ants.append(ant)
		#endfor
		return ants
	
	#recebe uma lista de formigas e manda elas explorarem o mapa
	def ant_search_food(self, ants):		
		#se afastando das formigas amigas
		x, y, cont = 0, 0, 0
		for ant in self.ants.my_ants():
			x = x + ant[0]
			y = y + ant[1]
			cont = cont + 1
		
		x = int(x / cont)
		y = int(y / cont)
		
		for ant in ants:
			target = self.ants.direction(x, y, ant[0], ant[1])
			#e se nao conseguir ir, tenta ir por um lado aleatprio que nao seja voltar para o formigueiro
			if target == 'n' or target == 's':
				aux = ('e', 'w')
				shuffle(aux)
				target = (target, aux[0], aux[1])
			if target == 'w' or target == 'e':
				aux = ('n', 's')
				shuffle(aux)
				target = (target, aux[0], aux[1])
			
			self.list_move.append((ant, target))
		#endfor
		return
	
	#define oq as formigas coletoras farao
	def collector(self):
		list_food = self.ants.food()
		list_ants = self.get_collectors()
		
		while len(list_food) > 0 and len(list_ants) > 0:
			minimo = 10000000
			aux_food = -1
			aux_ants = -1
			for i in range(len(list_food)):
				for j in range(len(list_ants)):
					aux = self.ants.distance(list_food[i][0], list_food[i][1], list_ants[j][0], list_ants[j][1])
					if aux < minimo:
						minimo = aux
						aux_food = i
						aux_ants = j
				#endfor
			#endfor
			
			food = list_food.pop(aux_food)
			ant = list_ants.pop(aux_ants)
			self.free_ants.remove(ant)
			
			target = self.ants.direction(ant[0], ant[1], food[0], food[1])

			self.list_move.append((ant, target))
			#endfor
		#endwhile
		return
	
	#move todas formigas, evitando colisoes. obs: se o movimento causar colisao entao nao se move
	def move(self):
		orders = []
		
		for move in self.list_move:
			new_pos = None
			flag = True
			
			for direction in move[1]:
				new_pos = self.ants.destination(move[0][0], move[0][1], direction)
				if self.ants.unoccupied(new_pos[0], new_pos[1]) and self.ants.passable(new_pos[0], new_pos[1]) and new_pos not in orders:
					orders.append(new_pos)
					self.ants.issue_order((move[0][0], move[0][1], direction))
					flag = False
					break
				#endif
			#endfor
			
			if flag:
				orders.append(move)
		#endfor
		return
	
	#metodo "main" para cada turno
	def do_turn(self, ants):
		self.list_move = []
		self.ants = ants
		
		for ant in self.ants.my_ants():
			if self.ants_list
			self.ants_list[ant] = Ant(ant)
		
		self.collector()
		self.ant_search_food(self.free_ants)
		self.move()

#default
if __name__ == '__main__':
	try:
		import psyco
		psyco.full()
	except ImportError:
		pass
	try:
		Ants.run(TheBot())
	except KeyboardInterrupt:
		print('ctrl-c, leaving ...')
