import string
import heapq
from math import sqrt, log
class Coach:
    def __init__(self, d):
        self.id = d["coachid"]
        self.firstname = d["firstname"]
        self.lastname = d["lastname"]
        self.season_win = int(d["season_win"])
        self.season_loss = int(d["season_loss"])
        self.playoff_win = int(d["playoff_win"])
        self.playoff_loss = int(d["playoff_loss"])

    def total_win(self):
        return self.playoff_win + self.season_win

    def total_loss(self):
        return self.playoff_loss + self.season_loss

    def total_avg(self):
        if self.total_win() == 0:
            return -float("inf")
        return float(self.total_win() + self.total_loss()) / self.total_win()

    def __str__(self):
        return "(%s %s, %d, %d, %d, %d)" % \
        (self.firstname, \
        self.lastname, \
        self.season_win, \
        self.season_loss, \
        self.playoff_win, \
        self.playoff_loss)

def read_csv(filename):
    f = open(filename, 'r')
    categories = ''.join(filter(lambda x: x in string.printable, f.next().strip())).split(",")
    out = []
    for l in f:
        line = l.strip().split(",")
        out.append(Coach({categories[i] : line[i] for i in range(len(line))}))
    return out

def pnormaldist(qn):
    b = [1.570796288, 0.03706987906, -0.8364353589e-3,
         -0.2250947176e-3, 0.6841218299e-5, 0.5824238515e-5,
         -0.104527497e-5, 0.8360937017e-7, -0.3231081277e-8,
         0.3657763036e-10, 0.6936233982e-12]
 
    if qn < 0.0 or 1.0 < qn:
        sys.stderr.write("Error : qn <= 0 or qn >= 1  in pnorm()!\n")
        return 0.0
 
    if qn == 0.5:
        return 0.0
 
    w1 = qn
 
    if qn > 0.5:
        w1 = 1.0 - w1
 
    w3 = -log(4.0 * w1 * (1.0 - w1))
    w1 = b[0]
 
    for i in range(1, 10):
        w1 += b[i] * w3**i
 
    if qn > 0.5:
        return sqrt(w1 * w3)
 
    return -sqrt(w1 * w3)

def ci_lower_bound(coach, confidence = 0.95):
    pos = coach.total_win()
    neg = coach.total_loss()
    n = pos + neg
    if n == 0:
        return 0
    z = pnormaldist(1-confidence/2)
    phat = 1.0*pos/n
    return (phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

coaches = read_csv('coaches_career.csv')

# filter out non-playoff-winning coaches
coaches = filter(lambda c : c.playoff_win > 0, coaches)

for coach in heapq.nlargest(100, coaches, ci_lower_bound):
    print coach