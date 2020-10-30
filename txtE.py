#-*- coding:utf-8 -*-
import re
import chardet
import os
import sys
import time
import shutil 
 
# 获取文件编码类型
def getEncoding(filePath):
    # 二进制方式读取，获取字节数据，检测类型
    try:
        with open(filePath, 'rb') as f:
            return chardet.detect(f.read())['encoding']
    except IsADirectoryError as e:
        return "directory"

def dirGetFileList(dirPath):
    '''
    for i,j,k in os.walk(dirPath):
        print(i)
        print(j)
        print(k)
    '''
    return os.listdir(dirPath)

def addNovChap(inPathName,outPath):
    if sys.platform == "win32":
        if outPath[-1] != '\\':
            outPath = outPath + "\\"
        outPathName = outPath + inPathName.split("\\")[-1]
    else:
        if outPath[-1] != '/':
            outPath = outPath + "/"
        outPathName = outPath + inPathName.split("/")[-1]
    file = open(inPathName, 'rt', encoding=getEncoding(inPathName)) # 读取文件
    while True:
        line = file.readline()
        #print("line: ", line)
        x = re.findall(r"^\d+\.?", line) # 使用findall()获取所有匹配
        x = re.findall(r"^\d{3,4}$", line) # 使用findall()获取所有匹配
        x = re.findall(r"^\d+", line) # 使用findall()获取所有匹配
        #print("x: ",x)
        # 判断是否为目录
        if x != []:
            y = re.findall(r'\d+', str(x))
            print("y: ",y)
            line1 = re.sub(''.join(x), '第'+ ''.join(y) +'章 ', line) # 使用sub()替换匹配
            line = line1 # 替换目录
            #print(line1)
        
        # 写入文件
        tempfileName = "." + str(random.randint(100,999)) + inPathName.split("/")[-1]
        with open(tempfileName, 'a', encoding='utf-8') as f:
            f.write(line)
        if not line:
            break
        shutil.move(tempfileName,outPathName)
    '''
    要点：
    ^表示只匹配开头

    \d+表示匹配1次或者多次数字

    \.?表示是匹配小数点
    '''

def updateInfo(inPathName,outPath,oldInfos,newInfos):
    '''
    此函数用于批量替换txt文件中需要替换的信息
    inPathName:原文件带路径的文件名
    outPath：替换后新文件的目录路径
    oldInfos：原文件需要被替换的关键字列表
    newInfos：需要替换的新关键字列表
    '''
    if sys.platform == "win32":
        if outPath[-1] != '\\':
            outPath = outPath + "\\"
        outPathName = outPath + inPathName.split("\\")[-1]
    else:
        if outPath[-1] != '/':
            outPath = outPath + "/"
        outPathName = outPath + inPathName.split("/")[-1]
    file = open(inPathName, 'rt', encoding=getEncoding(inPathName)) # 读取文件
    tempfileName = "." + str(time.time()) + inPathName.split("/")[-1]
    while True:
        line = file.readline()
        for i in range(0,len(oldInfos)):
            x = re.findall(oldInfos[i], line) # 使用findall()获取所有匹配
            # 判断是否有关键字
            if x != []:  # 判断是否有关键字
                line1 = re.sub(oldInfos[i], newInfos[i], line) # 使用sub()替换匹配
                line = line1 # 替换
        # 写入文件

        with open(tempfileName, 'a', encoding='utf-8') as f:
            f.write(line)
        if not line:
            break
    shutil.move(tempfileName,outPathName)
    try:
        os.remove(tempfileName)
    except Exception as e:
        pass


out = dirGetFileList("/Users/liudyixia/Documents/code/skBatEditor")
print(out)
for i in out:
    print(getEncoding(i))

#updateInfo("test.txt","./",["验证","数字","字母"],["[验证]","[数字]","[字母]"])
updateInfo("test.txt","./",["验证"*3,"数字"*3,"字母"*3],["验证","数字","字母"])