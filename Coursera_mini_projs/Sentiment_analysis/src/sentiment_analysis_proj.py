import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']

def strip_punctuation(string):
    for char in string:
        if char in punctuation_chars:
            string = string.replace(char, '')
    return string

positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())

def get_pos(long_string):
    string_mod = strip_punctuation(long_string)
    string_list = string_mod.lower().split()
    positive_count = 0
    for word in string_list:
        if word in positive_words:
            positive_count += 1
    return positive_count

negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())

def get_neg(x):
    string_mod = strip_punctuation(x)
    string_list = string_mod.lower().split()
    negative_count = 0
    for word in string_list:
        if word in negative_words:
            negative_count += 1
    return negative_count

rows_list = []
with open('project_twitter_data_input.csv', 'r') as fh:
    for line in fh:
        new_line = line.strip().split(',')
        retweet_count = new_line[1]
        reply_count = new_line[2]
        positive_score = get_pos(new_line[0])
        negative_score = get_neg(new_line[0])
        net_score = positive_score-negative_score
        row_string = '{}, {}, {}, {}, {}'.format(retweet_count, reply_count, positive_score, negative_score, net_score)
        rows_list.append(row_string)

resulting_data = open('resulting_data.csv', 'w')
resulting_data.write('Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score')
resulting_data.write('\n')
for string in rows_list[1:]:
    resulting_data.write(string)
    resulting_data.write('\n')


resulting_data.close()

master_df = pd.read_csv('resulting_data.csv')
x = pd.read_csv('resulting_data.csv',usecols=[' Net Score'])
y_size_color = pd.read_csv('resulting_data.csv',usecols=['Number of Retweets']).values.flatten()

fig, ax = plt.subplots(figsize=(12,12))

sns.set_style("darkgrid")
sns.scatterplot(x=" Net Score",y="Number of Retweets",data=master_df,size=y_size_color,hue=y_size_color,palette="dark:m_r",ax=ax)
ax.set_xlabel("Net Analysis Score")
ax.set_ylabel("Number of Retweets")
ax.set_title("Sentiment Analysis Results with sample Twitter data")

plt.show()
plt.savefig("sentiment_plot.png",dpi=300)