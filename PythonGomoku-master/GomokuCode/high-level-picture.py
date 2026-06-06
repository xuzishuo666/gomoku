import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QGroupBox, QTabWidget)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'FangSong', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False

class AlphaBetaAnalysisWindow(QMainWindow):
    """α-β剪枝算法性能分析窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('α-β剪枝算法性能分析系统')
        self.setGeometry(100, 100, 1400, 900)
        
        # 实验数据
        self.node_counts = [97, 187, 309, 385, 506, 591, 885, 97, 459, 459, 26, 139, 615]
        self.time_costs = [0.0650, 0.1300, 0.2001, 0.2450, 0.3427, 0.3885, 0.5829, 
                           0.0700, 0.3104, 0.3068, 0.0151, 0.1000, 0.4110]
        self.eval_times = [0.0600, 0.1100, 0.1701, 0.2150, 0.3083, 0.3361, 0.5329,
                           0.0650, 0.2684, 0.2800, 0.0101, 0.0750, 0.3575]
        
        # 分类数据：纯Minimax vs α-β剪枝
        # 假设前7个是纯Minimax，后6个是α-β剪枝
        self.minimax_nodes = self.node_counts[:7]
        self.minimax_times = self.time_costs[:7]
        self.minimax_evals = self.eval_times[:7]
        
        self.ab_nodes = self.node_counts[7:]
        self.ab_times = self.time_costs[7:]
        self.ab_evals = self.eval_times[7:]
        
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # 标签页1：性能对比图表
        tab_charts = QWidget()
        tabs.addTab(tab_charts, "性能对比图表")
        self.setup_charts_tab(tab_charts)
        
        # 标签页2：详细数据表格
        tab_table = QWidget()
        tabs.addTab(tab_table, "详细数据表格")
        self.setup_table_tab(tab_table)
        
        # 标签页3：统计分析
        tab_stats = QWidget()
        tabs.addTab(tab_stats, "统计分析")
        self.setup_stats_tab(tab_stats)
        
        # 标签页4：散点图分析
        tab_scatter = QWidget()
        tabs.addTab(tab_scatter, "散点图分析")
        self.setup_scatter_tab(tab_scatter)
    
    def setup_charts_tab(self, parent):
        """设置图表标签页"""
        layout = QVBoxLayout(parent)
        
        # 创建matplotlib图形
        fig = Figure(figsize=(12, 8), dpi=100)
        canvas = FigureCanvas(fig)
        
        # 添加工具栏
        toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        
        # 创建子图
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        
        # 1. 节点生成数对比（柱状图）
        algorithms = ['纯Minimax', 'α-β剪枝']
        avg_nodes = [np.mean(self.minimax_nodes), np.mean(self.ab_nodes)]
        bars1 = ax1.bar(algorithms, avg_nodes, color=['#4A90D9', '#50B86C'], 
                        edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('平均节点生成数（个）', fontsize=12)
        ax1.set_title('节点生成数对比', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars1, avg_nodes):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{val:.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # 添加削减比例
        reduction = (avg_nodes[0] - avg_nodes[1]) / avg_nodes[0] * 100
        ax1.annotate(f'↓ {reduction:.1f}%', xy=(1, avg_nodes[1]), 
                    xytext=(1.15, avg_nodes[1] + 50),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=12, color='red', fontweight='bold')
        
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # 2. 决策耗时对比（柱状图）
        avg_times = [np.mean(self.minimax_times), np.mean(self.ab_times)]
        bars2 = ax2.bar(algorithms, avg_times, color=['#4A90D9', '#50B86C'], 
                        edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('平均决策耗时（秒）', fontsize=12)
        ax2.set_title('决策耗时对比', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars2, avg_times):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{val:.3f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        reduction_time = (avg_times[0] - avg_times[1]) / avg_times[0] * 100
        ax2.annotate(f'↓ {reduction_time:.1f}%', xy=(1, avg_times[1]), 
                    xytext=(1.15, avg_times[1] + 0.02),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=12, color='red', fontweight='bold')
        
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        # 3. 评价耗时占比对比（堆叠柱状图）
        minimax_total = np.mean(self.minimax_times)
        minimax_eval = np.mean(self.minimax_evals)
        minimax_other = minimax_total - minimax_eval
        
        ab_total = np.mean(self.ab_times)
        ab_eval = np.mean(self.ab_evals)
        ab_other = ab_total - ab_eval
        
        x = np.arange(2)
        width = 0.6
        
        bars_eval = ax3.bar(x, [minimax_eval, ab_eval], width, 
                           label='评价耗时', color='#E74C3C')
        bars_other = ax3.bar(x, [minimax_other, ab_other], width, 
                            bottom=[minimax_eval, ab_eval],
                            label='其他耗时', color='#95A5A6')
        
        ax3.set_xticks(x)
        ax3.set_xticklabels(['纯Minimax', 'α-β剪枝'])
        ax3.set_ylabel('耗时（秒）', fontsize=12)
        ax3.set_title('评价耗时占比分析', fontsize=14, fontweight='bold')
        ax3.legend(loc='upper right')
        
        # 添加百分比标签
        for i, (eval_val, other_val) in enumerate(zip([minimax_eval, ab_eval], 
                                                       [minimax_other, ab_other])):
            total = eval_val + other_val
            eval_pct = eval_val / total * 100
            ax3.text(i, eval_val/2, f'{eval_pct:.1f}%', ha='center', va='center', 
                    fontsize=10, color='white', fontweight='bold')
        
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        
        # 4. 性能提升比例（雷达图/柱状图）
        improvements = [
            reduction,
            reduction_time,
            (np.mean(self.minimax_evals) - np.mean(self.ab_evals)) / np.mean(self.minimax_evals) * 100
        ]
        categories = ['节点数缩减', '耗时缩减', '评价耗时缩减']
        colors = ['#E67E22', '#E74C3C', '#3498DB']
        
        bars4 = ax4.bar(categories, improvements, color=colors, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('提升比例（%）', fontsize=12)
        ax4.set_title('性能提升比例', fontsize=14, fontweight='bold')
        ax4.set_ylim(0, 100)
        ax4.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
        
        for bar, val in zip(bars4, improvements):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        fig.tight_layout()
        canvas.draw()
    
    def setup_table_tab(self, parent):
        """设置数据表格标签页"""
        layout = QVBoxLayout(parent)
        
        # 创建分组框
        group_box = QGroupBox("实验数据详情")
        group_layout = QVBoxLayout(group_box)
        
        # 创建表格
        table = QTableWidget()
        table.setRowCount(len(self.node_counts))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['序号', '节点生成数', '总耗时(秒)', '评价耗时(秒)', '算法类型'])
        
        # 填充数据
        for i in range(len(self.node_counts)):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            table.setItem(i, 1, QTableWidgetItem(str(self.node_counts[i])))
            table.setItem(i, 2, QTableWidgetItem(f'{self.time_costs[i]:.4f}'))
            table.setItem(i, 3, QTableWidgetItem(f'{self.eval_times[i]:.4f}'))
            
            if i < 7:
                table.setItem(i, 4, QTableWidgetItem('纯Minimax算法'))
                table.item(i, 4).setBackground(Qt.lightGray)
            else:
                table.setItem(i, 4, QTableWidgetItem('α-β剪枝算法'))
                table.item(i, 4).setBackground(Qt.green)
        
        # 设置表格样式
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.resizeColumnsToContents()
        
        group_layout.addWidget(table)
        layout.addWidget(group_box)
        
        # 添加统计摘要
        summary_group = QGroupBox("统计摘要")
        summary_layout = QHBoxLayout(summary_group)
        
        # 纯Minimax统计
        minimax_group = QGroupBox("纯Minimax算法")
        minimax_layout = QVBoxLayout(minimax_group)
        minimax_layout.addWidget(QLabel(f"平均节点数: {np.mean(self.minimax_nodes):.0f}"))
        minimax_layout.addWidget(QLabel(f"平均总耗时: {np.mean(self.minimax_times):.4f}秒"))
        minimax_layout.addWidget(QLabel(f"平均评价耗时: {np.mean(self.minimax_evals):.4f}秒"))
        minimax_layout.addWidget(QLabel(f"评价耗时占比: {np.mean(self.minimax_evals)/np.mean(self.minimax_times)*100:.1f}%"))
        
        # α-β剪枝统计
        ab_group = QGroupBox("α-β剪枝算法")
        ab_layout = QVBoxLayout(ab_group)
        ab_layout.addWidget(QLabel(f"平均节点数: {np.mean(self.ab_nodes):.0f}"))
        ab_layout.addWidget(QLabel(f"平均总耗时: {np.mean(self.ab_times):.4f}秒"))
        ab_layout.addWidget(QLabel(f"平均评价耗时: {np.mean(self.ab_evals):.4f}秒"))
        ab_layout.addWidget(QLabel(f"评价耗时占比: {np.mean(self.ab_evals)/np.mean(self.ab_times)*100:.1f}%"))
        
        # 性能提升
        perf_group = QGroupBox("性能提升")
        perf_layout = QVBoxLayout(perf_group)
        node_improve = (np.mean(self.minimax_nodes) - np.mean(self.ab_nodes)) / np.mean(self.minimax_nodes) * 100
        time_improve = (np.mean(self.minimax_times) - np.mean(self.ab_times)) / np.mean(self.minimax_times) * 100
        eval_improve = (np.mean(self.minimax_evals) - np.mean(self.ab_evals)) / np.mean(self.minimax_evals) * 100
        
        perf_layout.addWidget(QLabel(f"节点数削减: {node_improve:.1f}%"))
        perf_layout.addWidget(QLabel(f"总耗时削减: {time_improve:.1f}%"))
        perf_layout.addWidget(QLabel(f"评价耗时削减: {eval_improve:.1f}%"))
        
        summary_layout.addWidget(minimax_group)
        summary_layout.addWidget(ab_group)
        summary_layout.addWidget(perf_group)
        
        layout.addWidget(summary_group)
    
    def setup_stats_tab(self, parent):
        """设置统计分析标签页"""
        layout = QVBoxLayout(parent)
        
        # 创建matplotlib图形
        fig = Figure(figsize=(12, 8), dpi=100)
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        # 子图1：节点数分布直方图
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.hist(self.minimax_nodes, bins=5, alpha=0.7, label='纯Minimax', color='#4A90D9', edgecolor='black')
        ax1.hist(self.ab_nodes, bins=5, alpha=0.7, label='α-β剪枝', color='#50B86C', edgecolor='black')
        ax1.set_xlabel('节点生成数（个）', fontsize=11)
        ax1.set_ylabel('频次', fontsize=11)
        ax1.set_title('节点数分布直方图', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3, linestyle='--')
        
        # 子图2：耗时分布直方图
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.hist(self.minimax_times, bins=5, alpha=0.7, label='纯Minimax', color='#4A90D9', edgecolor='black')
        ax2.hist(self.ab_times, bins=5, alpha=0.7, label='α-β剪枝', color='#50B86C', edgecolor='black')
        ax2.set_xlabel('决策耗时（秒）', fontsize=11)
        ax2.set_ylabel('频次', fontsize=11)
        ax2.set_title('耗时分布直方图', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3, linestyle='--')
        
        # 子图3：箱线图对比
        ax3 = fig.add_subplot(2, 2, 3)
        data_to_plot = [self.minimax_nodes, self.ab_nodes]
        bp = ax3.boxplot(data_to_plot, labels=['纯Minimax', 'α-β剪枝'], patch_artist=True)
        bp['boxes'][0].set_facecolor('#4A90D9')
        bp['boxes'][1].set_facecolor('#50B86C')
        ax3.set_ylabel('节点生成数（个）', fontsize=11)
        ax3.set_title('节点数箱线图对比', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        
        # 子图4：耗时箱线图对比
        ax4 = fig.add_subplot(2, 2, 4)
        data_to_plot_time = [self.minimax_times, self.ab_times]
        bp2 = ax4.boxplot(data_to_plot_time, labels=['纯Minimax', 'α-β剪枝'], patch_artist=True)
        bp2['boxes'][0].set_facecolor('#4A90D9')
        bp2['boxes'][1].set_facecolor('#50B86C')
        ax4.set_ylabel('决策耗时（秒）', fontsize=11)
        ax4.set_title('耗时箱线图对比', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        fig.tight_layout()
        canvas.draw()
    
    def setup_scatter_tab(self, parent):
        """设置散点图分析标签页"""
        layout = QVBoxLayout(parent)
        
        # 创建matplotlib图形
        fig = Figure(figsize=(10, 8), dpi=100)
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        ax = fig.add_subplot(111)
        
        # 绘制散点图
        ax.scatter(self.minimax_nodes, self.minimax_times, s=100, c='#4A90D9', 
                  marker='o', label='纯Minimax算法', alpha=0.7, edgecolors='black', linewidth=1)
        ax.scatter(self.ab_nodes, self.ab_times, s=100, c='#50B86C', 
                  marker='s', label='α-β剪枝算法', alpha=0.7, edgecolors='black', linewidth=1)
        
        # 标注平均值点
        avg_minimax = (np.mean(self.minimax_nodes), np.mean(self.minimax_times))
        avg_ab = (np.mean(self.ab_nodes), np.mean(self.ab_times))
        
        ax.scatter([avg_minimax[0]], [avg_minimax[1]], s=300, c='#4A90D9', 
                  marker='*', edgecolors='black', linewidth=2, zorder=5, label='Minimax均值')
        ax.scatter([avg_ab[0]], [avg_ab[1]], s=300, c='#50B86C', 
                  marker='*', edgecolors='black', linewidth=2, zorder=5, label='α-β均值')
        
        # 添加趋势线
        z1 = np.polyfit(self.minimax_nodes, self.minimax_times, 1)
        p1 = np.poly1d(z1)
        x_line1 = np.linspace(min(self.minimax_nodes), max(self.minimax_nodes), 100)
        ax.plot(x_line1, p1(x_line1), color='#4A90D9', linestyle='--', alpha=0.7, linewidth=2)
        
        z2 = np.polyfit(self.ab_nodes, self.ab_times, 1)
        p2 = np.poly1d(z2)
        x_line2 = np.linspace(min(self.ab_nodes), max(self.ab_nodes), 100)
        ax.plot(x_line2, p2(x_line2), color='#50B86C', linestyle='--', alpha=0.7, linewidth=2)
        
        # 添加数据标签
        for i, (x, y) in enumerate(zip(self.minimax_nodes, self.minimax_times)):
            ax.annotate(f'{y:.3f}s', (x, y), xytext=(5, 5), textcoords='offset points', 
                       fontsize=8, alpha=0.7)
        
        for i, (x, y) in enumerate(zip(self.ab_nodes, self.ab_times)):
            ax.annotate(f'{y:.3f}s', (x, y), xytext=(5, 5), textcoords='offset points', 
                       fontsize=8, alpha=0.7)
        
        ax.set_xlabel('节点生成数（个）', fontsize=12)
        ax.set_ylabel('决策耗时（秒）', fontsize=12)
        ax.set_title('节点数-耗时关系散点图', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(alpha=0.3, linestyle='--')
        
        # 添加相关系数标注
        corr_minimax = np.corrcoef(self.minimax_nodes, self.minimax_times)[0, 1]
        corr_ab = np.corrcoef(self.ab_nodes, self.ab_times)[0, 1]
        
        ax.text(0.05, 0.95, f'Minimax相关系数: {corr_minimax:.3f}', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#4A90D9', alpha=0.3))
        ax.text(0.05, 0.88, f'α-β剪枝相关系数: {corr_ab:.3f}', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#50B86C', alpha=0.3))
        
        fig.tight_layout()
        canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = AlphaBetaAnalysisWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()