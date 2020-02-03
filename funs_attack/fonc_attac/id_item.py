from test2 import stats_targets_hours
from tt_test import month_translator


def return_index_id(dico, key, month, tab):
    id_ = dico[key][1][month]
    if id_ not in tab[0]:
        n = len(tab[0])
        for k in range(1, 14):
            tab[k].append([])
        tab[0].append(id_)
    else:
        n = tab[0].index(id_)
    return tab, n

def id_item(gt, s):
    res = [[] for k in range(14)]
    dicoA = stats_targets_hours(s)
    dicoT = stats_targets_hours(gt)
    res_tot_gt = [[] for k in range(14)]  # nb of key linked to the id_user in gt

    for key in dicoT.keys():
        if key in dicoA.keys():
            stemp = key.split()
            date = stemp[0]

            for m in range(len(dicoT[key][1])):
                y = month_translator(date)

                res_tot_gt, nn = return_index_id(dicoT, key, m, res_tot_gt)
                res_tot_gt[y][nn] += key

                res, n = return_index_id(dicoT, key, m, res)
                for v in dicoA[key][1]:
                    res[y][n].append(v)
    #print(res[0])
    result = [res[0]] + [[dict() for k in range(len(res[0]))] for l in range(13)]
    for i in range(1, 14):
        for j in range(len(res[0])):
            tmp = res[i][j]
            temp = []
            cnt = []
            if len(tmp) != 0:
                for e in tmp:
                    if e in temp:
                        cnt[temp.index(e)] += 1
                    else:
                        temp.append(e)
                        cnt.append(1)
                for k in range(len(temp)):
                    result[i][j][temp[k]] = cnt[k] / len(res_tot_gt[i][j]) * 100  # %age of (month, id_item) corresponding to this id_user
    return result


def id_item2(gt, s):
    return id_item(gt, s)