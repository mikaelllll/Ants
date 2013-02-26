#!/usr/bin/env python
from ants import *
import random
import pdb

f = open("o.txt", "w")

def println(m):
	for i in m:
		f.write(str(i)+" ")
	f.write("\n")
	f.flush()

class Ant:
	pos = None
	new_pos = None
	target = None
	direction = None
	group = None
	
	def __init__(self,ant):
		self.pos = ant
	
	def set_group(self,c):
		self.group = c
		
	def get_pos(self):
		return self.pos
	
	def get_new_pos(self):
		return self.new_pos
		
	def get_target(self):
		return self.target
	
	def set_target(self,target):
		self.target = target
	
	def get_direction(self):
		return selfdirection
	
	def get_group(self):
		return self.group
	
	def set_pos(self,pos):
		self.pos = pos
		
	def set_new_pos(self,pos):
		self.new_pos = pos


class TheBot:
	
	p_collectors = 0.7
	p_explorers = 0.3
	total = 1.
	collectors = 1.
	explorers = 1.
	ants_list = {}
	ants = None
	mapa = ""
	
	def set_mapa(self):
		mapa = self.ants.render_text_map()
		linhas = mapa.split("\n")[:-1]
		matriz = [list(linha[2:]) for linha in linhas]
		
		self.mapa = matriz
	
	def move_ants(self,source,target):
		def sum_tuple(a, b):
			return tuple((a[0]+b[0], a[1]+b[1]))
		
		def generate_kids(pos):
			temp = []
			
			for i in AIM.keys():
				aux = sum_tuple(pos, AIM[i])
				if aux[0] < len(self.mapa) and aux[1] < len(self.mapa[0]) and aux[0] >= 0 and aux[1] >= 0:
					
					
					
					#f.write(str(len(self.mapa))+" "+str(len(self.mapa[aux[0]]))+" "+str(aux)+"\n")
					#f.flush()
					
					p = self.mapa[aux[0]]
					
					if self.mapa[aux[0]][aux[1]] == "." or self.mapa[aux[0]][aux[1]] == "*":
						temp.append(aux)
			return temp
		
		passed_by = {}
		actual = source
		cost = self.ants.distance(source[0], source[1], target[0], target[1])
		next_pos = {}
		next_pos[source] = cost
		father = {}
		father[source] = None
		cont = 0
		target_kids = generate_kids(target)
		
		while(actual not in target_kids):
			passed_by[actual] = True
			
			for kid in generate_kids(actual):
				if kid not in passed_by and kid not in next_pos:
					father[kid] = actual
					next_pos[kid] = self.ants.distance(kid[0], kid[1], target[0], target[1])

			if len(next_pos) == 0:
				return 's'
			
			del next_pos[actual]
			
			aux = 999999
			for	pos in next_pos:
				if next_pos[pos] < aux:
					aux = next_pos[pos]
					actual = pos
			
			cont = cont+1
			if cont == 11:
				break
		
		temp = actual
		while father[father[temp]] != None:
			temp = father[temp]
		
		return self.ants.direction(source[0], source[1], temp[0], temp[1])
		
	def refresh(self):
		temp_list = {}
		self.ants_list = {}
		total = 0.
		collectors = 0.
		explorer = 0.
		
		for ant1 in self.ants.my_ants():
			found = False
			"""for ant_key in self.ants_list:
				ant2 = self.ants_list[ant_key]
				if ant1 == ant2.get_pos():
					temp_list[ant1] = ant2
					
					if ant2.get_group() == "collector":
						self.collectors += 1
					elif ant2.get_group() == "explorer":
						self.explorers += 1
					
					self.total += 1
					
					found = True
					break"""
			if not found:
				temp_ant = self.create_new_ant(ant1)
				temp_list[ant1] = temp_ant
		
		self.ants_list = temp_list
	
	def create_new_ant(self,ant):
		temp_ant = Ant(ant)
		if ((self.collectors / self.total) / self.p_collectors) < ((self.explorers / self.total) / self.p_explorers):
			temp_ant.set_group("collector")
		else:
			temp_ant.set_group("explorer")
			#temp_ant.set_group("collector")
		temp_ant.set_pos(ant)
		return temp_ant
	
	def get_collectors(self):
		ants = []
		for ant_key in self.ants_list:
			ant = self.ants_list[ant_key]
			if ant.get_group() == "collector":
				ants.append(ant)
		#endfor
		return ants
	
	def get_explorers(self):
		ants = []
		for ant_key in self.ants_list:
			ant = self.ants_list[ant_key]
			if ant.get_group() == "explorer":
				ants.append(ant)
		#endfor
		return ants
	
	def collector(self):
		list_food = self.ants.food()
		list_ants = self.get_collectors()
		
		while len(list_food) > 0 and len(list_ants) > 0:
			minimo = 10000000
			aux_food = -1
			aux_ants = -1
			for i in range(len(list_food)):
				for j in range(len(list_ants)):
					aux = self.ants.distance(list_food[i][0], list_food[i][1], list_ants[j].get_pos()[0], list_ants[j].get_pos()[1])
					if aux < minimo:
						minimo = aux
						aux_food = i
						aux_ants = j
				#endfor
			#endfor
			
			food = list_food.pop(aux_food)
			ant = list_ants.pop(aux_ants)
			#self.free_ants.remove(ant)
			
			target = self.ants.direction(ant.get_pos()[0], ant.get_pos()[1], food[0], food[1])
			
			self.ants_list[ant.get_pos()].set_new_pos(food)
			self.ants_list[ant.get_pos()].set_target(target)
			#endfor
		#endwhile
		for ant in list_ants:
			ant.set_group("explorer")
		return

	def explore(self):
		list_ants = self.get_explorers()
		
		println([ant.get_pos() for ant in list_ants])
		
		for ant in list_ants:
			target = []
			close = self.ants.closest_unseen(ant.get_pos()[0],ant.get_pos()[1])
			
			if close == None:
				close = self.ants.closest_enemy_hill(ant.get_pos()[0],ant.get_pos()[1])
			
			if close == None:
				close = self.ants.closest_enemy_ant(ant.get_pos()[0],ant.get_pos()[1])
			
			if close == None:
				println([ant.get_pos(),])
				target, close = self.get_pos_explore(ant.get_pos())
				close = (ant.get_pos()[0]+random.randint(0,5),ant.get_pos()[1]+random.randint(0,5))
			else:
				target = self.ants.direction(ant.get_pos()[0],ant.get_pos()[1],close[0],close[1])
			
			ant.set_target(target)
			ant.set_new_pos(close)
	
	def get_pos_explore(self, ant):
		x, y, cont = 0, 0, 0
		for antx in self.ants.my_ants():
			x = x + antx[0]
			y = y + antx[1]
			cont = cont + 1
		
		x = int(x / cont)
		y = int(y / cont)
		
		#println([(x, y), ant, self.ants_list[ant].get_group()])
		
		target = self.ants.direction(x, y, ant[0], ant[1])
		
		if len(target) == 0:
			target = AIM.keys()
		
		random.shuffle(target)
		
		println([target,(ant[0]+AIM[target[0]][0], ant[1]+AIM[target[0]][1]), ant])
		
		return (target, (ant[0]+AIM[target[0]][0], ant[1]+AIM[target[0]][1]))
	
	def move(self):
		orders = []
		
		for ant_key in self.ants_list:
		#for move in self.list_move:
			ant = self.ants_list[ant_key]
			move = (ant.get_pos(),ant.get_target())
			new_pos = None
			flag = True
			
			
			temp = self.move_ants(move[0],ant.get_new_pos())
			
			#for direction in move[1]:
			for direction in temp:
				
				new_pos = self.ants.destination(move[0][0], move[0][1], direction)
				if self.ants.unoccupied(new_pos[0], new_pos[1]) and self.ants.passable(new_pos[0], new_pos[1]) and new_pos not in orders:
					orders.append(new_pos)
					self.ants.issue_order((move[0][0], move[0][1], direction))
					flag = False
					break
				#endif
			#endfor
			
			if flag:
				if len(self.ants.my_hills()) > 0 and move[0] in self.ants.my_hills():
					for direction in ['n','w','s','e']:
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
	
	def do_turn(self, ants):
		println([" ",])
		self.ants = ants
		self.set_mapa()
		self.refresh()
		self.collector()
		self.explore()
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
