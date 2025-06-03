import random
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D  # 导入Line2D用于自定义图例


class EconomicGame:
    def __init__(self, root):
        self.root = root
        self.root.title("经济政策模拟器")
        self.root.geometry("1500x900")

        # 设置matplotlib字体为黑体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        # 应用主题
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # 设置字体
        self.style.configure(".", font=("SimHei", 10))  # 使用黑体（SimHei）
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TLabelframe.Label", font=("SimHei", 11, "bold"))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("Title.TLabel", font=("SimHei", 24, "bold"))

        # 设置颜色
        self.bg_color = "#f0f5f9"  # 浅蓝色背景
        self.frame_bg_color = "#e0ecea"  # 浅灰色边框
        self.chart_bg_color = "#f8f9fa"  # 图表背景色
        self.text_color = "#333333"  # 文字颜色

        # 设置圆角样式
        self.style.layout("RoundedFrame", [
            ("RoundedFrame.border", {"sticky": "nswe", "children": [
                ("RoundedFrame.background", {"sticky": "nswe"})
            ]})
        ])
        self.style.configure("RoundedFrame", background=self.bg_color, borderwidth=2, relief="solid",
                             bordercolor=self.frame_bg_color,
                             lightcolor=self.frame_bg_color, darkcolor=self.frame_bg_color)

        # 游戏参数
        self.round = 1
        self.max_rounds = 10
        self.inflation_rate = 2.0
        self.unemployment_rate = 5.0
        self.interest_rate = 4.0
        self.gdp_growth = 2.5
        self.budget_balance = 0
        self.popular_support = 50
        self.economic_health = "稳定"
        self.policy_effects = {}
        self.economic_targets = {
            "inflation": (1.0, 3.0),
            "unemployment": (3.0, 6.0),
            "gdp_growth": (2.0, 4.0),
            "budget": (-20, 20),
            "support": (60, 100)
        }
        self.advisors = []
        self.advisor_visible = False

        # 初始化历史数据
        self.history = {
            "rounds": [0],
            "inflation": [self.inflation_rate],
            "unemployment": [self.unemployment_rate],
            "interest": [self.interest_rate],
            "gdp": [self.gdp_growth]
        }

        # 创建主框架
        self.create_widgets()

        # 初始化图表
        self.update_charts()

        # 显示欢迎信息
        self.show_welcome_message()

        # 初始化顾问
        self.init_advisors()

    def init_advisors(self):
        self.advisors = [
            {"name": "货币政策顾问", "specialty": "货币政策", "active": True},
            {"name": "财政政策顾问", "specialty": "财政政策", "active": True},
            {"name": "宏观经济顾问", "specialty": "经济预测", "active": True}
        ]

    def get_advisor_advice(self):
        advice = []

        if self.inflation_rate > self.economic_targets["inflation"][1]:
            advice.append("通货膨胀过高：建议提高利率或减少货币供应")
        elif self.inflation_rate < self.economic_targets["inflation"][0]:
            advice.append("通货膨胀过低：建议降低利率或增加货币供应")

        if self.unemployment_rate > self.economic_targets["unemployment"][1]:
            advice.append("失业率过高：建议增加政府支出或减税")
        elif self.unemployment_rate < self.economic_targets["unemployment"][0]:
            advice.append("失业率过低：可能会引发通胀，建议适度收紧政策")

        if self.gdp_growth < self.economic_targets["gdp_growth"][0]:
            advice.append("GDP增长疲软：建议刺激经济，降低利率或增加支出")

        if self.budget_balance < self.economic_targets["budget"][0]:
            advice.append("预算赤字过高：建议减少支出或增加税收")
        elif self.budget_balance > self.economic_targets["budget"][1]:
            advice.append("预算盈余过高：建议增加支出或减税")

        if self.popular_support < self.economic_targets["support"][0]:
            advice.append("民众支持率低：建议关注民生政策")

        return advice

    def create_widgets(self):
        title_frame = ttk.Frame(self.root, style="RoundedFrame")
        title_frame.pack(fill=tk.X, pady=(0, 10), padx=20)
        title_label = ttk.Label(title_frame, text="经济政策模拟器", style="Title.TLabel")
        title_label.pack(pady=15)

        status_frame = ttk.Frame(self.root, style="RoundedFrame")
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        status_label = ttk.Label(status_frame, text="经济状态:", font=("SimHei", 11, "bold"))
        status_label.pack(side=tk.LEFT, padx=(0, 10))

        self.status_indicator = ttk.Label(status_frame, text="稳定", font=("SimHei", 11, "bold"),
                                          background="#27ae60", foreground="white", width=10)
        self.status_indicator.pack(side=tk.LEFT)

        main_frame = ttk.Frame(self.root, style="RoundedFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        left_frame = ttk.LabelFrame(main_frame, text="经济指标", style="RoundedFrame")
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5, ipadx=10, ipady=10)

        indicators = [
            ("通货膨胀率", "inflation_rate", "%", (1.0, 3.0)),
            ("失业率", "unemployment_rate", "%", (3.0, 6.0)),
            ("利率", "interest_rate", "%", (2.0, 6.0)),
            ("GDP增长率", "gdp_growth", "%", (2.0, 4.0)),
            ("预算平衡", "budget_balance", "十亿", (-20, 20)),
            ("民众支持率", "popular_support", "%", (60, 100))
        ]

        self.indicator_labels = {}
        for i, (name, attr, unit, target_range) in enumerate(indicators):
            frame = ttk.Frame(left_frame, style="RoundedFrame")
            frame.pack(fill=tk.X, pady=5, padx=10)

            label = ttk.Label(frame, text=f"{name}:", width=12, anchor="w")
            label.pack(side=tk.LEFT, padx=(0, 5))

            value_frame = ttk.Frame(frame, style="RoundedFrame")
            value_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

            value_label = ttk.Label(value_frame, text="--", font=("SimHei", 11, "bold"), width=6)
            value_label.pack(side=tk.LEFT)

            unit_label = ttk.Label(value_frame, text=unit)
            unit_label.pack(side=tk.LEFT, padx=(0, 10))

            target_label = ttk.Label(frame, text=f"目标: {target_range[0]}-{target_range[1]}{unit}",
                                     font=("SimHei", 8), foreground="#7f8c8d")
            target_label.pack(side=tk.RIGHT)

            self.indicator_labels[attr] = value_label

        advisor_frame = ttk.Frame(left_frame, style="RoundedFrame")
        advisor_frame.pack(fill=tk.X, pady=(15, 5), padx=10)

        self.advisor_button = ttk.Button(advisor_frame, text="经济顾问建议",
                                         command=self.toggle_advisor_advice)
        self.advisor_button.pack(fill=tk.X, pady=5, padx=10)

        self.advice_frame = ttk.LabelFrame(left_frame, text="顾问建议", style="RoundedFrame")
        self.advice_frame.pack(fill=tk.X, pady=5, padx=10)

        self.advice_text = tk.Text(self.advice_frame, wrap=tk.WORD, font=("SimHei", 9),
                                   bg="white", height=5, padx=5, pady=5)
        self.advice_text.pack(fill=tk.BOTH, expand=True)
        self.advice_text.config(state=tk.DISABLED)

        round_frame = ttk.Frame(left_frame, style="RoundedFrame")
        round_frame.pack(fill=tk.X, pady=(10, 0), padx=10)

        round_label = ttk.Label(round_frame, text="当前回合:")
        round_label.pack(side=tk.LEFT)

        self.round_value_label = ttk.Label(round_frame, text=f"{self.round}/{self.max_rounds}",
                                           font=("SimHei", 11, "bold"))
        self.round_value_label.pack(side=tk.LEFT, padx=5)

        center_frame = ttk.LabelFrame(main_frame, text="经济趋势", style="RoundedFrame")
        center_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5, ipadx=10, ipady=10)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 8), dpi=100)
        self.fig.patch.set_facecolor(self.chart_bg_color)
        self.ax1.set_facecolor(self.chart_bg_color)
        self.ax2.set_facecolor(self.chart_bg_color)

        self.canvas = FigureCanvasTkAgg(self.fig, master=center_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_frame = ttk.LabelFrame(main_frame, text="政策选择", style="RoundedFrame")
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5, ipadx=10, ipady=10)

        monetary_frame = ttk.LabelFrame(right_frame, text="货币政策", style="RoundedFrame")
        monetary_frame.pack(fill=tk.X, pady=5, padx=5)

        self.monetary_var = tk.StringVar(value="保持不变")
        monetary_options = ["提高利率", "降低利率", "增加货币供应", "减少货币供应", "量化宽松", "保持不变"]
        for option in monetary_options:
            rb = ttk.Radiobutton(monetary_frame, text=option, variable=self.monetary_var,
                                 value=option)
            rb.pack(anchor=tk.W, padx=5, pady=2)

        fiscal_frame = ttk.LabelFrame(right_frame, text="财政政策", style="RoundedFrame")
        fiscal_frame.pack(fill=tk.X, pady=5, padx=5)

        self.fiscal_var = tk.StringVar(value="保持不变")
        fiscal_options = ["增加政府支出", "减少政府支出", "增加税收", "减少税收", "结构性减税", "保持不变"]
        for option in fiscal_options:
            rb = ttk.Radiobutton(fiscal_frame, text=option, variable=self.fiscal_var,
                                 value=option)
            rb.pack(anchor=tk.W, padx=5, pady=2)

        button_frame = ttk.Frame(right_frame, style="RoundedFrame")
        button_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM, padx=10)

        self.execute_button = ttk.Button(button_frame, text="执行政策",
                                         command=self.execute_policy)
        self.execute_button.pack(pady=10, ipady=8)

        bottom_frame = ttk.LabelFrame(main_frame, text="事件与结果", style="RoundedFrame")
        bottom_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5, ipadx=10, ipady=10)

        self.result_text = tk.Text(bottom_frame, wrap=tk.WORD, font=("SimHei", 10),
                                   bg="white", height=20, padx=10, pady=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(bottom_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_columnconfigure(2, weight=2)

        main_frame.columnconfigure(0, minsize=250)
        main_frame.columnconfigure(1, minsize=500)
        main_frame.columnconfigure(2, minsize=300)

        self.advice_frame.pack_forget()

    def toggle_advisor_advice(self):
        if self.advisor_visible:
            self.advice_frame.pack_forget()
            self.advisor_button.config(text="经济顾问建议")
            self.advisor_visible = False
        else:
            advice = self.get_advisor_advice()
            self.advice_text.config(state=tk.NORMAL)
            self.advice_text.delete(1.0, tk.END)

            if advice:
                self.advice_text.insert(tk.END, "经济顾问建议:\n\n")
                for item in advice:
                    self.advice_text.insert(tk.END, f"• {item}\n")
            else:
                self.advice_text.insert(tk.END, "经济状况良好，无需特别建议。")

            self.advice_text.config(state=tk.DISABLED)
            self.advice_frame.pack(fill=tk.X, pady=5, padx=10)
            self.advisor_button.config(text="隐藏经济顾问建议")
            self.advisor_visible = True

    def show_welcome_message(self):
        welcome_text = (f"欢迎来到经济政策模拟器！\n\n"
                        f"你是国家的经济政策决策者，需要通过调整货币政策和财政政策来维持经济稳定。\n"
                        f"你的目标是在{self.max_rounds}个回合内，保持通货膨胀率、失业率和GDP增长率在合理范围内，"
                        f"同时维持较高的民众支持率。\n\n"
                        f"当前经济状况：\n"
                        f"- 通货膨胀率: {self.inflation_rate}%\n"
                        f"- 失业率: {self.unemployment_rate}%\n"
                        f"- GDP增长率: {self.gdp_growth}%\n"
                        f"- 利率: {self.interest_rate}%\n"
                        f"- 预算平衡: {self.budget_balance}十亿\n"
                        f"- 民众支持率: {self.popular_support}%\n\n"
                        f"请选择你的政策，然后点击'执行政策'按钮。\n\n"
                        f"提示：点击'经济顾问建议'按钮获取专业建议。")

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, welcome_text)

        self.update_indicators()
        self.update_economic_health()

    def update_economic_health(self):
        health_score = 0

        if self.economic_targets["inflation"][0] <= self.inflation_rate <= self.economic_targets["inflation"][1]:
            health_score += 1
        elif self.inflation_rate < self.economic_targets["inflation"][0]:
            health_score -= 0.5
        else:
            health_score -= 1

        if self.economic_targets["unemployment"][0] <= self.unemployment_rate <= self.economic_targets["unemployment"][1]:
            health_score += 1
        elif self.unemployment_rate > self.economic_targets["unemployment"][1]:
            health_score -= 1

        if self.economic_targets["gdp_growth"][0] <= self.gdp_growth <= self.economic_targets["gdp_growth"][1]:
            health_score += 1
        elif self.gdp_growth < self.economic_targets["gdp_growth"][0]:
            health_score -= 1

        if self.economic_targets["budget"][0] <= self.budget_balance <= self.economic_targets["budget"][1]:
            health_score += 0.5
        elif self.budget_balance < self.economic_targets["budget"][0]:
            health_score -= 0.5

        if self.popular_support >= self.economic_targets["support"][0]:
            health_score += 0.5
        else:
            health_score -= 0.5

        if health_score >= 3:
            self.economic_health = "健康"
            color = "#27ae60"
        elif health_score >= 1.5:
            self.economic_health = "稳定"
            color = "#f39c12"
        else:
            self.economic_health = "衰退"
            color = "#e74c3c"

        self.status_indicator.config(text=self.economic_health, background=color)

    def update_indicators(self):
        self.indicator_labels["inflation_rate"].config(text=f"{self.inflation_rate:.1f}")
        self.indicator_labels["unemployment_rate"].config(text=f"{self.unemployment_rate:.1f}")
        self.indicator_labels["interest_rate"].config(text=f"{self.interest_rate:.1f}")
        self.indicator_labels["gdp_growth"].config(text=f"{self.gdp_growth:.1f}")
        self.indicator_labels["budget_balance"].config(text=f"{self.budget_balance:.1f}")
        self.indicator_labels["popular_support"].config(text=f"{self.popular_support:.1f}")

        self.round_value_label.config(text=f"{self.round}/{self.max_rounds}")

        self.update_economic_health()

    def update_charts(self):
        self.ax1.clear()
        self.ax2.clear()

        # 确保有足够的数据点
        rounds = min(5, len(self.history["rounds"]))
        x = self.history["rounds"][-rounds:]
        inflation_history = self.history["inflation"][-rounds:]
        unemployment_history = self.history["unemployment"][-rounds:]
        gdp_history = self.history["gdp"][-rounds:]
        interest_history = self.history["interest"][-rounds:]

        # 创建自定义图例句柄
        custom_lines = [
            Line2D([0], [0], marker=' ', linestyle='none', label='通货膨胀率'),
            Line2D([0], [0], marker=' ', linestyle='none', label='失业率'),
            Line2D([0], [0], marker=' ', linestyle='none', label='GDP增长率'),
            Line2D([0], [0], marker=' ', linestyle='none', label='利率')
        ]

        # 绘制图表并设置图例为文字描述
        l1, = self.ax1.plot(x, inflation_history, 'r-o', linewidth=2, markersize=8)
        l2, = self.ax1.plot(x, unemployment_history, 'b-s', linewidth=2, markersize=8)
        self.ax1.set_title('通货膨胀率与失业率趋势', fontsize=12)
        self.ax1.set_ylabel('百分比(%)', fontsize=10)

        # 使用自定义图例句柄
        self.ax1.legend(handles=custom_lines[:2], loc='best', fontsize=9, frameon=False)

        self.ax1.grid(True, linestyle='--', alpha=0.7)

        self.ax1.axhspan(self.economic_targets["inflation"][0], self.economic_targets["inflation"][1],
                         color='green', alpha=0.1)
        self.ax1.axhspan(self.economic_targets["unemployment"][0], self.economic_targets["unemployment"][1],
                         color='blue', alpha=0.1)

        l3, = self.ax2.plot(x, gdp_history, 'g-o', linewidth=2, markersize=8)
        l4, = self.ax2.plot(x, interest_history, 'm-s', linewidth=2, markersize=8)
        self.ax2.set_title('GDP增长率与利率趋势', fontsize=12)
        self.ax2.set_xlabel('回合', fontsize=10)
        self.ax2.set_ylabel('百分比(%)', fontsize=10)

        # 使用自定义图例句柄
        self.ax2.legend(handles=custom_lines[2:], loc='best', fontsize=9, frameon=False)

        self.ax2.grid(True, linestyle='--', alpha=0.7)

        self.ax2.axhspan(self.economic_targets["gdp_growth"][0], self.economic_targets["gdp_growth"][1],
                         color='green', alpha=0.1)

        self.fig.tight_layout(pad=3.0)
        self.canvas.draw()

    def execute_policy(self):
        if self.round > self.max_rounds:
            messagebox.showinfo("游戏结束", "所有回合已完成！")
            return

        monetary_policy = self.monetary_var.get()
        fiscal_policy = self.fiscal_var.get()

        # 存储当前状态
        self.policy_effects[self.round] = {
            'inflation_rate': self.inflation_rate,
            'unemployment_rate': self.unemployment_rate,
            'interest_rate': self.interest_rate,
            'gdp_growth': self.gdp_growth,
            'budget_balance': self.budget_balance,
            'popular_support': self.popular_support,
            'monetary_policy': monetary_policy,
            'fiscal_policy': fiscal_policy
        }

        # 更新历史数据
        self.history["rounds"].append(self.round)
        self.history["inflation"].append(self.inflation_rate)
        self.history["unemployment"].append(self.unemployment_rate)
        self.history["interest"].append(self.interest_rate)
        self.history["gdp"].append(self.gdp_growth)

        monetary_effect = ""
        if monetary_policy == "提高利率":
            self.interest_rate += 0.5
            self.inflation_rate -= 0.7
            self.unemployment_rate += 0.4
            self.gdp_growth -= 0.3
            self.popular_support -= 2
            monetary_effect = "提高利率 0.5%。这抑制了通货膨胀，但导致失业率上升和经济增长放缓。"
        elif monetary_policy == "降低利率":
            self.interest_rate -= 0.5
            self.inflation_rate += 0.7
            self.unemployment_rate -= 0.4
            self.gdp_growth += 0.3
            self.popular_support += 2
            monetary_effect = "降低利率 0.5%。这刺激了经济增长和通货膨胀，同时降低了失业率。"
        elif monetary_policy == "增加货币供应":
            self.inflation_rate += 1.0
            self.unemployment_rate -= 0.6
            self.gdp_growth += 0.5
            self.popular_support += 3
            monetary_effect = "增加货币供应。这刺激了经济增长，降低了失业率，但加剧了通货膨胀。"
        elif monetary_policy == "减少货币供应":
            self.inflation_rate -= 1.0
            self.unemployment_rate += 0.6
            self.gdp_growth -= 0.5
            self.popular_support -= 3
            monetary_effect = "减少货币供应。这抑制了通货膨胀，但导致失业率上升和经济增长放缓。"
        elif monetary_policy == "量化宽松":
            self.inflation_rate += 0.8
            self.unemployment_rate -= 0.5
            self.gdp_growth += 0.4
            self.popular_support += 2
            monetary_effect = "实施量化宽松政策。这增加了市场流动性，刺激了经济增长，但也可能引发通货膨胀。"
        else:
            monetary_effect = "保持货币政策不变。"

        fiscal_effect = ""
        if fiscal_policy == "增加政府支出":
            self.budget_balance -= 5
            self.gdp_growth += 0.5
            self.unemployment_rate -= 0.3
            self.inflation_rate += 0.5
            self.popular_support += 3
            fiscal_effect = "增加政府支出 50 亿。这刺激了经济增长，降低了失业率，但增加了通货膨胀和预算赤字。"
        elif fiscal_policy == "减少政府支出":
            self.budget_balance += 5
            self.gdp_growth -= 0.5
            self.unemployment_rate += 0.3
            self.inflation_rate -= 0.5
            self.popular_support -= 3
            fiscal_effect = "减少政府支出 50 亿。这减少了预算赤字和通货膨胀，但导致经济增长放缓和失业率上升。"
        elif fiscal_policy == "增加税收":
            self.budget_balance += 7
            self.gdp_growth -= 0.4
            self.inflation_rate -= 0.4
            self.popular_support -= 4
            fiscal_effect = "增加税收 70 亿。这增加了预算盈余并抑制了通货膨胀，但导致经济增长放缓。"
        elif fiscal_policy == "减少税收":
            self.budget_balance -= 7
            self.gdp_growth += 0.4
            self.inflation_rate += 0.4
            self.popular_support += 4
            fiscal_effect = "减少税收 70 亿。这刺激了经济增长和通货膨胀，但增加了预算赤字。"
        elif fiscal_policy == "结构性减税":
            self.budget_balance -= 3
            self.gdp_growth += 0.3
            self.unemployment_rate -= 0.2
            self.popular_support += 2
            fiscal_effect = "实施结构性减税。这促进了特定产业的发展，提高了生产效率，对经济增长和就业有积极影响。"
        else:
            fiscal_effect = "保持财政政策不变。"

        phillips_effect = random.uniform(-0.3, 0.3)
        self.inflation_rate += phillips_effect
        self.unemployment_rate -= phillips_effect * 0.5

        random_event, event_effect = self.generate_random_event()

        result_text = (f"第 {self.round} 回合结果:\n"
                       f"========================================\n"
                       f"货币政策: {monetary_policy}\n"
                       f"{monetary_effect}\n\n"
                       f"财政政策: {fiscal_policy}\n"
                       f"{fiscal_effect}\n\n"
                       f"随机事件: {random_event}\n"
                       f"{event_effect}\n\n"
                       f"当前经济指标:\n"
                       f"- 通货膨胀率: {self.inflation_rate:.1f}%\n"
                       f"- 失业率: {self.unemployment_rate:.1f}%\n"
                       f"- GDP增长率: {self.gdp_growth:.1f}%\n"
                       f"- 利率: {self.interest_rate:.1f}%\n"
                       f"- 预算平衡: {self.budget_balance:.1f} 十亿\n"
                       f"- 民众支持率: {self.popular_support:.1f}%\n"
                       f"- 经济状态: {self.economic_health}\n\n")

        result_text += "经济原理解释:\n"
        if monetary_policy in ["提高利率", "降低利率"]:
            result_text += ("利率政策是央行调控经济的重要工具。提高利率通常会抑制通货膨胀，因为它增加"
                            "了借贷成本，减少了消费和投资，从而降低经济活动。相反，降低利率则会刺激经济增长。")
        elif monetary_policy in ["增加货币供应", "减少货币供应", "量化宽松"]:
            result_text += ("货币供应量的变化直接影响通货膨胀和经济增长。增加货币供应可以刺激短期经济增长，"
                            "但也可能导致通货膨胀上升，因为市场上有更多的钱追逐相同数量的商品和服务。")

        if fiscal_policy in ["增加政府支出", "减少政府支出"]:
            result_text += "\n政府支出是财政政策的重要组成部分。增加政府支出可以直接刺激经济增长，创造就业机会，但也可能增加预算赤字。"
        elif fiscal_policy in ["增加税收", "减少税收", "结构性减税"]:
            result_text += "\n税收政策影响居民可支配收入和企业投资。增加税收可以减少经济中的总需求，抑制通货膨胀，但也可能减缓经济增长。"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        self.update_indicators()
        self.update_charts()

        self.round += 1
        if self.round > self.max_rounds:
            self.execute_button.config(text="游戏结束", state=tk.DISABLED)
            self.show_game_results()
        else:
            if self.popular_support <= 0:
                self.execute_button.config(text="游戏结束", state=tk.DISABLED)
                messagebox.showinfo("游戏结束", "你的民众支持率已降至0！\n\n你失去了职位。")
            elif self.inflation_rate > 15 or self.unemployment_rate > 15:
                self.execute_button.config(text="游戏结束", state=tk.DISABLED)
                messagebox.showinfo("游戏结束", "经济陷入严重衰退！\n\n你被解职了。")

    def generate_random_event(self):
        events = [
            ("国际油价上涨", "这导致国内能源价格上升，推高了通货膨胀率。",
             {"inflation_rate": 1.2, "gdp_growth": -0.3}),
            ("技术突破", "这提高了生产效率，促进了经济增长并降低了失业率。",
             {"gdp_growth": 0.8, "unemployment_rate": -0.5}),
            ("贸易战升级", "这阻碍了国际贸易，导致经济增长放缓。",
             {"gdp_growth": -0.6, "inflation_rate": 0.5}),
            ("消费者信心增强", "这刺激了消费，促进了经济增长。",
             {"gdp_growth": 0.7, "unemployment_rate": -0.3}),
            ("自然灾害", "这破坏了基础设施，导致经济增长放缓。",
             {"gdp_growth": -0.5, "budget_balance": -3}),
            ("央行注入流动性", "这降低了市场利率，刺激了投资。",
             {"interest_rate": -0.4, "gdp_growth": 0.4}),
            ("房地产市场繁荣", "这刺激了相关产业，促进了经济增长。",
             {"gdp_growth": 0.6, "inflation_rate": 0.4}),
            ("股市崩盘", "这导致消费者信心下降，经济增长放缓。",
             {"gdp_growth": -0.7, "popular_support": -5}),
            ("金融危机", "这导致信贷紧缩，经济增长停滞。",
             {"gdp_growth": -1.0, "unemployment_rate": 1.0}),
            ("全球疫情爆发", "这导致供应链中断，经济增长大幅放缓。",
             {"gdp_growth": -1.5, "unemployment_rate": 1.5, "popular_support": -8}),
            ("汇率波动", "本币升值影响出口，导致贸易收支变化。",
             {"gdp_growth": -0.2}),
            ("新兴市场危机", "全球资本流动变化，影响国内金融市场。",
             {"interest_rate": 0.5, "budget_balance": -1}),
            ("无事件", "本回合经济运行平稳，没有重大事件发生。", {})
        ]

        event_weights = [1.0] * len(events)

        if self.economic_health == "衰退":
            event_weights[0] = 1.5
            event_weights[2] = 1.5
            event_weights[4] = 1.5
            event_weights[7] = 1.5
            event_weights[8] = 1.5
            event_weights[9] = 1.2
            event_weights[10] = 0.8
            event_weights[11] = 1.3
        elif self.inflation_rate > 5:
            event_weights[0] = 1.5
            event_weights[2] = 1.2
            event_weights[5] = 0.8

        event_name, event_description, effects = random.choices(events, weights=event_weights, k=1)[0]

        for attr, value in effects.items():
            current_value = getattr(self, attr, None)
            if current_value is not None:
                setattr(self, attr, current_value + value)

        return event_name, event_description

    def show_game_results(self):
        score = 0

        inflation_diff = abs(self.inflation_rate - 2.0)
        score += max(0, 20 - inflation_diff * 4)

        if 4.0 <= self.unemployment_rate <= 6.0:
            score += 20
        else:
            unemployment_diff = min(abs(self.unemployment_rate - 4.0), abs(self.unemployment_rate - 6.0))
            score += max(0, 20 - unemployment_diff * 4)

        if 2.0 <= self.gdp_growth <= 4.0:
            score += 20
        else:
            gdp_diff = min(abs(self.gdp_growth - 2.0), abs(self.gdp_growth - 4.0))
            score += max(0, 20 - gdp_diff * 10)

        budget_diff = abs(self.budget_balance)
        score += max(0, 15 - budget_diff * 1.5)

        if self.popular_support >= 70:
            score += 25
        else:
            score += self.popular_support * 0.357

        final_stats = (f"最终经济指标:\n"
                       f"- 通货膨胀率: {self.inflation_rate:.1f}%\n"
                       f"- 失业率: {self.unemployment_rate:.1f}%\n"
                       f"- GDP增长率: {self.gdp_growth:.1f}%\n"
                       f"- 利率: {self.interest_rate:.1f}%\n"
                       f"- 预算平衡: {self.budget_balance:.1f} 十亿\n"
                       f"- 民众支持率: {self.popular_support:.1f}%\n\n"
                       f"你的最终得分: {score:.1f}/100\n\n")

        if score >= 90:
            evaluation = "优秀！你是一位杰出的经济政策制定者，成功维持了经济的稳定增长和低通胀。"
        elif score >= 75:
            evaluation = "良好！你有效地管理了国家经济，大部分经济指标处于合理范围。"
        elif score >= 60:
            evaluation = "及格。经济表现一般，有些指标需要改进。"
        else:
            evaluation = "需要改进。经济面临一些挑战，你可能需要重新考虑你的政策策略。"

        messagebox.showinfo("游戏结束", final_stats + evaluation)

        self.result_text.insert(tk.END, "\n" + "=" * 40 + "\n")
        self.result_text.insert(tk.END, "游戏结束！\n\n")
        self.result_text.insert(tk.END, final_stats)
        self.result_text.insert(tk.END, evaluation)


if __name__ == "__main__":
    root = tk.Tk()
    game = EconomicGame(root)
    root.mainloop()