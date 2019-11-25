import pandas
import hashlib
import random

gt = pandas.read_csv("ground_truth.csv")
gt1= pandas.read_csv("ground_truth_month_1.csv")
gt2= pandas.read_csv("ground_truth_month_2.csv")
gt3= pandas.read_csv("ground_truth_month_3.csv")
gt4= pandas.read_csv("ground_truth_month_4.csv")
gt5= pandas.read_csv("ground_truth_month_5.csv")
gt6= pandas.read_csv("ground_truth_month_6.csv")
gt7= pandas.read_csv("ground_truth_month_7.csv")
gt8= pandas.read_csv("ground_truth_month_8.csv")
gt9= pandas.read_csv("ground_truth_month_9.csv")
gt10= pandas.read_csv("ground_truth_month_10.csv")
gt11= pandas.read_csv("ground_truth_month_11.csv")
gt12= pandas.read_csv("ground_truth_month_12.csv")
gt13= pandas.read_csv("ground_truth_month_13.csv")

ngt=[gt1,gt2,gt3,gt4,gt5,gt6,gt7,gt8,gt9,gt10,gt11,gt12,gt13]

#########################################################################
# concatenation and write
    
def write_data(file_data_dst):  ##write data to csv file
    gt1.to_csv(file_data_dst, sep = ',', index=False)

def concat(): ## concatenate all csv file into 1 dataframe
    conc = pandas.concat(ngt)
    return conc

def write_data_conc(file_data_dst,co):  ## write concatenate dataframe to csv file
    co.to_csv(file_data_dst, sep = ',', index=False)
    

###########################################################################
# modif data

#######################################################################

def lissage_date():
    for g in ngt:
        dat = g.date.unique().tolist()
        ran=random.choice(dat)
        print(ran)
        g.date = ran #0
        #print(g.id_user.count())


########################################################

def mul_price(co):
    co["price"] *= co["qty"]
    #co.id_item[co.id_item.str.contains('A')] = "COUCOU"

def mul_price_month():
    for g in ngt:
        g["price"] *= g["qty"]

def lissage_hour():
    for g in ngt:
        hour = g.hours.unique().tolist()
        ran=random.choice(hour)
        print(ran)
        g.hours = ran

def gen_new_ids(ngt):
    for gt in ngt:
        new_uids = []
        corresp = {}

        for uid in set(gt['id_user']):
            transacs = []
            for row in gt.loc[gt['id_user'] == uid].values:
                transacs.append(f"{row[0]}{row[1]}{row[2]}{row[3]}{row[4]}{row[5]}")
            htransac = hashlib.sha512(str.encode(random.choice(list(set(transacs))))).hexdigest()
            borne = 0
            while htransac[borne:borne+5] in new_uids and borne < 123:
                borne += 1
            new_uids.append(htransac[borne:borne+5])
            corresp[uid] = htransac[borne:borne+5]

            gt.loc[gt['id_user'] == uid, 'id_user'] = corresp[uid]

def write_hash_date(i):
    for fil in range(i):
        gen_new_ids(ngt)
        lissage_date()
        lissage_hour()
        co=concat()
        mul_price(co)
        write_data_conc("submission_modif_anthony"+str(fil)+".csv", co)
############################################################################

if __name__ == "__main__":
    write_hash_date(10)
