# 鄞响新媒体刷量工具
import tkinter as tk
from threading import Thread
from yzNews import clickCalculator, autoReflash, finalInfo


def startBrush():
    count = int(count_entry.get())
    url = url_entry.get()

    brush_thread = Thread(target=mainProc, args=(count, url))
    brush_thread.start()


def mainProc(_count, _url):
    '''
    主程序入口，为各线程分配点击次数，同时控制按钮可用状态
    '''
    start_button["state"] = "disabled"
    clickCounts = clickCalculator(_count)
    autoReflash(clickCounts, _url)
    finalInfo()
    start_button["state"] = "normal"


# 创建主窗口
root = tk.Tk()
root.title("鄞响新媒体阅读量加速器")
window_width = 400
window_height = 100
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 创建一个 Frame，用于容纳所有组件
frame = tk.Frame(root)
frame.grid()
#frame.pack(expand=True)

# 标签和输入框：助力次数
count_label = tk.Label(frame, text="助力次数：")
count_label.grid(row=0,column=0,padx=10,pady=10)
count_entry = tk.Entry(frame, width=10)
count_entry.grid(row=0,column=1,padx=10,pady=10)

# 标签和输入框：目标页面URL
url_label = tk.Label(frame, text="目标页面URL：")
url_label.grid(row=1,column=0,padx=10,pady=10)
url_entry = tk.Entry(frame, width=30)
url_entry.grid(row=1,column=1,columnspan=2,padx=10,pady=10)

# 开始助力按钮
start_button = tk.Button(frame, text="开始助力", command=startBrush)
start_button.grid(row=0,column=2,padx=10,pady=10)
#start_button.pack()

# 运行主循环
root.mainloop()
