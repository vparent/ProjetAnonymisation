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
nngt=[gt1,gt2,gt3,gt4,gt5]
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L"]
date = ["JA","FE","MA","AP","MY","JN","JL","AU","SE","OC","NO","DE"]


dat_list = gt1.date.unique().tolist()
indexl =len(dat_list)-1


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

## Modif id_user ==> letter + id + month
def modif_user(index): 
    for g in ngt:
        if index == 13 : 
            index = 1
        g["letter"] = alphabet[index-1]
        g["months"] = date[index-1]
        g["id_user"] = g["letter"] + g["id_user"].apply(str) + g["months"]
        del g["letter"]
        del g["months"]
        index+=1
        #print(g.id_user)

#######################################################################

def lissage_date():
    for g in ngt:
        g.date = g.loc[0,"date"]


def new_date(x):
    global indexl
    #print(indexl) 
    dat = gt1.date.unique().tolist()
    #print(dat)
    x = dat[indexl]
    #print(gt1.date)
    if indexl==0:
        indexl+=(len(dat))
    indexl-=1
    #print(indexl)
    return x

def lissage_date_1():
        dat = gt1.date.unique().tolist()
        gt1.apply(new_date, axis=1)
        print(gt1.date)


########################################################

#modif price ==> price btw 0 and 10€ ==> [0:10]
def modif_price():
    for g in ngt:
        g["price"] = g["price"].mean()

def test_del(conc):
    conc["id_user"]= "DEL"


def mul_price(co):
    co["price"] *= co["qty"]
    #co.id_item[co.id_item.str.contains('A')] = "COUCOU"

def suppr_singleton_item():
    for g in ngt:
        print(g["id_user","id_item"])

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

            

############################################################################

if __name__ == "__main__":
    #modif_user(12)

    gen_new_ids(ngt)
    
    #print(gt1.id_user)
    #print(gt1.price)
    #print(gt1.dtypes)
    
    #lissage_date_1()
    #write_data("test_gt1.csv")

    lissage_date()
    co=concat()
    mul_price(co)
    #print(gt1["id_item"].value_counts())

    #print(co.id_user)

    write_data_conc("submission_modif_anthony_new.csv", co)



##  DAY ONLY :
#   U: 0.442389085   R: 0.146618

## WITH ID_USER:
#   U: 0.6380805368572241 R : 0.124857
## WITH REST:
#   U: 0.6826931653  R: 0.11029
