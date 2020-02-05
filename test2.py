from gauss import *
from tt_test import month_translator


def date_month(date):
    return date[:-3]


def to_string(x):
    return str(x)


def stats_targets(rows, list_fields, fun_id_user=to_string, fun_date=to_string, fun_hours=to_string,
fun_id_item=to_string, fun_price=to_string, fun_qty=to_string):
    """
    DMA
    :param fun_id_user: function to modify all users with it
    :param fun_date: function to modify all dates with it
    :param fun_hours: function to modify all hours with it
    :param fun_id_item: function to modify all id_items with it
    :param fun_price: function to modify all prices with it
    :param fun_qty: function to modify all qty with it
    :param rows: (dict) rows of csv file
    :param list_fields: (list str) exact names of fields to compare
    :return: (dict) keys : values of fields sep ' ' ; values : times keys was encountred
    """
    res = dict()
    funs = dict([('id_user', fun_id_user), ('date', fun_date), ('hours', fun_hours),
                ('id_item', fun_id_item), ('price', fun_price), ('qty', fun_qty)])
    for r in rows:
        temp = ""
        for f in list_fields:
            temp += funs[f](r[f])
            temp += ' '
        if temp in res.keys():
            res[temp] += 1
        else:
            res[temp] = 1
    return res


def split_stats_target(dic, list_fields):
    res = []
    for r in dic.items():
        stemp = r[0].split()
        temp = dict()
        for i in range(len(list_fields)):
            temp[list_fields[i]] = stemp[i]
        temp['nb'] = r[-2]
        res += temp
    return res

def stats_targets_hours(rows, hours=False):
    """
    DMA
    date format change in AAAA/MM
    :param rows: (dict) rows of csv file
    :param list_fields: (list str) exact names of fields to compare
    :return: (dict) keys : values of fields sep ' ' ; values : times keys war encountred
    """
    if hours:
        list_fields = ['date', 'hours', 'id_item']
    else:
        list_fields = ['date', 'id_item']
    res = dict()
    for r_ in rows:
        temp_ = ""
        for f_ in list_fields:
            if f_ == 'date':
                temp_ += r_[f_][:-3]
            elif f_ == 'hours':
                temp_ += r_[f_][:3]
            else:
                temp_ += str(r_[f_])
            temp_ += ' '

        if temp_ in res.keys():
            res[temp_][0] += 1
            if r_['id_user'] in res[temp_][1]:
                k_ = res[temp_][1].index(r_['id_user'])
                res[temp_][2][k_] += 1
            else:
                res[temp_][1].append(r_['id_user'])
                res[temp_][2].append(1)
        else:
            res[temp_] = [1, [r_['id_user']], [1]]
    return res


"""
for i in range(1, 14):
    fil = f + str(i) + "_cpl" + ".csv"
    filt = ft + str(i) + "_cpl" + ".csv"
    rows = csv_getter(fil)
    rowst = csv_getter(filt)
    dicoA = stats_targets_hours(rows)
    dicoT = stats_targets_hours(rowst)
    for el in dicoA.items():
        if el[0] in dicoT.keys():
"""


def main_att(f, name):
    hours = True

    #f = "S_5IF_aboutis_at_2-date_sorted"
    ft = "ground_truth"

    fil = f
    rows = csv_getter(fil)
    dicoA = stats_targets_hours(rows, hours=hours)

    filt = ft + ".csv"
    rowst = csv_getter(filt)
    dicoT = stats_targets_hours(rowst, hours=hours)

    result = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for key in dicoT.keys():
        if key in dicoA.keys():
            stemp = key.split()
            date = stemp[0]

            for m in range(len(dicoT[key][1])):
                id_ = dicoT[key][1][m]
                if id_ not in result[0]:
                    n = len(result[0])
                    for k in range(1, 14):
                        result[k].append([])
                    result[0].append(id_)
                else:
                    n = result[0].index(id_)
                y = month_translator(date)
                for v in dicoA[key][1]:
                    result[y][n].append(v)

    result1 = [result[0]] + [['' for k in range(len(result[0]))] for l in range(13)]

    for i in range(1, 14):
        for j in range(len(result[0])):
            tmp = result[i][j]
            temp = []
            cnt = []
            if len(tmp) != 0:
                for e in tmp:
                    if e in temp:
                        cnt[temp.index(e)] += 1
                    else:
                        temp.append(e)
                        cnt.append(1)
                maxi = max(cnt)
                y = cnt.index(maxi)
                result1[i][j] = temp[y]
                cnt.pop(y)
                temp.pop(y)
    result1 = transpo_mat(result1)
    with open("res11_" + name + ".csv", 'w', newline='') as writer:
        wr = csv.writer(writer, quoting=csv.QUOTE_ALL)
        for r in result1:
            wr.writerow(r)
