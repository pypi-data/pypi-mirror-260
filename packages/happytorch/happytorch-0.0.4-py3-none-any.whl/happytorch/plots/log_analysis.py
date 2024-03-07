import os
import re
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

from pandas.core.frame import DataFrame
# plt.style.use('ggplot')

sns.set_style("whitegrid")

# log_path = "/userHome/nemo/outputs/ttaa1010_time/2023_10_11_21_54_12.log"
# log_path = "/userHome/nemo/outputs/ttaa1010_time/2023_10_18_00_04_55.log"
log_path = "/userHome/nemo/outputs/ttaa1027a_time/2023_10_27_20_48_44.log"

pattern = re.compile(r'Epoch:\ \d+\n')

patt1 = re.compile(r'Loss:\ Prediction\ \d+\.?\d*/\ Compactness\ \d+\.?\d*/\ Separateness\ \d+\.?\d*/\ ranking_loss\ \d+\.?\d*\n')
patt2 = re.compile(r'AUC:\ \d+\.?\d*%\n')

num_patt = re.compile(r'\d+\.?\d*')

with open(log_path, encoding='utf-8') as file_obj:
    contents = file_obj.read()
    file_obj.close()

auc_list = [num_patt.findall(x) for x in patt2.findall(contents)]
auc_list = np.array([float(x[0]) for x in auc_list])[:-1]
epochs = np.array([x for x in range(len(auc_list))])

matches = patt1.findall(contents)
losses_list = [num_patt.findall(x) for x in matches]
losses_list = np.array(losses_list, dtype=np.float32).T

print(len(epochs), len(auc_list), len(losses_list[0]), len(losses_list[1]), len(losses_list[2]), len(losses_list[3]))
data = DataFrame({'epoch': epochs, 'auc': auc_list, 'prediction': losses_list[0], 'compactness': losses_list[1], 'separateness': losses_list[2], 'ranking_loss': losses_list[3]})

fig, ax = plt.subplots(figsize=(12, 6))

# 
auc_max = np.max(data['auc'])
index_max = np.argmax(data['auc'])
print(auc_max, index_max)
xy = (index_max, auc_max)
plt.plot(index_max, auc_max, marker='v', markersize=5, c='r', zorder=2)
plt.annotate("(%s: %.2f%%)" % xy, xy=xy, xytext=(-20, 10), textcoords='offset points', 
    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.5), zorder=3)

sns.lineplot(x='epoch', y='auc', c='darkorange', data=data, zorder=1)
plt.axvline(60, c="b", ls="-", lw=0.5, alpha=0.5)
plt.axhline(auc_list[0], c="b", ls=(45,(55,20)), lw=0.5)

p1 = ax.twinx()
p3 = ax.twinx()

sns.lineplot(x='epoch', y='prediction', data=data, ax=p1, color='b', ls='-.', lw=1, alpha=0.5, label='prediction')

sns.lineplot(x='epoch', y='compactness', data=data, ax=p1, color='g', ls='dashed', alpha=0.5, label='compactness')

sns.lineplot(x='epoch', y='separateness', data=data, ax=p3, color='m', ls='dotted', alpha=0.5, label='separateness')
sns.lineplot(x='epoch', y='ranking_loss', data=data, ax=p1, color='k', ls='dotted', alpha=0.5, label='ranking_loss')

p3.spines['right'].set_position(('outward', 80))

plt.subplots_adjust(left=0.05, right=0.8)
# plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.legend(loc='center right', bbox_to_anchor=(1.0, 0.4))
p1.legend(loc='center right')

sns.despine()


plt.savefig('/userHome/nemo/outputs/ttaa1027a_time/2023_10_27_20_48_44.png')
