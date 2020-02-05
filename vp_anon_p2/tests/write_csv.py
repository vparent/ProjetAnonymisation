import csv
import sys

f = open("data/ground_truth.csv", "r")
reader = csv.DictReader(f)

data = [ line for line in reader ][0:10]

fo = open("test_copy_gt_py.csv", "w")
writer = csv.DictWriter(fo, fieldnames=list(data[0].keys()))

writer.writeheader()
writer.writerows(data)
