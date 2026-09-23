import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("income.csv", index_col=None, names=["income", "count"], skiprows=1)
# print(df.head())

sns.set(rc={'figure.figsize':(10,10)})
g = sns.barplot(x="income", y="count", data=df)
g.set_xticklabels(g.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()

sns.set(rc={'figure.figsize':(10,10)})
g = sns.barplot(x="income", y="count", data=df)
g.set_xticklabels(g.get_xticklabels(), rotation=45, horizontalalignment='right')
g.set(xscale="log")
plt.show()

