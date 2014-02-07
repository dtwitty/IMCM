from bs4 import BeautifulSoup
import urllib2
import re
import string
import json
from multiprocessing import Pool

def get_seasons(ext):
    ''' input: the first and last name of the coach
        output: a list of the coach's seasons'''
    url = "http://www.sports-reference.com%s" % ext
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    if not table: return []
    rows = table.findAll("tr")
    out = []
    for i in xrange(1, len(rows)):
        try:
            row = rows[i].findAll("td")
            if row[0].string.lower() == "career": break
            data = {}
            # year - year of season end
            data["year"] = int(row[0].string.split("-")[0]) + 1
            # school
            school_str = row[1].get_text(strip=True)
            match = re.match(r"([A-Z][a-z]*)(\*?) ?([RTFN]?)([RTFN]?)([RTFN]?)([RTFN]?)", school_str)
            data["school"] = match.groups()[0]
            data["ncaa_appearance"] = "*" in match.groups()
            data["conf_reg_win"] = "R" in match.groups()
            data["conf_tourn_win"] = "T" in match.groups()
            data["ff_appearance"] = "F" in match.groups()
            data["ncaa_win"] = "N" in match.groups()
            # games
            data["games"] = int(row[3].get_text())
            # wins
            data["wins"] = int(row[4].get_text())
            # losses
            data["losses"] = int(row[5].get_text())
            # srs
            data["srs"] = 0.0 if row[6].get_text() == "" else float(row[6].get_text())
            # sos
            data["sos"] = 0.0 if row[7].get_text() == "" else float(row[7].get_text())
            out.append(BasketballSeason(data))
        except Exception as e:
            print "Error on extension %s" % ext 
    return out

def get_coaches(letter):
    ''' input: the first letter of the last name
        output: a list of fully-defined coaches'''
    url = "http://www.sports-reference.com/cbb/coaches/%s-index.html" % letter
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    if not table: return []
    rows = table.findAll("tr")
    out = []
    for i in xrange(len(rows)):
        try:
            row = rows[i].findAll("td")
            if len(row) == 0: continue
            if not re.match(r"[0-9]*", row[0].string): continue
            data = {}
            # name
            name = re.sub(r"[^a-z ]", "", row[1].get_text().lower())
            print "new coach: %s" % name
            data["name"] = str(name)
            # seasons
            ext = row[1].findAll('a')[0].get('href')
            data["seasons"] = get_seasons(ext)
            # start year
            data["start_year"] = int(row[2].get_text())
            # end year
            data["end_year"] = int(row[3].get_text())
            # years active
            data["years_active"] = int(row[5].get_text())
            # games
            data["games"] = int(row[6].get_text())
            # wins
            data["wins"] = int(row[7].get_text())
            # losses
            data["losses"] = int(row[8].get_text())
            # regular conference wins
            data["conf_reg_wins"] = int(row[10].get_text())
            # tournament conference wins
            data["conf_tourn_wins"] = int(row[11].get_text())
            # ncaa appearances
            data["ncaa_appearances"] =  0 if row[12].get_text() == "" else int(row[12].get_text())
            # final four appearances
            data["ff_appearances"] = 0 if row[13].get_text() == "" else int(row[13].get_text())
            # ncaa wins
            data["ncaa_wins"] = 0 if row[13].get_text() == "" else int(row[13].get_text())
            out.append(BasketballCoach(data))
        except Exception as e:
            pass
    return out

class BasketballSeason:
    def __init__(self, data):
        self.year = int(data["year"])
        self.school = str(data["school"])
        self.games = int(data["games"])
        self.wins = int(data["wins"])
        self.losses = int(data["losses"])
        self.srs = float(data["srs"])
        self.sos = float(data["sos"])
        self.ncaa_appearance = bool(data["ncaa_appearance"])
        self.conf_reg_win = bool(data["conf_reg_win"])
        self.conf_tourn_win = bool(data["conf_tourn_win"])
        self.ff_appearance = bool(data["ff_appearance"])
        self.ncaa_win = bool(data["ncaa_win"])
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return str(self)

class BasketballCoach:
    def __init__(self, data):
        if type(data) == type(""):
            data = json.loads(data)
            data["seasons"] = [BasketballSeason(s) for s in data["seasons"]]
        self.name = str(data["name"])
        self.start_year = int(data["start_year"])
        self.end_year = int(data["end_year"])
        self.years_active = int(data["years_active"])
        self.games = int(data["games"])
        self.wins = int(data["wins"])
        self.losses = int(data["losses"])
        self.conf_reg_wins = int(data["conf_reg_wins"])
        self.conf_tourn_wins = int(data["conf_tourn_wins"])
        self.ncaa_appearances = int(data["ncaa_appearances"])
        self.ff_appearances = int(data["ff_appearances"])
        self.ncaa_wins = int(data["ncaa_wins"])
        self.seasons = data["seasons"]
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return str(self)

def load_data_file_basketball(outfilename = "bb_coaches.json"):
    out_dict = {"coaches" : []}
    pool = Pool(processes=16)
    unflat_list = pool.map(get_coaches, [chr(o) for o in xrange(ord('a'), ord('z') + 1)])
    for l in unflat_list:
        for coach in l:
            out_dict["coaches"].append(coach)
    with open(outfilename, 'w') as outfile:
        json.dump(out_dict, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=2)

def read_data_file_basketball(infilename = "bb_coaches.json"):
    with open(infilename, "r") as infile:
        bb = json.load(infile)
        coaches = map(BasketballCoach, bb["coaches"])
        return coaches

if __name__ == "__main__":
    load_data_file_basketball()
