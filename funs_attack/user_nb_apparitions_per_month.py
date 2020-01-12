from test2 import stats_targets, date_month, split_stats_target
from tt_test import month_translator


def user_nb_apparitions_per_month(gt, s):
    list_fields = ['id_user', 'date']
    f = lambda x: stats_targets(x, list_fields, fun_date=date_month)
    dicoA = f(s)
    dicoT = f(gt)

    resA = split_stats_target(dicoA)
    resT = split_stats_target(dicoT)

    res = [[] for k in range(14)]
    nbs = [[] for k in range(14)]
    for r in resT:
        if r['id_user'] not in res[0]:
            n = len(nbs[1])
            res[0].append(r['id_user'])
            for i in range(1, 14):
                res[i].append(dict())
                nbs[i].append(0)
        else:
            n = res[0].index(r['id_user'])
        y = month_translator(r['date'])
        nbs[n][y] += r['nb']
    for r in resA:
        y = month_translator(r['date'])
        for i in range(len(res[0])):
            res[y][i][r['id_user']] = r['nb'] / nbs[y][i] * 100
    return res



