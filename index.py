# pip install baidu-aip
# pip install pyttsx3
# pip install requests
# http://ai.baidu.com/docs#/ASR-Online-Python-SDK/top
from tkinter import *
from aip import AipSpeech
import Recorder
import Control
import pyttsx3
import requests
import json
from tkinter import messagebox
# pip install jsonpath
# import jsonpath

def action():
    data = entry1.get().strip()
    control = Control.Order()
    control.run(data)

rec = Recorder.Recorder()
def ok(event):
    print('开始录音')
    rec.start()
def no():
    print('结束录音')
    # 结束录音
    rec.stop()
    # 保存音频
    file = rec.save('audio')
    # 调用百度aip语音识别转义成文字
    APP_ID = 'your APP_ID'
    API_KEY = 'your API_KEY'
    SECRET_KEY = 'your SECRET_KEY'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    with open(file,'rb') as fp:
            data = fp.read()
    result = client.asr(data,'wav',16000,{
        'dev_pid':1537
    })
    print(result)
    try:
        data = result['result'][0]
    except Exception as err:
        exit(err)
    return data

def voiceControl(event):
    result = no()
    print(result)
    messagebox.showinfo('提示',result)
    # 提取前三位，判断是操控还是聊天
    data = result[0:2]
    order = result[2:-1:]
    print(order)
    if data =='操作':
        control = Control.Order()
        control.run(order)
    else:
        print(1)
        show(result)

def show(content):
    # 构造请求参数
    request_data = {
        "key":"your key",
        "info":content,
        "userid":"老杨真帅"
    }
    # 构造请求url
    url = "http://www.tuling123.com/openapi/api"
    # 发送请求
    result = requests.post(url,request_data)
    # 转换格式
    response = json.loads(result.text)
    print(response['text'])
    # 语音输出
    engine = pyttsx3.init()
    engine.say(response['text'])
    engine.runAndWait()
# exit()
# 实例化 创建一个GUI对象
master = Tk()
# 设置标题
master.title('贾维斯')
# 设置窗体大小以及出现在屏幕上面的位置
# 宽x高+X轴+Y轴
# 此处有坑，不是*，而是x
master.geometry('300x100+450+300')
master.resizable(False,False)
# 设置标签
# # 网格布局
Label(master,text='输入指令:',font=('黑体',18),fg='blue').grid()
# Label(master,text.txt='结果:',font=('黑体',18),fg='blue').grid(row=1,column=0)
# 设置第一个输入框
entry1 = Entry(master)
# 网格布局
entry1.grid(row=0,column=1)
button1 = Button(master,text='运行',width=10,command=action)
button1.grid(row=1,column=0)
button = Button(master,text='声控',width=10)
button.grid(row=1,column=1)
button.bind("<Button-1>",ok)
button.bind("<ButtonRelease-1>",voiceControl)
# 消息循环
master.mainloop()
