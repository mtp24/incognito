import pandas as pd


T_COL = {'id_user': 0, 'date': 1, 'hours': 2, 'id_item': 3, 'price': 4, 'qty': 5}
users_items = {}



def search_id(row):

    id_row = row[T_COL['id_user']]
    id_product = row[T_COL['id_item']]
    qty = row[T_COL['qty']]
    if id_row in users_items:
        if id_product in users_items[id_row]:
            users_items[id_row][id_product] += qty
        else :
            users_items[id_row] = pd{
                id_product: [qty]
            }
    else:
        users_items[id_row] = pd{
            id_product: [qty]
        }


def main():
    """main
    """
    print("Beginning of the script")

    file_path = "./data/ground_truth.csv"
    global users_items

    df = pd.read_csv(file_path, sep=',', engine='c', na_filter=False, low_memory=False)

    df.apply(search_id, axis=1)
   # df_user = pd.DataFrame.from_dict(users_items)
    print(users_items)

    print("All clear")


if __name__ == "__main__":
        main()
