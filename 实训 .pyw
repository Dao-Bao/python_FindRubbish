import tkinter       #windows下窗体库
import tkinter.messagebox,tkinter.simpledialog
import os,os.path
import threading

rubbishExt = ['.tmp','.bak','.old','.$$$']

class Window:
    def __init__(self):
        self.root = tkinter.Tk()

        # 创建菜单
        menu = tkinter.Menu(self.root)

        # 创建“系统”子菜单
        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="关于......", command=self.MenuAbout)#调用MenuAbout函数
        submenu.add_separator()     #分割线
        submenu.add_command(label="退出", command=self.MenuExit)
        menu.add_cascade(label="系统", menu=submenu)

        # 创建“清理”子菜单
        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="扫描垃圾文件", command=self.MenuScanRubbish)
        submenu.add_separator()     #分割线
        submenu.add_command(label="删除垃圾文件", command=self.MenuDelRubbish)
        menu.add_cascade(label="清理", menu=submenu)

        # 创建“查找”子菜单
        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="搜索大文件", command=self.MenuScanBigFile)
        submenu.add_separator()     #分割线
        submenu.add_command(label="按名称搜索大文件", command=self.MenuSearchFile)
        menu.add_cascade(label="查找", menu=submenu)

        self.root.config(menu=menu)     #创建主窗体

        # 创建标签，用于显示状态信息
        self.progress = tkinter.Label(self.root, anchor=tkinter.W, text='状态', bitmap='hourglass', compound='left')
        self.progress.place(x=10, y=370, width=480, height=15)

        # 创建文本框，显示文件列表
        self.flist=tkinter.Text(self.root)
        self.flist.place(x=10,y=10,width=480,height=350)


        # 为文本框添加垂直滚动条
        self.vscroll = tkinter.Scrollbar(self.flist)
        self.vscroll.pack(side='right', fill='y')
        self.flist['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.flist.yview

    # 去的当前计算机盘符
    def GetDrives(self):
        drives = []                   #定义一个drives数组
        for i in range(65, 91):       #从65到90之间取数
            vol = chr(i) + ':/'       #循环A到Z之间的盘符
            if os.path.isdir(vol):      #判断电脑有什么盘符
                drives.append(vol)      #把盘符添加到空列表
        return tuple(drives)            #返回盘符列表

    #设置主窗体
    def MainLoop(self):
        self.root.title("Windows垃圾文件清理工具")
        self.root.minsize(500, 400)
        self.root.maxsize(500, 400)
        self.root.mainloop()

    # "关于"菜单
    def MenuAbout(self):           #定义

        tkinter.messagebox.showinfo("Window垃圾文件清理工具", "这是用Python编写的应用程序。\n欢迎使用，并提出宝贵意见!")

    # "退出"菜单
    def MenuExit(self):
        self.root.quit()

    #删除垃圾文件
    def MenuDelRubbish(self):
        result = tkinter.messagebox.askquestion("Windows垃圾文件清理工具", "删除垃圾文件需要较长时间，是否继续？")
        if result == 'yes':
               return tkinter.messagebox.askquestion("Windows垃圾文件清理工具", "马上开始删除垃圾垃圾文件！")
        self.drives = self.GetDrives()
        t = threading.Thread(target=self.DeleteRubbish, args=(self.drives,))
        t.start()


    #扫描大文件
    def MenuScanBigFile(self):
        result = tkinter.messagebox.askquestion("Windows垃圾文件清理工具", "扫描大文件将需要较长时间，是否继续")
        if result == 'yes':
            s = tkinter.simpledialog.askinteger("Windows垃圾文件清理工具", "请设置大文件的大小(M):")
            tkinter.messagebox.showinfo("Windows垃圾文件清理工具", "马上开始扫描大文件！")
            t = threading.Thread(target=self.ScanBigFile, args=(s,))
            t.start()
        pass

    #扫描垃圾文件
    def MenuScanRubbish(self):
        result = tkinter.messagebox.askquestion("Windows垃圾文件清理工具", "扫描垃圾文件需要较长时间，是否继续？")
        if result == 'yes':
            tkinter.messagebox.askquestion("Windows垃圾文件清理工具", "马上开始扫描垃圾垃圾文件！")
            self.drives = self.GetDrives()
            # self.ScanRubbish()   #单线程
            t = threading.Thread(target=self.ScanRubbish,args=(self.drives,))  # 创建线程   调用ScanRubbish函数
            t.start()

    #按名称扫描文件
    def MenuSearchFile(self):
        result = tkinter.messagebox.askquestion("Windows垃圾文件清理工具", "按名称扫描文件可能需要较长时间，是否继续？")
        if result == 'yes':
            s = tkinter.simpledialog.askstring("Windows垃圾文件清理工具", "请输入文件名称:")
            t = threading.Thread(target=self.SearchFile, args=(s,))
            t.start()
        pass


    def ScanRubbish(self,scanpath):
            global rubbishExt     #改变全局变量
            total = 0
            filesize = 0
            for drive in scanpath:   #变量访问scanpath路径
                for root,dirs,files in os.walk(drive):  #文件目录遍历，得到所有文件和文件夹
                    try:
                        for fil in files:    #便利文件列表
                            filesplit = os.path.splitext(fil)    #将路径拆分为文件名 + 扩展名
                            if filesplit[1] == '':#若无文件扩展名
                                continue
                            try:   #try except用来捕获中间代码的异常
                                if rubbishExt.index(filesplit[1]) >= 0:#扩展名在垃圾文件扩展名列表中
                                    fname = os.path.join(os.path.abspath(root),fil)  #拼接路径  
                                    filesize += os.path.getsize(fname)   #累加文件大小
                                    if total % 20 == 0:
                                        self.flist.delete(0.0,tkinter.END)   #删除列表里的文件
                                    self.flist.insert(tkinter.END,fname + '\n')  
                                    l = len(fname)
                                    if 1 > 60:
                                        self.progress['text'] = fname[:30] + '....' + fname[1-30:1] #文件切割，30为一段
                                    else:
                                        self.progress['text'] = fname
                                    total += 1               #状态栏显示
                            except ValueError:   #检测到异常值
                                pass
                    except Exception as e:     
                        print(e)              #发现异常e，并且把e输出
                        pass
            self.progress['text'] = "找到%s个垃圾文件，共占用%.2f M" % (total,filesize/1024/1024)


        #删除垃圾文件
    def DeleteRubbish(self,scanpath):
            global  rubbishExt
            total = 0
            filesize = 0
            for drive in scanpath:
                for root,dirs,files in os.path.splitext(drive):
                    try:
                        for fil in files:
                            filesplit = os.path.splitext(fil)
                            if filesplit[1] == '': #若无文件扩展名
                                continue
                            try:
                                if rubbishExt.index(filesplit[1]) >= 0:  #扩展名在垃圾文件扩展名列表中
                                    fname = os.path.join((os.path.abspath(root)),fil)   #将多个路径组合后返回
                                    filesize += os.path.getsize(fname)
                                    try:
                                        os.remove(fname)
                                        l = len(fname)
                                        if 1>50:
                                            fname = fname[:25]+'....'+fname[1-25:1]
                                            if total % 20 == 0:
                                                self.flist.delete(0,0,tkinter.END)
                                            self.flist.insert(tkinter.END,'删除文件',fname + '/n')    #显示文件名
                                            self.progress['text'] = fname
                                            total += 1
                                    except:
                                        pass
                            except ValueError:
                                pass
                    except Exception as e:
                        print(e)
                        pass

        #搜索大文件
    def ScanBigFile(self,filesize):
            total = 0
            filesize = filesize*1024*1024 #换算成字节单位
            for drive in self.GetDrives():
                for root,dirs,files in os.walk(drive):      #文件目录遍历
                    for fil in files:
                        try:
                            fname = os.path.join(os.path.abspath(root),fil)     #将多个路径组合后返回
                            fsize = os.path.getsize(fname)
                            self.progress['text'] = fname
                            if fsize >= filesize:
                                total += 1
                                self.flist.insert(tkinter.END,'%s,[%.2f]\n'%(fname,fsize/1024/1024))#显示的是文件名和它的大小，fsize/1024/1024是将字节单位转换成MB
                        except:
                            pass
        #按名称搜索文件
    def SearchFile(self,fname):
            total = 0
            fpath = ''
            #fname = fname.upper() #将小写字母转换为大写字母
            for drive in self.GetDrives():
                for root,dirs,files in os.walk(drive):      #文件目录遍历
                    for fil in files:
                        try:
                            fpath = os.path.join(os.path.abspath(root), fil)
                            self.progress['text'] = fpath
                            if fil == fname:
                                total += 1
                                #self.progress['text'] = fpath
                                self.flist.insert(tkinter.END,'已找到！'+fpath+'\n')
                        except:
                            pass
if __name__ == "__main__":
    window = Window()
    window.MainLoop()
