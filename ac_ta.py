import re
import pandas as pd
import numpy as np

data = pd.read_csv("Data.csv", encoding="big5",index_col=0)
data.fillna("noname", inplace=True)
data["status"] = data["status"].replace("有庫存", 1)
data["status"] = data["status"].replace("沒庫存", 0)
# print(data.head())

def rank_calu(data):
    new_data = []
    new = eval(data)
    newlist = [newval for sublist in new for newval in sublist]
    new_data.append(newlist)
    new_data.append(np.sum(newlist))
    new_data.append(len(newlist))
    new_data.append(np.mean(newlist))

    return new_data

def re_name(word):
    new_name = re.sub('\s_.+_\s?', '', word)

    return new_name

def max_class(new_name):
    new_name = new_name.lower().replace(" ", "")
    sort_list = sorted(new_name)
    ad = {}
    for i in sort_list:
        if i in ad:
            ad[i] += 1
        else:
            a= {i:1}
            ad.update(a)
    max_key = max(ad, key=lambda key: ad[key])

    return max_key


col = ["class", "book name", "rank", "rank sum", "rank num", "rank mean", "name", "status"]
new_df = pd.DataFrame(columns=col)
# print(new_df)
new_df["status"] = data["status"]
new_df["name"] = data["name"]
# print(new_df)

for i in range(data.shape[0]):
    temp_list = []
    data_r = data.iloc[i,1]
    new_data = rank_calu(data_r)
    word = data.iloc[i,0]
    new_name = re_name(word)
    max_key = max_class(new_name)
    temp_list.append(max_key)
    temp_list.append(new_name)
    temp_list += new_data
    new_df.iloc[i,0:6] = temp_list

new_df.to_csv("data_new.csv", encoding='utf_8_sig')

# ====

new_df = pd.read_csv("data_new.csv", encoding="utf_8_sig")
# class
new_class = new_df.groupby("class").size()

# no name
qu_1 = new_df.query("name == 'noname'")
qu_1 = qu_1.groupby("class").size()

# stock out
qu_2 = new_df.query("status == 0")
qu_2 = qu_2.groupby("class").size()

# all no
qu_1_2 = new_df.query("name == 'noname' & status == 0")
qu_1_2 = qu_1_2.groupby("class").size()

# name & 1
qu_3 = new_df.query("name != 'noname' & status == 1")
qu_3 = qu_3.groupby("class")

# sum
qu_3_s1 = qu_3["rank sum"].sum()
qu_3_s2 = qu_3["rank num"].sum()
qu_3_s3 = qu_3_s1/qu_3_s2

# mean
qu_3_m1 = qu_3["rank mean"].sum()
qu_3_m2 = qu_3.size()
qu_3_m3 = qu_3["rank mean"].mean()
# print(qu_3.size())


cols = ["class","no name", "stock out", "all no", "sum", "sum num", "sum mean", "mean sum", "mean num", "mean"]
new_cal = pd.concat([new_class, qu_1, qu_2, qu_1_2, qu_3_s1, qu_3_s2, qu_3_s3, qu_3_m1, qu_3_m2, qu_3_m3], axis=1)

new_cal.fillna(0, inplace=True)

new_cal.columns = cols
new_cal.to_csv("data_cal.csv", encoding='utf_8_sig')
