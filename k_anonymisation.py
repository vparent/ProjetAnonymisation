import pandas 

gt= pandas.read_csv("ground_truth.csv")

def print_data(file_data):
    #print(gt)
    #print(gt.describe())
    #print(gt.head())
    #print(gt["id_user"].value_counts())
    print(gt.loc[(gt["qty"]==6)])

def write_data(file_data_dst):
    df.to_csv(file_data_dst, sep = '\t')

if __name__ == "__main__":
    #write_data('test_write.csv')
    print_data(gt)

"""
datalist=[]

#read file and convert lines into lists to get access to infos
def read_data(file_data):
    indice=0
    data = open(file_data, 'r')
    lines = data.readlines()
    for line in lines:
        if indice !=0:
            info = line.split(',')
            for i in info:
                info[-1] = info[-1].rstrip('\n')
            datalist.append(info)
        indice+=1
            #print(info)
    #print(datalist)
    data.close()


#write infos in file
def write_data(file_data_src, file_data_dst):
    rfile = open(file_data_src, 'r')
    wfile = open(file_data_dst, 'w')
    wfile.write(file_data_src)
    wfile.close()
    rfile.close()

#print line
def print_data(line):
    for i in range(line):
        print(datalist[i])

"""

