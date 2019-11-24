import pandas

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
        g["letter"] = alphabet[index-1]
        g["months"] = date[index-1]
        g["id_user"] = g["letter"] + g["id_user"].apply(str) + g["months"]
        del g["letter"]
        del g["months"]
        index+=1
        #print(g.id_user)


#modif price ==> price btw 0 and 10€ ==> [0:10]
def modif_price():
    for g in ngt:
        g["price"] = g["price"].mean()


def mul_price(co):
    co["price"] *= co["qty"]

############################################################################

if __name__ == "__main__":
    #modif_user(12)
    
    #print(gt1.id_user)
    #print(gt1.price)
    #print(gt1.dtypes)
    
    co=concat()
    mul_price(co)
    write_data_conc("submission_modif_anthony.csv", co)
