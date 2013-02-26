from ants import *
from random import shuffle

my_ants = {}

class NewBot:
	f = open("o.txt", "w")
	
	def do_turn(self, ants):
		for ant in ants.my_ants():
			
		
class Ant:
	pos = None
	new_pos = None
	
	def __init__(self, ant):
		self.pos = ant

if __name__ == '__main__':
	try:
		import psyco
		psyco.full()
	except ImportError:
		pass
	try:
		Ants.run(NewBot())
	except KeyboardInterrupt:
		print('ctrl-c, leaving ...')
