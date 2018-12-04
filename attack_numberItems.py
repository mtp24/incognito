import pandas as pd
from collections import OrderedDict


T_COL = {'id_user': 0, 'date': 1, 'hours': 2, 'id_item': 3, 'price': 4, 'qty': 5}
users_items = {}


def search_id(row):

    id_user = row[T_COL['id_user']]
    id_product = row[T_COL['id_item']]
    qty = row[T_COL['qty']]
    if id_user in users_items:
        if id_product in users_items[id_user]:
            users_items[id_user][id_product] += qty
        else:
            users_items[id_user][id_product] = qty
    else:
        users_items[id_user] = {
            id_product: qty
        }

#def find_buyer_oneP() :




def main():
    """main
    """
    print("Beginning of the script")

    file_path = "./data/ground_truth.csv"
    global users_items

    df = pd.read_csv(file_path, sep=',', engine='c', na_filter=False, low_memory=False)

    df.apply(search_id, axis=1)

    users_items_sorted = {}
    for user in users_items.items():
        users_items_sorted[user[0]] = (sorted(user[1].items(), key=lambda t: t[1], reverse=True))

    user_one_item = {}
    user_two_item = {}
    user_three_item = {}
    user_four_item = {}
    user_five_item = {}
    user_six_item = {}
    user_seven_item = {}
    for user in users_items_sorted.items():
        if len(user[1]) == 1:
            user_one_item[user[0]] = user
        if len(user[1]) == 2:
            user_two_item[user[0]] = user
        if len(user[1]) == 3:
            user_three_item[user[0]] = user
        if len(user[1]) == 4:
            user_four_item[user[0]] = user
        if len(user[1]) == 5:
            user_five_item[user[0]] = user
        if len(user[1]) == 6:
            user_six_item[user[0]] = user
        if len(user[1]) == 7:
            user_seven_item[user[0]] = user
    print(len(user_one_item))
    print(len(user_two_item))
    print(len(user_three_item))
    print(len(user_four_item))
    print(len(user_five_item))
    print(len(user_six_item))
    print(len(user_seven_item))


    #print(users_items_sorted)

    print("All clear")


if __name__ == "__main__":
        main()

