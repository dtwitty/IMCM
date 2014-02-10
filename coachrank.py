import networkx as nx
from networkx import algorithms as alg
import re
import math


start_year = 1800
end_year = 2100

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
		self.year_map = {}
		self.reverse_map = {}
		self.G = nx.DiGraph()


		yf = open("basketball_start_year.csv", "r")
		yf.readline()
		for line in yf:
			_, k, v = line.replace("\n", "").replace("\"", "").split(" ")
			self.year_map[k] = int(v)
		yf.close()

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
			if winner in self.year_map and loser in self.year_map:
				if start_year < self.year_map[winner] and self.year_map[winner] < end_year:
				 	if start_year < self.year_map[loser] and self.year_map[loser] < end_year:
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
		i = 1
		for k, v in arr:
			if self.reverse_map[v] in self.year_map:
				f.write("%d,%s,%d,%f\n" % (i, self.reverse_map[v], self.year_map[self.reverse_map[v]], k))
				i += 1
		f.close()

Coachrank()
