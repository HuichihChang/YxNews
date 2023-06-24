# 鄞响新媒体刷量工具
import requests
import csv
from tkinter import messagebox
from bs4 import BeautifulSoup
from threading import Thread

def mainProc(_count, _url):
    '''
    主程序入口，为各线程分配点击次数，同时使按钮不可用
    '''
    clickCounts = clickCalculator(_count)
    #threadWorker(clickCounts, _url)
    autoReflash(clickCounts, _url)
    finalInfo()


def autoReflash(_count, _url):
    '''
    自动刷新功能，中途可调用阅读量截取函数进行统计
    '''
    # clickCounts = clickCalculator(_count)
    i = 1
    while (i <= _count):
        res = requests.get(_url)
        # detectCounts(i, res)
        i += 1


def finalInfo():
    '''
    程序运行结束时，弹出弹窗提醒
    '''
    messagebox.showinfo(message="助力完成")


def threadWorker(_count, _url):
    '''
    线程工作分配函数，为四个线程分配点击次数（不要用，会因为访问速度过快被拉黑）
    '''
    threadList = []

    t1 = Thread(target=autoReflash, args=(_count/4, _url))
    t1.start()
    t2 = Thread(target=autoReflash, args=(_count/4, _url))
    t2.start()
    t3 = Thread(target=autoReflash, args=(_count/4, _url))
    t3.start()
    t4 = Thread(target=autoReflash, args=(_count/4, _url))
    t4.start()

    threadList.append(t1)
    threadList.append(t2)
    threadList.append(t3)
    threadList.append(t4)

    for t in threadList:
        t.join()


def detectCounts(_res):
    '''
    阅读量截取函数
    '''
    html = _res.text
    soup = BeautifulSoup(html, 'html.parser')
    readText = (soup.find('span', class_='readNumber')).getText()
    readCount = readText.replace("阅读", '')

    return readCount


def recordCounts(_i, _res):
    '''
    阅读量记录函数，会在当前目录下生成实际点击次数与阅读量的表格，用来在开发中作为拟合公式的参照
    '''
    readCount = detectCounts(_res)
    with open("点击结果记录.csv", "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # 逐行写入数据，左侧为点击次数，右侧为阅读量
        writer.writerow([_i, readCount])


def printCounts(_i, _res):
    '''阅读量输出函数'''
    readCount = detectCounts(_res)
    print(str(_i)+"  "+readCount)


def clickCalculator(_targetCount):
    '''
    点击量与阅读量间不是一对一的关系，所以我用测试数据拟合了一个多项式函数用来计算为达到目标点击量，实际需要的访问次数。
    在拟合中我尝试过1-10次的多项式次数进行线性拟合，呈现的结果没有显著差异。因此这里就用了1次方程计算点击次数
    此外，据观察阅读量与点击存在反复横跳的情况，常见5-10的跳跃，也存在2-3次原地不动的情况
    可能是服务器端使用了随机数或其他方式协同点击量计算阅读量，所以对50次以下的阅读量需求，直接返回实际次数，不使用公式计算
    '''
    if (_targetCount <= 50):
        return _targetCount
    else:
        clickCounts = int((_targetCount-14.59)/4.497)
        print("需要访问"+str(clickCounts)+"次")
        return clickCounts
