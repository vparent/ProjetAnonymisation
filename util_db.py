#! /usr/bin/python3

from MySQLdb import _mysql

import os
import sys
import csv

def main():
    cleanup, setup = False, False

    if len(sys.argv) < 2:
        print("usage ./util_db [--cleanup to clean the database] "
                "[--setup to setup the database]")

    cleanup = True if "--cleanup" in sys.argv and not setup else False
    setup = True if "--setup" in sys.argv and not cleanup else False

    if setup:
        print("Setting up the database")
        setup_script = "setup_db.sql"
        print("Enter the mysql root user password")
        os.system(f"mysql -u root -p < {setup_script}")

    if cleanup:
        print("Cleaning up the database")
        cleanup_script="cleanup_db.sql"
        os.system(f"mysql -u root -p < {cleanup_script}")

def populate_table(csv_file, table):
    db = _mysql.connect(host="localhost",
            user="anonymisation",
            passwd="azerty")

    f = open(csv_file, "r")
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        id_user = row['id_user']
        date = row['date']
        hours = row['hours']
        id_item = row['id_item']
        price = row['price']
        qty = row['qty']

        db.query(f"INSERT INTO {table} VALUES ("
                f"{id_user}, {date}, {hours}, {id_item}, "
                f"{price}, {qty}"
                f");")
    db.commit()

if __name__ == '__main__':
    main()
