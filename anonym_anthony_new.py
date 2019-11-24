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
        g["letteir"] = alphabet[index-1]
        g["months"] = date[index-1]
        g["id_user"] = g["letter"] + g["id_user"].apply(str) + g["months"]
        del g["letter"]
        del g["months"]
        index+=1

######################################################

def mul_price(co):
    co["price"] *= co["qty"]


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


##########################################################################

if __name__ == "__main__":

    gen_new_ids(ngt)
    
    co=concat()
    mul_price(co)


    write_data_conc("submission_modif_anthony_new.csv", co)



##  DAY ONLY :
#   U: 0.442389085   R: 0.146618

## WITH ID_USER:
#   U: 0.6380805368572241 R : 0.124857
## WITH REST:
#   U: 0.6826931653  R: 0.11029
