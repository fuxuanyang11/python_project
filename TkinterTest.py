import os
import shutil
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pickle


file_path = "E:\\python_test\\"
file_paths = "E:\\python_test\\apk.out\\"
meteDataKey = "YD_Channel"
keyStore = "201911040946271711.keystore"


# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('Wellcome to Hongwei Website')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('400x300')  # 这里的乘是小x


# 第5步，用户信息
tk.Label(window, text='keyAlias:', font=('Arial', 14)).place(x=10, y=170)
tk.Label(window, text='Password:', font=('Arial', 14)).place(x=10, y=210)

# 用户名
key_alias = tk.StringVar()
entry_usr_name = tk.Entry(window, textvariable=key_alias, font=('Arial', 14))
entry_usr_name.place(x=120, y=175)
# 用户密码
key_password = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=key_password, font=('Arial', 14), show='*')
entry_usr_pwd.place(x=120, y=215)




def run():
    os.chdir(r'E:\python_test')  # 进入指定的目录
    os.system("apktool.bat d -o apk.out source.apk")

# 查找所有mete-data下key为data_Name的value值
def openFile():
    manifest_path = os.path.join("E:\\python_test\\apk.out", 'AndroidManifest.xml')
    if manifest_path == None:
        raise IOError
    with open(manifest_path, 'r') as f:
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


def sign(channel, keyAlias, password):

    os.chdir(r'E:\python_test')  # 进入指定的目录
    unSignApk = "unsign_" + channel + ".apk"
    signApk = "sign_" + channel + ".apk"
    os.system("apktool.bat b -o "+unSignApk+" apk.out")
    cmd = 'jarsigner -verbose -keystore '+keyStore + ' -signedjar '+signApk+ ' ' + unSignApk + ' '+  keyAlias + ' -storepass ' + password
    os.system(cmd)
    os.remove(unSignApk)
    move_file(signApk, file_path + "apk\\" + signApk)




def getNewChannel():
    keyAlias = key_alias.get()
    password = key_password.get()
    if keyAlias == "":
        tkinter.messagebox.showerror(message='输入别名')
        return

    if password == "":
        tkinter.messagebox.showerror(message='输入密码')
        return

    run()
    f = open(file_path + "channel.txt", 'r')
    all_lines = f.readlines()
    for line in all_lines:
        line = line.strip()
        value = openFile()
        replace(file_paths + "AndroidManifest.xml", value, line)
        sign(line, keyAlias, password)
    f.close()

def getOneChannel():
    run()
    sign("test")



# 第7步，login and sign up 按钮
btn_login = tk.Button(window, text='Login', command=getNewChannel)
btn_login.place(x=120, y=240)


# 第10步，主窗口循环显示
window.mainloop()