import pandas as pd
import random
import time
import csv
from collections import OrderedDict


T_COL = {'id_user': 0, 'date': 1, 'hours': 2, 'id_item': 3, 'price': 4, 'qty': 5}

unique_top_user = []


def search_id(row, u_items, u_list_items):

    id_user = row[T_COL['id_user']]
    id_product = row[T_COL['id_item']]
    qty = row[T_COL['qty']]


    if id_user in u_items:
        if id_product in u_items[id_user]:
            u_items[id_user][id_product] += qty
        else:
            u_items[id_user][id_product] = qty
            u_list_items[id_user].append(id_product)
    else:
        u_items[id_user] = {
            id_product: qty
        }
        u_list_items[id_user] = [id_product]


def sort_items(u_items, u_items_sorted):
    for user in u_items.items():
        u_items_sorted[user[0]] = (sorted(user[1].items(), key=lambda t: t[1], reverse=True))


def find_uniqueness_top_items(number_items):
    global users_items_sorted
    global unique_top_user
    unique_top_user = []

    for user in users_items_sorted:
        top_items_user = []
        if len(users_items_sorted[user]) >= number_items:
            for i in range(number_items):
               top_items_user.append(users_items_sorted[user][i][0])
            uniqueness = True
            for other_user in users_items_sorted:
                if user != other_user and len(users_items_sorted[other_user]) >= number_items:
                    top_items_other = []
                    for i in range(number_items):
                        top_items_other.append(users_items_sorted[other_user][i][0])
                    #print(top_items_other)
                    if len(set(top_items_user).intersection(top_items_user,top_items_other)) == number_items:
                        uniqueness = False
                        break
            if uniqueness == True:
                unique_top_user.append(user)


def find_uniqueness_random_items(nb_repetition, nb_items, u_list_items, unique_u_random_items):
    for user in u_list_items:
        nb_purchased_items = len(u_list_items[user])
        items_user = []
        for i in range(0, nb_repetition):
            items_user = []
            for j in range(0, nb_items):
                randomIndex = random.randrange(0, nb_purchased_items)
                items_user.append(u_list_items[user][randomIndex])
            uniqueness = True
            for other_user in u_list_items:
                if uniqueness == False:
                    break
                if user != other_user:
                    if set(items_user).issubset(u_list_items[other_user]):
                    #    print("")
                    #    print("-------")
                    #    print("user", user)
                    #    print("item_user", item_user)
                    #    print("item_other_user", item_other_user)
                    #    print("-----")
                    #    print("")
                        uniqueness = False
                        break

            if uniqueness == True and user not in unique_u_random_items:
                unique_u_random_items[user] = items_user
                break


def file_analysis(path, u_items,u_list_items, u_items_sorted):

    df = pd.read_csv(path, sep=',', engine='c', na_filter=False, low_memory=False)
    df.apply(lambda row: search_id(row, u_items, u_list_items), axis=1)
    sort_items(u_items, u_items_sorted)


def find_match_random(unique_users_random_items_anonymized, users_list_items_truth, id_matching):
    for anonymized_user in unique_users_random_items_anonymized:
        count_match = 0
        for user in users_list_items_truth:
            if set(unique_users_random_items_anonymized[anonymized_user]).issubset(users_list_items_truth[user]):
                count_match += 1
                same_user = user

        if count_match == 1:
            id_matching[same_user] = anonymized_user


def find_users_increasing_item_number(users_list_items_analysis, users_list_items_truth, id_matching):
    users_list_items_analysis_remaining = users_list_items_analysis.copy()
    unique_user_truth_remaining = users_list_items_truth.copy()
    for i in range(0, 6):
        id_found = {}
        unique_users_anonymized = {}
        find_uniqueness_random_items(2, i, users_list_items_analysis_remaining, unique_users_anonymized)
        find_match_random(unique_users_anonymized, unique_user_truth_remaining, id_found)
        print(len(id_found), " users where found at this loop")
        for user_found in id_found:
            users_list_items_analysis_remaining.pop(id_found[user_found])
            unique_user_truth_remaining.pop(user_found)
        #add the new user found to id_matching
        id_matching = {**id_found, **id_matching}




def main():
    """main
    """
    print("Beginning of the script")
    path_truth = "./data/ground_truth.csv"

    users_items_truth = {}
    users_list_items_truth = {}
    users_items_sorted_truth = {}
   # unique_users_random_items_truth = []

    file_analysis(path_truth, users_items_truth, users_list_items_truth,  users_items_sorted_truth)

    nbUser_truth = len(users_items_sorted_truth)
    print("nbUser truth", nbUser_truth)
    path_analysis = "./data/ouputTestprice.csv"

    users_items_analysis = {}
    users_list_items_analysis = {}
    users_items_sorted_analysis = {}
    unique_users_random_items_anonymized = {}

    file_analysis(path_analysis, users_items_analysis, users_list_items_analysis, users_items_sorted_analysis)

    # Trying to match user by using the matching method step by step
    id_matching = {}
    start = time.time()
    find_users_increasing_item_number(users_list_items_analysis, users_list_items_truth, id_matching)
    end = time.time()
    time_increasing = end-start
    print(time_increasing, "for the first one")


    #Trying to match user by using the matching method directly
    id_matching = {}
    start = time.time()
    find_uniqueness_random_items(2, 6, users_list_items_analysis, unique_users_random_items_anonymized)
    print("NB anonymized users potentially identifiable", len(unique_users_random_items_anonymized))
    find_match_random(unique_users_random_items_anonymized, users_list_items_truth, id_matching)
    end = time.time()
    time_brute = end-start
    print(time_brute, "for the second one")

    #print(id_matching)

    print("Nb identified", len(id_matching))

  #  with open('dict.csv', 'wb') as csv_file:
  #      writer = csv.writer(csv_file)
  #      for key, value in unique_users_random_items_anonymized.items():
  #          print("key", key)
  #          print("value", value)
  #          writer.writerow([key, value])


    # for i in range (1,6):
    #    find_uniqueness_top_items(i)
     #   print("Nb unique d'user: ", len(unique_top_user), ", pour", i, "articles")






    print("All clear")

if __name__ == "__main__":
        main()

