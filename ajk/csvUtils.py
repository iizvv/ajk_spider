import csv

def saveMsg(filename, msg):
    with open(filename + '.csv', 'a+', newline="") as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(msg)