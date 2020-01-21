# coding:utf-8
import os
# import pickle
# import sys
import re
import shutil

string_path = "E:\python_test\\apk.out\\res\\values\\strings.xml"
app_name = "哈哈哈"
local_path = "D:\\qq文件\\icon"
replace_path = "E:\\python_test\\apk.out\\res"
icon = "app_icon.png"
icon_file = "mipmap"
replace_app_name = "去吧皮卡丘"
local_app_name = "精灵训练师"


password = "6316877" #皮卡丘
file_path = "E:\\python_test\\"
file_paths = "E:\\python_test\\apk.out\\"
keyAlias = "android.keystore"#皮卡丘
keyStore = "android.keystore"#皮卡丘
apkName = "pkq.apk" #皮卡丘


def replace(file_path, old_str, new_str):
    f = open(file_path,'r+', encoding='utf8')
    all_lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in all_lines:
      line = line.replace(old_str, new_str)
      f.write(line)
    f.close()



def copyFiles(old_path, new_path):
    shutil.copyfile(old_path, new_path)

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for dir in dirs:
            if icon_file in dir:
                for roots, dirss, filess in os.walk(file_dir + "\\" +dir):
                    for file in filess:
                        if icon in file:
                            copyFiles(local_path + "\\" + dir + "\\" + icon, replace_path + "\\" + dir + "\\" + icon)
                            print(dir)

def run():
    os.chdir(r'E:\python_test')  # 进入指定的目录
    os.system("apktool.bat d -o apk.out " + apkName)

def sign(channel):
    os.chdir(r'E:\python_test')  # 进入指定的目录
    unSignApk = "unsign_" + channel + ".apk"
    signApk = "sign_" + channel + ".apk"
    os.system("apktool.bat b -o "+unSignApk+" apk.out")
    cmd = 'jarsigner -verbose -keystore '+keyStore + ' -signedjar '+signApk+ ' ' + unSignApk + ' '+  keyAlias + ' -storepass ' + password
    os.system(cmd)
    os.remove(unSignApk)
    move_file(signApk, file_path + "apk\\" + signApk)

def move_file(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))


def getNewPkg():
    run()
    # replace(string_path, replace_app_name, local_app_name)
    file_name(replace_path)
    sign("pkq")


getNewPkg()
# run()
# file_name("E:\\python_test\\apk.out\\res")
