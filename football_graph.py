import networkx as nx
from bs4 import BeautifulSoup
import urllib2
import re
from multiprocessing import Pool

def get_link(s):
    return s.find_all('a')[0].get('href')

def get_coach_id(ext):
    url = "http://www.sports-reference.com" + ext
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    bold_coach = soup.findAll(text = "Coach:")[0]
    coach_tag = bold_coach.parent.parent
    coach_href = get_link(coach_tag)
    return str(coach_href).split("/")[-1].split(".")[0]

def parse_bowl_game(row):
    winner_tag = row[3]
    winner_ref = get_link(winner_tag)
    winner_coach = get_coach_id(winner_ref)
    winner_score = int(row[4].get_text())
    loser_tag = row[5]
    loser_ref = get_link(loser_tag)
    loser_coach = get_coach_id(loser_ref)
    loser_score = int(row[6].get_text())
    print (winner_coach, winner_score, loser_coach, loser_score)
    return (winner_coach, winner_score, loser_coach, loser_score)
    
def parse_all_games(bowl_ext):
    url = "http://www.sports-reference.com" + bowl_ext
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    if not table: return []
    rows = table.findAll("tr")
    out = []
    for i in xrange(len(rows)):
        try:
            row = rows[i].findAll("td")
            if len(row) <= 1: continue
            if not re.match(r"[0-9]*", row[0].string): continue
            out.append(parse_bowl_game(row))
        except Exception as e:
            pass
    return out

def parse_all_bowls():
    url = "http://www.sports-reference.com/cfb/bowls/"
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    rows = table.findAll("tr")
    out = []
    bowl_exts = []
    for i in xrange(len(rows)):
        row = rows[i].findAll("td")
        if len(row) == 0: continue
        if row[0].get_text == "Bowl": continue
        bowl_ext = get_link(row[0])
        bowl_exts.append(bowl_ext)
    pool = Pool(8)
    unflat = pool.map(parse_all_games, bowl_exts)
    for l in unflat:
        out.extend(l)
    return out

games = parse_all_bowls()
f = open("football_games.txt", "w")
for game in games:
    f.write(str(game))
    f.write("\n")
