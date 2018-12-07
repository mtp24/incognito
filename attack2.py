import pprint
import sys

import pandas as pd
import time
import csv
from collections import OrderedDict, Counter
from datetime import datetime
import numpy as np

T_COL = {'id_user': 0, 'date': 1, 'hours': 2, 'id_item': 3, 'price': 4, 'qty': 5}
users_to_items = {}
items_to_users = {}
nb_invalid = 0


def search_id(row):
    global nb_invalid
    id_user = row[T_COL['id_user']]
    id_date = row[T_COL['date']]
    try:
        dt = datetime.strptime(id_date, '%Y/%m/%d')
        month = str(dt.month)
        if dt.month < 10:
            month = '0' + month
        id_month = str(dt.year) + month

        id_month_user = str(id_user) + ' ' + id_month

        id_product = row[T_COL['id_item']]
        qty = row[T_COL['qty']]

        if id_month_user in users_to_items:
            if id_product not in users_to_items[id_month_user]:
                users_to_items[id_month_user].append(id_product)
        else:
            users_to_items[id_month_user] = []
            users_to_items[id_month_user].append(id_product)

    except ValueError:
        nb_invalid = nb_invalid + 1


def search_product(row):
    global nb_invalid
    id_user = row[T_COL['id_user']]
    id_date = row[T_COL['date']]
    try:
        dt = datetime.strptime(id_date, '%Y/%m/%d')
        month = str(dt.month)
        if dt.month < 10:
            month = '0' + month
        id_month = str(dt.year) + month

        id_month_user = str(id_user) + ' ' + id_month

        id_product = row[T_COL['id_item']]

        if id_product in items_to_users:
            if id_month_user not in items_to_users[id_product]:
                items_to_users[id_product].append(id_month_user)
        else:
            items_to_users[id_product] = []
            items_to_users[id_product].append(id_month_user)

    except ValueError:
        nb_invalid = nb_invalid + 1


def find_user():
    global users_to_items
    found_users = 0
    for puser, product in users_to_items.items():
        cnt = Counter()
        for prd in product:
            if prd in items_to_users:
                for user in items_to_users[prd]:
                    cnt[user] += 1
        if len(cnt.most_common()) == 1 or cnt.most_common(2)[0][1] != cnt.most_common(2)[1][1]:
            found_users +=1
            result = found_users*100/len(users_to_items.items())
            sys.stdout.write("\r{0}%".format(round(result,2)))
            sys.stdout.flush()
    print("\n-----Final Result-----")
    print("Total of user : ", len(users_to_items.items()))
    print("Number of user identified :", found_users)
    print("Percentage : ", round(result,2), '%')

def export_base():
    global items_to_users
    with open('base.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in items_to_users.items():
            writer.writerow([key, ','.join(value)])

def import_base():
    with open('base.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        temp_dict = dict(reader)
    mydict = {k: v.split(',') for k, v in temp_dict.items()}
    csv_file.close()
    return mydict

def main():
    """main
    """
    print("Beginning of the script")

    file_path = "./ouput.csv"
    base_path = "./data/ground_truth.csv"
    global users_to_items
    global items_to_users

    df = pd.read_csv(file_path, sep=',', engine='c', na_filter=False, low_memory=False)
    base = pd.read_csv(base_path, sep=',', engine='c', na_filter=False, low_memory=False)

    #base.apply(search_product, axis=1)
    #print("base done")
    #export_base()
    items_to_users = import_base()
    print('Base imported')

    df.apply(search_id, axis=1)
    print("Number of invalid dates : ", nb_invalid)
    print("Test imported")

    find_user()

    print("All clear")


if __name__ == "__main__":
    main()
