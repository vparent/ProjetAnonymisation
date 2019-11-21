import time
import csv
import sys
import tt_test

def csv_getter(f):
    with open(f, 'r') as truth:
        reader = csv.DictReader(truth)
        rows = []
        for r in reader:
            rows.append(r)
    return rows


def change_row(rows, mrows, i, j, field_):
    mrows[i][field_].append(j)
    mrows[j][field_].append(i)
    temp = (rows[i][field_], mrows[i][field_])
    rows[i][field_], mrows[i][field_] = rows[j][field_], mrows[j][field_]
    rows[j][field_], mrows[j][field_] = temp
    return rows, mrows


def field_comp_sup_strict(r1, r2, field_):
    if field_ in ['date', 'price', 'qty']:
        return r1[field_] > r2[field_]
    else:  # field_ == 'hours'
        return r1[field_][:2] > r2[field_][:2] or r1[field_][-2:] > r2[field_][-2:]


def bubble_sort(rows, melted_rows, field_):
    for i in range(len(rows) - 1, 0, -1):
        for j in range(1, i):
            if field_comp_sup_strict(rows[j - 1], rows[j], field_):
                temp = rows[j - 1], melted_rows[j - 1]
                rows[j - 1], melted_rows[j - 1] = rows[j], melted_rows[j]
                rows[j], melted_rows[j] = temp
    return rows, melted_rows


def str_back(val):
    if val < 10:
        return '0' + str(val)
    else:
        return str(val)


def field_avg_of_2(r1, r2, field_):
    if field_ == 'price':
        return (r1[field_] + r2[field_]) / 2
    elif field_ == 'qty':
        return (r1[field_] + r2[field_]) // 2
    elif field_ == 'date':  # dates are in the sme month
        d1 = int(r1[field_][:-2])
        d2 = int(r2[field_][:-2])
        d = (d1 + d2) // 2
        return str_back(d)
    elif field_ == 'hours':
        h1 = (int(r1[field_][:2]), int(r1[field_][-2:]))
        h2 = (int(r2[field_][:2]), int(r2[field_][-2:]))
        t = (h1[0] + h2[0])
        th = t // 2
        mh = (h1[1] + h2[1]) // 2
        if t % 2 == 0:  # t pair
            h = (th, mh)
        elif mh % 30 != mh:  # mh >= 30 et t impair
            h = (th + 1, (mh - 30))
        else:
            h = (th, mh)
        return str_back(h[0]) + ":" + str_back(h[1])


def field_avg(rows, field_):
    if field_ in ['price', 'qty', 'date']:
        res = 0
        for r in rows:
            res +=  int(r[field_][:-2]) if field == 'date' else r[field_]
        if field_ == 'price':
            return res / len(rows)
        elif field_ == 'qty':
            return res // len(rows)
        else:
            return r[field_][-2:] + str_back(res)
    else:  # field_ == "hours"
        th = 0
        tm = 0
        for r in rows :
            th, tm = th + int(r[field_][:2]), int(r[field_][-2:])
        n = len(rows)
        h = th // n
        m = tm // n + int((th // n - h) * 60)
        return h + m // 60, m % 60


def mix_field(rows, melted_rows, field_, p):  # TODO finish this function
    q = 1 - p
    rows, melted_rows = bubble_sort(rows, melted_rows, field_)
    q1 = int(len(rows) * p)
    m = len(rows) // 2
    q3 = int(len(rows) * q)
    if len(rows) % 2 == 0:
        vq1 = rows[q1][field_]
        vm = field_avg([rows[m], rows[m + 1]], field_)
        vq3 = rows[q3][field_]
    else:  # len(rows)%2 == 1
        vq1 = field_avg([rows[q1], rows[q1 + 1]], field_)
        vm = rows[m][field_]
        vq3 = field_avg([rows[q3], rows[q3 + 1]], field_)
    # TODO mix val of field. /!\ mixer pour grandir (price, qty, ...) gauss ou l'élargir (date, hours)
    return rows, melted_rows


# main

# Debut du decompte du temps
start_time = time.time()

if not len(sys.argv) in range(2, 5) or (
        len(sys.argv) >= 4 and not (sys.argv[3] in ['date', 'hours', 'price', 'qty'])) or (
        sys.argv[1] == '--help'):  # between 2 and 4 arguments
    print("source.csv is needed ; others are optional ; field in ['date', 'hours', 'price', 'qty']\n it should be "
          "like :\n ./python .../gauss.py source.csv quartiles_per_centage field")
else:
    if len(sys.argv) >= 3:
        quartile_part = int(sys.argv[2])
    else:
        quartile_part = 0.1
    if len(sys.argv) >= 4:  # if field is not manage, it will be done on date
        field = sys.argv[3]
    else:
        field = 'date'

    file = sys.argv[1]
    rows_t = csv_getter(file)  # rows of thruth
    rows_m = []
    melted = []
    k = 0
    for row in rows_t:
        #melted.append(dict([('id_user', [k]), ('date', [k, k]), ('hours', [k]), ('id_item', [k]), ('price', [k]), ('qty', [k])]))  # making an array of modifications
        rows_m.append(row)
    #mix_field(rows_m, melted, field, quartile_part)

    statistics = tt_test.stats_targets(rows_m, ['date', 'hours'])
    print(statistics)
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
