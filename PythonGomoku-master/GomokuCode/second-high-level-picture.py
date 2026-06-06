import matplotlib.pyplot as plt
import numpy as np

# 数据
depths = [1, 2, 3, 4]
avg_nodes = [200, 562, 12341, 129687]
avg_time_ms = [5, 13.5, 287.3, 1215.6]
eval_time_ms = [4, 11.7, 265.1, 1138.2]
eval_ratio = [80, 86.7, 92.3, 93.6]

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形，两个子图上下排列
fig = plt.figure(figsize=(10, 10))

# ==================== 上子图：耗时和节点数 ====================
ax1 = plt.subplot(2, 1, 1)

# 柱状图 - 耗时
x = np.arange(len(depths))
width = 0.35
bars1 = ax1.bar(x - width/2, avg_time_ms, width, color='#5B9BD5', 
                label='耗时 (ms)', edgecolor='white', linewidth=1)

# 折线图 - 节点数（双Y轴）
ax1_twin = ax1.twinx()
line1 = ax1_twin.plot(x, avg_nodes, 'o-', color='#ED7D31', 
                      linewidth=2.5, markersize=8, label='节点数 (个)')

# 在节点数折线上添加数值标签
for i, (xi, nodes) in enumerate(zip(x, avg_nodes)):
    if nodes >= 10000:
        label = f'{nodes/1000:.0f}k'
    else:
        label = str(nodes)
    ax1_twin.annotate(label, (xi, nodes), textcoords="offset points", 
                      xytext=(0, 12), ha='center', fontsize=9, 
                      color='#ED7D31', fontweight='bold')

# 在柱状图上添加耗时标签
for bar, time_val in zip(bars1, avg_time_ms):
    ax1.annotate(f'{time_val}ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

# 设置标题和标签
ax1.set_xlabel('搜索深度', fontsize=12, fontweight='bold')
ax1.set_ylabel('耗时 (ms)', fontsize=12, fontweight='bold', color='#5B9BD5')
ax1.tick_params(axis='y', labelcolor='#5B9BD5')
ax1.set_xticks(x)
ax1.set_xticklabels([f'深度 {d}' for d in depths], fontsize=11)
ax1.set_title('搜索性能分析 - 耗时与节点数', fontsize=14, fontweight='bold', pad=15)

ax1_twin.set_ylabel('节点数 (个)', fontsize=12, fontweight='bold', color='#ED7D31')
ax1_twin.tick_params(axis='y', labelcolor='#ED7D31')
ax1_twin.set_yscale('log')  # 节点数跨度大，使用对数坐标

# 添加网格
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

# ==================== 下子图：估值耗时和棋力评估 ====================
ax2 = plt.subplot(2, 1, 2)

# 堆积分组柱状图：估值耗时 vs 其他耗时
x = np.arange(len(depths))
width = 0.5

other_time = [avg_time_ms[i] - eval_time_ms[i] for i in range(len(depths))]

bars_eval = ax2.bar(x, eval_time_ms, width, color='#70AD47', 
                    label='估值函数耗时', edgecolor='white', linewidth=1)
bars_other = ax2.bar(x, other_time, width, bottom=eval_time_ms, 
                     color='#FFC000', label='其他耗时', edgecolor='white', linewidth=1)

# 在每个柱状组上方显示总耗时和估值占比
for i, (xi, total, eval_t, eval_r) in enumerate(zip(x, avg_time_ms, eval_time_ms, eval_ratio)):
    # 总耗时标签
    ax2.text(xi, total + 15, f'{total}ms', ha='center', fontsize=9, fontweight='bold')
    # 估值占比标签
    ax2.text(xi, total / 2, f'估值占{int(eval_r)}%', ha='center', fontsize=8, 
             color='white', fontweight='bold')

# 设置第二个子图的格式
ax2.set_xlabel('搜索深度', fontsize=12, fontweight='bold')
ax2.set_ylabel('耗时 (ms)', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels([f'深度 {d}' for d in depths], fontsize=11)
ax2.set_title('耗时构成分析 - 估值函数占比', fontsize=14, fontweight='bold', pad=15)

# 添加棋力评估文本标注
strength_labels = ['弱\n(无防守)', '中等\n(有基本防守)', '较强\n(复杂攻防)', '强\n(深度预判)']
for i, (xi, label) in enumerate(zip(x, strength_labels)):
    ax2.annotate(label, (xi, -80), ha='center', fontsize=10, 
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8E8E8', alpha=0.8),
                 fontweight='bold')

# 添加网格
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_axisbelow(True)

# 添加图例
ax2.legend(loc='upper left', fontsize=10)

# 调整整体布局
plt.tight_layout()
plt.subplots_adjust(hspace=0.35)

# 保存图片
plt.savefig('chess_ai_performance.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.show()

print("图表已保存为 chess_ai_performance.png")