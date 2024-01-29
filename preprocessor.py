import pandas as pd
def preprocess(df,region_df):
    # FILTERING FOR SUMMER OLYMPICS
    df = df[df['Season']=='Summer']
    # MERGING WITH REGION DF
    df = df.merge(region_df,on='NOC',how='left')
    # DROPPING DUPLICATES
    df = df.drop_duplicates()
    # ONE-HOT ENCODING MEDALS
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df