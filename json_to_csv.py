from scrape_bb import read_data_file_basketball

coaches = read_data_file_basketball()

f = open("basketball_coach_career.csv", "w")

column_names = [name for name in coaches[0].__dict__]
for i in xrange(len(column_names)):
	column_name = column_names[i]
	if column_name == "seasons": continue
	f.write(column_name)
	if i != len(column_names) - 1: f.write(",")

for coach in coaches:
	f.write("\n")
	for i in xrange(len(column_names)):
		column_name = column_names[i]
		if column_name == "seasons": continue
		f.write(str(coach.__dict__[column_name]))
		if i != len(column_names) - 1: f.write(",")
f.close()

