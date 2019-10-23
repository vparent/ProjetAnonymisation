import pandas 

def read_data(file_data):
    df = pandas.read_csv(file_data, index_col = 0)
    print(df)

def write_data(file_data_src,file_data_dst):
    df = pandas.read_csv(file_data_src, index_col = 0)

    df.to_csv(file_data_dst, sep = '\t')

if __name__ == "__main__":
    read_data('ground_truth.csv')
    write_data('ground_truth.csv','test_write.csv')
    #print(len(datalist))
   # print_data(30)

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

