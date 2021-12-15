import tkinter as tk
from tkinter import ttk

root = tk.Tk()
# 设置窗口大小
winWidth = 900
winHeight = 600
# 获取屏幕分辨率
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)

# 设置主窗口标题
root.title("文件批量编辑工具")
# 设置窗口初始位置在屏幕居中
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
# 设置窗口图标
root.iconbitmap("./image/icon.ico")
# 设置窗口宽高固定
root.resizable(0, 0)

# 定义列的名称
# 顶层
tab = ttk.Notebook(root)
frm1 = tk.Frame(tab, bg="red")
tab1 = tab.add(frm1, text="1.PDF工具")

frm2 = tk.Frame(tab, bg="yellow")
tab2 = tab.add(frm2, text="2.图片工具")

frm3 = tk.Frame(tab, bg="blue")
tab3 = tab.add(frm3, text="3.word工具")

frm4 = tk.Frame(tab, bg="PeachPuff")
tab4 = tab.add(frm4, text="4.excel工具")

frm5 = tk.Frame(tab, bg="Lime")
tab5 = tab.add(frm5, text="5.ppt工具")

tab.pack(expand=True, fill=tk.BOTH)

# 二层
# 二层1,"https://smallpdf.com/cn/pdf-converter"
tab1_0 = ttk.Notebook(frm1)
frm1_1 = tk.Frame(frm1, bg="red")
tab1_1 = tab1_0.add(frm1_1, text="1.1转档&压缩&分割&合并")
frm1_2 = tk.Frame(frm1, bg="red")
tab1_2 = tab1_0.add(frm1_2, text="1.2检视＆编辑")
frm1_3 = tk.Frame(frm1, bg="red")
tab1_3 = tab1_0.add(frm1_3, text="1.3从PDF转换为")
frm1_4 = tk.Frame(frm1, bg="red")
tab1_4 = tab1_0.add(frm1_4, text="1.4签署＆安全选项")
tab1_0.pack(expand=True, fill=tk.BOTH)

# 三层
# 三层1.PDF工具1.1转档&压缩&分割&合并
tab1_1_0 = ttk.Notebook(frm1_1)
frm1_1_1 = tk.Frame(frm1_1, bg="red")
tab1_1_1 = tab1_1_0.add(frm1_1_1, text="1.1.1压缩PDF")
frm1_1_2 = tk.Frame(frm1_1, bg="red")
tab1_1_2 = tab1_1_0.add(frm1_1_2, text="1.1.2分割PDF")
frm1_1_3 = tk.Frame(frm1_1, bg="red")
tab1_1_3 = tab1_1_0.add(frm1_1_3, text="1.1.3合并PDF")
tab1_1_0.pack(expand=True, fill=tk.BOTH)

# 三层1.PDF工具1.2检视＆编辑
tab1_2_0 = ttk.Notebook(frm1_2)
frm1_2_1 = tk.Frame(frm1_2, bg="red")
tab1_2_1 = tab1_2_0.add(frm1_2_1, text="1.2.1PDF排页数")
frm1_2_2 = tk.Frame(frm1_2, bg="red")
tab1_2_2 = tab1_2_0.add(frm1_2_2, text="1.2.2PDF删除页面")
frm1_2_3 = tk.Frame(frm1_2, bg="red")
tab1_2_3 = tab1_2_0.add(frm1_2_3, text="1.2.3旋转PDF")
tab1_2_0.pack(expand=True, fill=tk.BOTH)

# 设置选中tab1
tab.select(frm1)

# 1.1.2分割PDF
f1_1_2_b1 = tk.Button(frm1_1_2, text="开始切割按钮")
f1_1_2_b1.pack()

# 主界面循环
root.mainloop()
