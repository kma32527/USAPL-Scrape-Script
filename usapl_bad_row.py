import csv

filename = 'usapl_data.csv'
with open(filename, 'r') as f:
    reader = csv.reader(f)
    raw_examples = list(reader)

for i in range(len(raw_examples)):
    if len(raw_examples[i]) == 22:
        print(raw_examples[i])