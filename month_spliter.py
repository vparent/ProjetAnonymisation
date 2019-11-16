import csv

with open('ground_truth.csv') as truth:
    reader = csv.DictReader(truth)
    row1 = reader.__next__()
    temp = row1['date'][0:7]
    print(temp)
    i = 1
    month = []
    for row in reader:
        if row['date'][0:7] == temp:
            month.append(row)
        else:
            with open("ground_truth_month_"+str(i)+".csv", 'w') as writer:
                fields = ['id_user','date','hours','id_item','price','qty']
                mwriter = csv.DictWriter(writer, delimiter=',', fieldnames=fields)
                mwriter.writeheader()
                for r in month:
                    mwriter.writerow(r)
            month=[row]
            temp = row['date'][0:7]
            i += 1

