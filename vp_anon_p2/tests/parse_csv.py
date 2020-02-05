import csv
import sys

f = open("data/ground_truth.csv", "r")
reader = csv.DictReader(f)

data = [ line for line in reader ]
