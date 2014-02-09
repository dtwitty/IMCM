import networkx as nx
from networkx import algorithms as alg
import re
import math

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

		f = open("basketball_playoff_games.txt", 'r')
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
				add_weight = math.log(1 + 0.1 * new_diff)
				if self.G.get_edge_data(winner_index, loser_index):
					rev_weight = self.G[winner_index][loser_index]['weight']
					if rev_weight > add_weight:
						self.G[winner_index][loser_index]['weight'] -= add_weight
					elif rev_weight == add_weight:
						self.G.remove_edge(winner_index, loser_index)
					else:
						self.G.remove_edge(winner_index, loser_index)
						self.G.add_edge(loser_index, winner_index, weight=(add_weight - rev_weight))
				elif self.G.get_edge_data(loser_index, winner_index):
					self.G[loser_index][winner_index]['weight'] += add_weight
				else:
					self.G.add_edge(loser_index, winner_index, weight=add_weight)
		print len(self.G.nodes())
		print len(self.G.edges())
		print(nx.number_weakly_connected_components(self.G))

	def coach_rank(self, top_k):
		result = alg.pagerank(self.G, alpha=0.95)
		result_arr = sorted((result[k], k) for k in result.keys())[::-1]
		self.write_result(result_arr)
		result_arr = result_arr[:top_k]
		
		for v, k in result_arr:
			s1 = 0
			for i, j in self.G.in_edges(k):
				s1 += self.G[i][j]['weight']
			s2 = 0
			for i, j in self.G.out_edges(k):
				s2 += self.G[i][j]['weight']
			# print len(self.G.out_edges(k))
			# print len(self.G.in_edges(k)) - len(self.G.out_edges(k))
			print self.reverse_map[k], k, v, s1 - s2

	def write_result(self, arr):
		f = open("wenhai_basketball_result.csv", "w")
		for k, v in arr:
			f.write("%s,%f\n" % (self.reverse_map[v], k))
		f.close()

Coachrank()
