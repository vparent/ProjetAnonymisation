def stats(rows) :
    res = dict([('id_user', dict()), ('date', dict()), ('hours', dict()), ('id_item', dict()), ('price', dict()), ('qty', dict())])
    for r in rows:
        iu = r['id_user']
        d = r['date']
        h = r['hours']
        it = r['id_item']
        p = r['price']
        q = r['qty']
        if iu in res['id_user'].keys():
            res['id_user'][iu] += 1
        else:
            res['id_user'][iu] = 1
        if d in res['date'].keys():
            res['date'][d] += 1
        else:
            res['date'][d] = 1
        if h in res['hours'].keys():
            res['hours'][h] += 1
        else :
            res['hours'][h] = 1
        if it in res['id_item'].keys():
            res['id_item'][it] += 1
        else:
            res['id_item'][it] = 1
        if p in res['price'].keys():
            res['price'][p] += 1
        else:
            res['price'][p] = 1
        if q in res['qty'].keys():
            res['qty'][q] += 1
        else:
            res['qty'][q] = 1
    return res


def stats_targets(rows, list_fields):
    res = dict()
    for r in rows:
        temp = ""
        for f in list_fields:
            temp += str(r[f]) + ' '
        if temp in res.keys():
            res[temp] += 1
        else:
            res[temp] = 1
    return res