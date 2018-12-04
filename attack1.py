import pandas as pd
import random
from collections import OrderedDict


T_COL = {'id_user': 0, 'date': 1, 'hours': 2, 'id_item': 3, 'price': 4, 'qty': 5}
users_items = {}
users_items_sorted = {}
unique_top_user = []
unique_users_random_items = []
users_list_items = {}

def search_id(row, u_items):

    id_user = row[T_COL['id_user']]
    id_product = row[T_COL['id_item']]
    qty = row[T_COL['qty']]


    if id_user in u_items:
        if id_product in u_items[id_user]:
            u_items[id_user][id_product] += qty
        else:
            u_items[id_user][id_product] = qty
            users_list_items[id_user].append(id_product)
    else:
        u_items[id_user] = {
            id_product: qty
        }
        users_list_items[id_user] = [id_product]

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

            if uniqueness == True and {user : items_user} not in unique_u_random_items:
                unique_u_random_items.append({user: items_user})
                break




def main():
    """main
    """
    print("Beginning of the script")

    file_path = "./data/ground_truth.csv"
  #  global users_items
#    global users_items_sorted

    df = pd.read_csv(file_path, sep=',', engine='c', na_filter=False, low_memory=False)

    df.apply(lambda row: search_id(row, users_items), axis=1)
    sort_items(users_items, users_items_sorted)
    nbUser = len(users_items_sorted)
    print ("nbUser", nbUser)


   # for i in range (1,6):
    #    find_uniqueness_top_items(i)
     #   print("Nb unique d'user: ", len(unique_top_user), ", pour", i, "articles")

#    print(users_items_sorted)
   # print(users_list_items)
    unique_users_random_items = []
    find_uniqueness_random_items(5, 6, users_list_items, unique_users_random_items)
    print(len(unique_users_random_items))


    print("All clear")

if __name__ == "__main__":
        main()

