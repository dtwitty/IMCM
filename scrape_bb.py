from bs4 import BeautifulSoup
import urllib2
import re
import string


def get_seasons(first, last):
	''' input: the first and last name of the coach
		output: a list of the coach's seasons'''
	url = "http://www.sports-reference.com/cbb/coaches/%s-%s-1.html" % (first, last)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)
	table = soup.find("table")
	rows = table.findAll("tr")
	out = []
	for i in xrange(1, len(rows)):
		row = rows[i].findAll("td")
		if row[0].string.lower() == "career": break
		data = {}
		# year - year of season end
		data["year"] = int(row[0].string.split("-")[0]) + 1
		# school
		data["school"] = row[1].get_text(strip=True)
		# games
		data["games"] = int(row[3].get_text())
		# wins
		data["wins"] = int(row[4].get_text())
		# losses
		data["losses"] = int(row[5].get_text())
		# srs
		data["srs"] = float(row[6].get_text())
		# sos
		data["sos"] = float(row[7].get_text())
		out.append(BasketballSeason(data))
	return out

def get_coaches(letter):
	'''	input: the first letter of the last name
		output: a list of fully-defined coaches'''

class BasketballSeason:
	def __init__(self, data):
		self.year = data["year"]
		self.school = data["school"]
		self.games = data["games"]
		self.wins = data["wins"]
		self.losses = data["losses"]
		self.srs = data["srs"]
		self.sos = data["sos"]
	def __str__(self):
		return str(self.__dict__)
	def __repr__(self):
		return str(self)

class BasketballCoach:
	def __init__(self, data, seasons = []):
		self.name = data["name"]
		self.start_year = data["start_year"]
		self.end_year = data["end_year"]
		self.years_active = data["years_active"]
		self.games = data["games"]
		self.wins = data["wins"]
		self.losses = data["losses"]
		self.conf_reg_wins = data["conf_win"]
		self.conf_tourn_wins = data["cont_tourn_win"]
		self.ncaa_appearances = data["ncaa_appear"]
		self.ff_appearances = data["ff_appearances"]
		self.ncaa_wins = data["ncaa_wins"]
		self.seasons = seasons

print get_seasons("tom", "abatemarco")
