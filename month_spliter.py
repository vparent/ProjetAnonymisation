import csv
import sys
from gauss import write_file


def write_file_month(f, j, m):
    write_file(f[:-4] + "_month_" + str(j), m, ['id_user', 'date', 'hours', 'id_item', 'price', 'qty'])
    return

"""
Get the csv file puted in arguments and creates 1 csv file for each months
"""
if __name__ == "__main__":
    if not len(sys.argv) in [2, 3]:
        print("source.csv is needed, others are optional :\n./python .../month_spliter.py source.csv nb_month_to_export")
    else:
        if len(sys.argv) == 3:
            k = int(sys.argv[2])
        else:
            k = 0
        print(k)
        file = sys.argv[1]

        with open(file, 'r') as truth:
            reader = csv.DictReader(truth)
            row1 = reader.__next__()
            temp = row1['date'][0:7]
            i = 1
            month = [row1]
            for row in reader:
                if row['date'][0:7] == temp:
                    month.append(row)
                else:
                    write_file_month(file, i, month)
                    month = [row]
                    temp = row['date'][0:7]
                    i += 1
                    if k != 0 and i > k:
                        break
        if k == 0 or i <= k:
            write_file_month(file, i, month)
