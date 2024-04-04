import pandas as pd


def filter(input, string, col,  output):
    
    df = pd.read_csv("csv/"+input)



    masque = df.apply(lambda row: string in str(row[col]).lower(), axis=1)


    df_filtre = df[masque]


    df_filtre = df_filtre.reset_index(drop=True)


    df_filtre.to_csv("csv/"+output, index=False)

def FindDifferences(df1, df2):
    
    if df1.shape != df2.shape:
        raise ValueError("Les DataFrames n'ont pas la même taille.")


    indices_diff = [(i, j) for i in range(df1.shape[0]) for j in range(df1.shape[1]) if df1.iloc[i, j] != df2.iloc[i, j]]

    return indices_diff




