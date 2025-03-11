#　GitHub Copilot 使用
# TKinterを使用してタブで２枚のグラフを表示したい。モジュール毎にしてほしい。また、リアルタイムプロットしたい
# 2枚あるグラフのタブ画面を順番に自動で表示したい が、１回だけでよい

import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.pyplot as plt
#

class RealTimePlot:
    def __init__(self, root):

        self.root = root
        self.root.title("Real-Time Plot with Tabs")

        self.tab_control = ttk.Notebook(root)
        self.tab0 = ttk.Frame(self.tab_control)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab0, text='Control')
        self.tab_control.add(self.tab1, text='Graph 1')
        self.tab_control.add(self.tab2, text='Graph 2')
        self.tab_control.pack(expand=1, fill='both')

        self.start_button = tk.Button(self.tab0, text="Start Plotting", command=self.Plot_Start)
        self.start_button.pack(side=tk.TOP, pady=10)

    def Plot_Start(self):

        print("Starting plots")
        self.t_interval = self.t_interval_init = self.rest_time = 1.0 # sec   Rest time 
        self.time_0 = self.time_old = time.time()

        #Enable automatically switch tabs once
        self.current_tab = 0
        self.Switch_Tabs()

        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()

        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab1)
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab2)
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.num = 0
        self.x_data1 = []
        self.y_data1 = []
        self.x_data2 = []
        self.y_data2 = []

        while True:
            self.Update_Graph1()
            self.Update_Graph2()   

            time.sleep(self.rest_time)
            self.Adjust_Time()
            self.num += 1
            if self.num > 100:
                break
        return

    def Update_Graph1(self):

        self.x_data1.append(len(self.x_data1))
        self.y_data1.append(random.randint(0, 10))

        self.ax1.clear()
        self.ax1.plot(self.x_data1, self.y_data1)
        self.canvas1.draw()
        self.canvas1.flush_events()

        return

    def Update_Graph2(self):

        self.x_data2.append(len(self.x_data2))
        self.y_data2.append(random.randint(0, 10))

        self.ax2.clear()
        self.ax2.plot(self.x_data2, self.y_data2)
        self.canvas2.draw()
        self.canvas2.flush_events()

        return

    def Switch_Tabs(self):
        if self.current_tab < 3:
            self.tab_control.select(self.current_tab)
            self.current_tab += 1
            self.root.after(100, self.Switch_Tabs)  # Switch tabs every 0.1 seconds
        return
    
    def Adjust_Time(self):
        time_instant = time.time()
        elapsed_time = time_instant - self.time_0
        #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

        # teurn around time
        turnaround_time =  time_instant - self.time_old
        self.time_old = time_instant

        # adjust rest_time
        self.rest_time  = 1 - (elapsed_time % 1)
        print('elapsed_time =', f'{elapsed_time:.3f}')
        print(' turnaround_time =', f'{turnaround_time:.3f}',',  rest_time = ',  f'{self.rest_time:.3f}')

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlot(root)
    root.mainloop()
