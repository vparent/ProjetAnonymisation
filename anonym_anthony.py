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

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L"]

def write_data(file_data_dst,co):
    co.to_csv(file_data_dst, sep = ',', index=False)

def concat():
    frames = [gt,gt2,gt3,gt4,gt5,gt6,gt7,gt8,gt9,gt10,gt11,gt12]
    conc = pandas.concat(frames)
    return conc

if __name__ == "__main__":
    #co= concat()
    #modif_id(0)
    write_data("modif_m1.csv",co)

