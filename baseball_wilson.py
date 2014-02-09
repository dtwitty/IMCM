from math import log, sqrt
from heapq import nlargest
def read_coaches(f = "baseball_coaches.csv"):
    with open(f, "r") as infile:
        it = iter(infile)
        colnames = it.next().strip().split(",")
        out = []
        for line in it:
            row = line.strip().split(",")
            data = {}
            for i in xrange(len(colnames)):
                colname = colnames[i]
                if row[i].isdigit():
                    data[colname] = int(row[i])
                else:
                    data[colname] = row[i]
            out.append(data)
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

def ci_lower_bound(pos, neg, confidence = 0.95):
    n = pos + neg
    if n == 0:
        return 0
    z = pnormaldist(1-confidence/2)
    phat = 1.0*pos/n
    return (phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def judge_coach(coach):
    return ci_lower_bound(coach["wins"], coach["losses"])

coaches = read_coaches()
bestn = nlargest(10, coaches, judge_coach)
for coach in bestn:
    print coach["name"], judge_coach(coach)
