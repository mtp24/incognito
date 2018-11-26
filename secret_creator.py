import pandas as pd
import sys


T_COL = {'id_user':1, 'date':2, 'hours':3, 'id_item':4, 'price':5, 'qty':6}


def trunc_hours(row):
    return '00:00'



def main():
    """main
    """
    print("Beginning of the script")
    file_path = "./data/ground_truth.csv"

    df = pd.read_csv(file_path, sep=',', engine='c', na_filter=False, low_memory=False, index_col=0)

    df['hours'] = df.apply(trunc_hours, axis=1)

    print(df)

    df.to_csv("./hideData.csv")

    print("All clear")


if __name__ == "__main__":
        main()

