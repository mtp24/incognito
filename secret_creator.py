import pandas as pd
import sys


T_COL = {'id_user':1, 'date':2, 'hours':3, 'id_item':4, 'price':5, 'qty':6}


def trunc_hours(row):
    return '00:00'



def main():
    """main
    """
    print("Beginning of the script")
    file_path = "/Users/charles/Documents/IF/IF/DARC/data/ground_truth.csv"

    df = pd.read_csv(file_path, sep=',', engine='c', na_filter=False, low_memory=False, index_col=0)
   # df.columns = T_COL.values()
    print(df)

    df['hours'] = df.apply(trunc_hours, axis=1)

   # for row in df.iterrows():
    #   row[1][T_COL['hours']] = '00:00'

    print(df)

    df.to_csv("./tachatte.csv", index=False)

    print("All clear")


if __name__ == "__main__":
        main()

