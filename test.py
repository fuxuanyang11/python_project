import os
import re
import shutil

# password = "4399ztxjyd" #泽天仙决
password = "123456" #本地
# password = "dgame@2018" #末日求生
# password = "6316877" #皮卡丘
file_path = "E:\\python_test\\"
file_paths = "E:\\python_test\\apk.out\\"
keyAlias = "123456"#本地
# keyAlias = "ztxjyd"#泽天仙决
# keyAlias = "yl_mrqs"#末日求生
# keyAlias = "android.keystore"#皮卡丘
meteDataKey = "YD_Channel"
# meteDataKey = "YD_RY_KEY"
# keyStore = "201911040946271711.keystore"#泽天仙决
keyStore = "key123456.keystore"#本地
# keyStore = "android.keystore"#皮卡丘
# keyStore = "yl_mrqs.jks"#末日求生
# apkName = "source.apk" #泽天仙决
# apkName = "yl_mrqs.apk"#末日求生
apkName = "stxzyl.apk"

def run():
    os.chdir(r'E:\python_test')  # 进入指定的目录
    # os.system("apktool.bat d --only - main - classes " + apkName)
    os.system("apktool.bat d -o apk.out " + apkName)

# 查找所有mete-data下key为data_Name的value值
def openFile():
    manifest_path = os.path.join("E:\\python_test\\apk.out", 'AndroidManifest.xml')
    if manifest_path == None:
        raise IOError
    with open(manifest_path, 'r+') as f:
        m_result = f.read()
        # re正则匹配的渠道key，不同apk可能不一样,这里是InstallChannel，有的是umeng_channel
        pattern = re.compile(r'<meta-data android:name="%s" android:value="(\w+)"' % meteDataKey)
        value = pattern.findall(m_result)[0]
        return value


def replace(file_path, old_str, new_str):
    f = open(file_path,'r+')
    all_lines = f.readlines()
    f.seek(0)
    f.truncate()
    for line in all_lines:
      line = line.replace(old_str, new_str)
      f.write(line)
    f.close()


def move_file(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))


def sign(channel):
    os.chdir(r'E:\python_test')  # 进入指定的目录
    unSignApk = "unsign_" + channel + ".apk"
    signApk = "sign_" + channel + ".apk"
    os.system("apktool.bat b -o "+unSignApk+" apk.out")

    cmd = 'jarsigner -verbose -keystore '+keyStore + ' -signedjar '+signApk+ ' ' + unSignApk + ' '+  keyAlias + ' -storepass ' + password
    os.system(cmd)
    os.remove(unSignApk)
    move_file(signApk, file_path + "apk\\" + signApk)




def getNewChannel():
    run()
    f = open(file_path + "channel.txt", 'r')
    all_lines = f.readlines()
    for line in all_lines:
        line = line.strip()
        value = openFile()
        replace(file_paths + "AndroidManifest.xml", value, line)
        sign(line)
    f.close()



def getOneChannel():
    run()
    sign("test")

# run()
# sign("test")
getNewChannel()
# getOneChannel()