import re

def parse_tuple(s):
	match = re.match(r"\('(.*)', (.*), '(.*)', (.*)\)", s)
	groups = match.groups()
	winner = groups[0]
	winning_score = int(groups[1])
	loser = groups[2]
	losing_score = int(groups[3])
	return winner, winning_score, loser, losing_score

class Sorter():
	def __init__(self):
		self.read_data()

	def best_k(self, arr, k):
		return sorted(range(len(arr)), key=lambda i:arr[i])[::-1][:k]

	def read_data(self):
		lines = []
		self.coach_map = {}
		self.reverse_map = {}

		f = open("basketball_playoff_games.txt", 'r')
		for line in f:
			winner, winning_score, loser, losing_score = parse_tuple(line)
			if winner not in self.coach_map:
				winner_index = len(self.coach_map)
				self.coach_map[winner] = winner_index
				self.reverse_map[winner_index] = winner
			if loser not in self.coach_map:
				loser_index = len(self.coach_map)
				self.coach_map[loser] = loser_index
				self.reverse_map[loser_index] = loser
			lines.append((winner, winning_score, loser, losing_score))

		self.agg_win = [0] * len(self.coach_map)
		self.agg_loss = [0] * len(self.coach_map)
		self.agg_season_win = [0] * len(self.coach_map)
		self.agg_season_loss = [0] * len(self.coach_map)
		self.agg_playoff_win = [0] * len(self.coach_map)
		self.agg_playoff_loss = [0] * len(self.coach_map)

		for winner, winning_score, loser, losing_score in lines:
			winner_index = self.coach_map[winner]
			loser_index = self.coach_map[loser]

			self.agg_win[winner_index] += 1
			self.agg_loss[loser_index] += 1
			self.agg_playoff_win[winner_index] += 1
			self.agg_playoff_loss[loser_index] += 1


	def print_result(self, best_coaches):
		for coach_index in best_coaches:
			print self.reverse_map[coach_index],
			print self.agg_playoff_win[coach_index], self.agg_playoff_loss[coach_index],
			print self.agg_season_win[coach_index], self.agg_season_loss[coach_index]

	# Disadvantage
	# Some coach never even make once into playoff and win 5 season games then quit
	def agg_ratio_sort(self, k):
		agg_ratio = [float(x + 1)/float(y + 1) for x, y in zip(self.agg_win, self.agg_loss)]
		best_coaches = self.best_k(agg_ratio, 5)
		self.print_result(best_coaches)

	# Disadvantage
	# Old dudes have total advantage
	def agg_win_sort(self, k):
		net_win = [x - y for x, y in zip(self.agg_win, self.agg_loss)]
		best_coaches = self.best_k(net_win, 5)
		self.print_result(best_coaches)

	# Disadvantage:
	# Only playoffs matter
	# No weight on the number of playoffs played
	def lexi_ratio_sort(self, k):
		agg_playoff_ratio = [float(x + 1)/float(y + 1) for x, y in zip(self.agg_playoff_win, self.agg_playoff_loss)]
		agg_season_ratio = [float(x + 1)/float(y + 1) for x, y in zip(self.agg_season_win, self.agg_season_loss)]
		ratio_combined = zip(agg_playoff_ratio, agg_season_ratio)
		best_coaches = self.best_k(ratio_combined, 5)
		self.print_result(best_coaches)

	# Disadvantage:
	# Only playoffs matter
	# Old dudes have advantage (maybe justifiable? credentials? playoff wins?)
	def lexi_win_sort(self, k):
		net_playoff_win = [x - y for x, y in zip(self.agg_playoff_win, self.agg_playoff_loss)]
		net_season_win = [x - y for x, y in zip(self.agg_season_win, self.agg_season_loss)]
		ratio_combined = zip(net_playoff_win, net_season_win)
		best_coaches = self.best_k(ratio_combined, 5)
		self.print_result(best_coaches)

sorter = Sorter()
print "=================AGG WIN/LOSS RATIO SORT========================"
sorter.agg_ratio_sort(5)
print "=================AGG NET WIN SORT========================"
sorter.agg_win_sort(5)
# print "=================LEXI WIN/LOSS RATIO SORT========================"
# sorter.lexi_ratio_sort(5)
# print "=================LEXI NET WIN SORT========================"
# sorter.lexi_win_sort(5)