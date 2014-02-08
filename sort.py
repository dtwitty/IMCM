THRESHOLD = 5 # At least k games in a season to be considered

class Sorter():
	def __init__(self):
		self.read_data()

	def best_k(self, arr, k):
		return sorted(range(len(arr)), key=lambda i:arr[i])[::-1][:k]

	def read_data(self):
		lines = []
		f = open("coaches_data.csv", 'r')
		f.readline()
		self.coach_map = {}
		self.reverse_map = {}
		for line in f:
			line = line.replace("\n", "")
			toks = line.split(",")
			toks[0] = toks[0].upper()
			if len(toks) == 10:
				coach_id, y, yr, firstname, lastname, sw, sl, pw, pl, t = toks
				games_played = int(sw) + int(sl) + int(pw) + int(pl)
				if games_played > THRESHOLD:
					lines.append(toks)
					if coach_id not in self.coach_map:
						index = len(self.coach_map)
						self.coach_map[coach_id] = {"index": index, "firstname": firstname, "lastname": lastname}
						self.reverse_map[index] = coach_id

		self.agg_win = [0] * len(self.coach_map)
		self.agg_loss = [0] * len(self.coach_map)
		self.agg_season_win = [0] * len(self.coach_map)
		self.agg_season_loss = [0] * len(self.coach_map)
		self.agg_playoff_win = [0] * len(self.coach_map)
		self.agg_playoff_loss = [0] * len(self.coach_map)

		for coach_id, _, _, _, _, s_win, s_loss, p_win, p_loss, _ in lines:
			index = self.coach_map[coach_id]["index"]

			self.agg_win[index] += int(s_win) + int(p_win)
			self.agg_loss[index] += int(s_loss) + int(p_loss)
			self.agg_season_win[index] += int(s_win)
			self.agg_season_loss[index] += int(s_loss)
			self.agg_playoff_win[index] += int(p_win)
			self.agg_playoff_loss[index] += int(p_loss)

	def print_result(self, best_coaches):
		for coach_index in best_coaches:
			coach_id = self.reverse_map[coach_index]
			print coach_id, self.coach_map[coach_id]["firstname"], self.coach_map[coach_id]["lastname"],
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
print "=================LEXI WIN/LOSS RATIO SORT========================"
sorter.lexi_ratio_sort(5)
print "=================LEXI NET WIN SORT========================"
sorter.lexi_win_sort(5)