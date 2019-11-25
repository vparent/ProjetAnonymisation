import csv
import getopt
import sys

def main():
    opts, _ = getopt.getopt(sys.argv[1:], "g: f: n:")
    ground_truth, f_file, month_nb = None, None, None

    for opt in opts:
        opt_name, opt_val = opt
        if opt_name == "-g":
            ground_truth = opt_val
        if opt_name == "-f":
            f_file = opt_val
        if opt_name == "-n":
            month_nb = int(opt_val)

    gen_f_file(ground_truth, f_file, month_nb)

def gen_f_file(ground_truth_filename, blank_f_file_filename, month_nb):
    fr = open(ground_truth_filename, "r")
    fw = open(blank_f_file_filename, "w")

    reader = csv.DictReader(fr)
    user_ids = [ row['id_user'] for row in reader ]
    user_ids = list(set(user_ids))
    user_ids.sort()

    header = ['id_user'] + [ str(i) for i in range(month_nb) ]
    writer = csv.DictWriter(fw, delimiter=',', fieldnames=header)
    writer.writeheader()

    for uid in user_ids:
        row = { 'id_user': uid }
        for i in range(month_nb):
            row[str(i)] = 'DEL'
        writer.writerow(row)

    fr.close()
    fw.close()
    
if __name__ == '__main__':
    main()
