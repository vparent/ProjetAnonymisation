import csv
from gauss import *
from tt_test import *
from test2 import *
import sys
import shutil
from stats1 import count_ids
"""
start_time = time.time()
file = "submission_steph.csv"
rows_steph = csv_getter(file)
rows_my, rows_del, rows_del_indices = get_deleted_lines(rows_steph)
rows_my = tt_test.shuffle_uniq_usr_item(rows_my, file)
rows_my = tt_test.smooth_half_hour(rows_my)
rows_my = merge_rows(rows_my, rows_del, rows_del_indices)
write_file("temp2", rows_my, fields_)
print("\n\nTemps d execution : %s secondes ---" % (time.time() - start_time))
"""
"""
f = "S_TMTM_submission_1-date_sorted_month_"
# fields = ['id_user', 'date', 'hours', 'id_item', 'price', 'qty']
for i in range(1, 14):
    fil = f + str(i) + ".csv"
    rows = csv_getter(fil)
    count_ids(rows, fil)
"""
start_time = time.time()
if len(sys.argv) == 1:
    print("use : creer : F_nom_equipe_numero-LCOINSTI.csv !!!!!!!!!!!!!!!!!!!!)")
    print("nom_equipe_numero == argv[2]")
    print("python test.py S_file.csv nom_equipe_numero")
    print("------------------------------------------------------------")
else:
    f = sys.argv[1]
    gpe_att = f[:-4]
    shutil.copyfile('ffile.csv', "F_" + gpe_att + "-LCOINSTI.csv")
    main_att(f, gpe_att)

    ffile_transloator("res11_" + gpe_att + ".csv", "F_" + gpe_att + "-LCOINSTI.csv")
    print("res = F_nom_equipe_numero-LCOINSTI.csv")
print("\n\nTemps d execution : %s secondes ---" % (time.time() - start_time))
# bin
"""
def order_fields(liste):
    temp = ['id_user', 'date', 'hours', 'id_item', 'price', 'qty']
    res = []
    for l in temp:
        if l in liste:
            res.append(l)
    return res

res = dicoA.items()
with open("tset_cpl_TMTM" + ".csv", 'w', newline='') as writer:
    wr = csv.writer(writer, quoting=csv.QUOTE_ALL)
    for r in res:
        wr.writerow(r)

"""