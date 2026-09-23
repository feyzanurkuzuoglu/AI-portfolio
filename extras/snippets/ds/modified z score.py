import pandas as pd
import numpy as np

df = pd.read_csv("movie_revenues.csv")

df["revenue_mln"] = df["revenue"].apply(lambda x: x/1000000)
# print(df.revenue_mln.describe())

_, mean, std, *_ = df.revenue_mln.describe()

# print(mean, std)

def get_z_score(value, mean, std):
    return (value - mean) / std


df["z_score"] = df.revenue_mln.apply(lambda x: get_z_score(x, mean, std))

def get_mad(s):
    median = np.median(s)
    diff = np.abs(s - median)
    MAD = np.median(diff)
    return MAD

median = np.median(df.revenue_mln)
MAD = get_mad(df.revenue_mln)

def get_modified_z_score(x, median, MAD):
    return 0.6745*(x-median)/MAD

df["modified_z_score"] = df.revenue_mln.apply(lambda x: get_modified_z_score(x, median, MAD))

print(df[df.modified_z_score > 3.5])