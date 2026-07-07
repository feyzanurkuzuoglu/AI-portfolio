import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("weight-height.csv")
# print(df.head())      # birkaç tane (ilk 5?) satırı veriyor
# print(df.Height.describe())     #height sütununda mean, standard deviation , 50th percentile gibi değerleri verir

# sns.histplot(df.Height, kde=True)
# plt.show()

std_deviation = df.Height.std()
mean = df.Height.mean()

alt_outlier = mean - 3*std_deviation
ust_outlier = mean + 3*std_deviation

# print(df[(df.Height < alt_outlier) | (df.Height > ust_outlier)])

df_no_outlier = df[(df.Height > alt_outlier) & (df.Height < ust_outlier)]
# print(df_no_outlier.shape)

df["zscore"] = (df.Height - df.Height.mean())/df.Height.std()

print(df[(df.zscore>3) | (df.zscore<-3)])




