import networkx as nx
from networkx import algorithms as alg
import re

def parse_tuple(s):
	match = re.match(r"\('(.*)', (.*), '(.*)', (.*)\)", s)
	groups = match.groups()
	winner = groups[0]
	winning_score = int(groups[1])
	loser = groups[2]
	losing_score = int(groups[3])
	return winner, winning_score, loser, losing_score

class Coachrank():
	def __init__(self):
		self.build_graph()
		self.coach_rank(5)

	def build_graph(self):
		self.coach_map = {}
		self.reverse_map = {}
		self.G = nx.DiGraph()

		f = open("football_games.txt", 'r')
		for line in f:
			winner, winning_score, loser, losing_score = parse_tuple(line)
			if winner not in self.coach_map:
				winner_index = len(self.coach_map)
				self.coach_map[winner] = winner_index
				self.reverse_map[winner_index] = winner
			else:
				winner_index = self.coach_map[winner]

			if loser not in self.coach_map:
				loser_index = len(self.coach_map)
				self.coach_map[loser] = loser_index
				self.reverse_map[loser_index] = loser
			else:
				loser_index = self.coach_map[loser]

			new_diff = winning_score - losing_score
			if new_diff > 0:
				# # 1 as edge weight
				self.G.add_edge(loser_index, winner_index, weight=1)

				# # min test score difference as edge weight
				# if self.G.get_edge_data(loser_index, winner_index):
				# 	old_diff = self.G[loser_index][winner_index]['weight']
				# 	self.G[loser_index][winner_index]['weight'] = min(old_diff, new_diff)
				# else:
				# 	self.G.add_edge(loser_index, winner_index, weight=new_diff)

	def coach_rank(self, top_k):
		result = alg.pagerank(self.G, alpha=0.95)
		result_arr = sorted((result[k], k) for k in result.keys())[::-1][:top_k]
		for v, k in result_arr:
			print self.reverse_map[k], v


Coachrank()
