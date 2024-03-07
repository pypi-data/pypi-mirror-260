import matplotlib.pyplot as plt

# 创建一个新的图形
fig = plt.figure()

# 使用add_axes创建不同比例的子图
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
ax1 = fig.add_axes([left, bottom, width, height])  # 主图
ax2 = fig.add_axes([0.2, 0.6, 0.25, 0.25])         # 子图1
ax3 = fig.add_axes([0.6, 0.2, 0.25, 0.25])         # 子图2

# 在每个子图中绘制示例图形
ax1.plot([0, 1], [0, 1])
ax2.plot([0, 1], [1, 0])
ax3.plot([0, 1], [0.5, 0.5])

plt.show()
