#!/usr/bin/python3
# @Time      : 2019/5/25 13:07
# @Author    : 老杨
# @FileName  : Order.py
# @Software  : PyCharm
# pip install PyAudio
import pyaudio
import time
import threading
import wave
import os
class Recorder():
    def __init__(self, chunk=1024, bits=pyaudio.paInt16, channels=1, rate=16000):
        """
        初始设置
        :param chunk: wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段
        :param format: 这个参数后面写的pyaudio.paInt16表示我们使用量化位数 16位来进行录音
        :param channels:代表的是声道，这里使用的单声道
        :param rate: 采样率16k
        :return: 生成的文件路径
        """
        self.CHUNK = chunk
        self.FORMAT = bits
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
        self._startTime = 0
        self._stopTime = 0
        self._duration = 0

    def start(self):
        """
        生成新的线程
        """
        threading._start_new_thread(self.__recording, ())

    def __recording(self):
        """
        开始录音
        """
        self._startTime = time.time()
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        """
        停止录音
        :return: 录音时长
        """
        self._stopTime = time.time()
        self._running = False
        self._duration = int(self._stopTime-self._startTime)
        return self._duration

    def save(self, dirName,fileName=''):
        """
        保存文件
        :param fileName: 需要保存的文件路径
        :return: 生成的文件路径
        """
        p = pyaudio.PyAudio()
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        if not fileName:
            fileName = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))+".wav"
            fileName = os.path.join(dirName, fileName)
        if not fileName.endswith(".wav"):
            filename = fileName + ".wav"
            fileName = os.path.join(dirName,fileName)
        wf = wave.open(fileName, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        return fileName

    def getDuration(self):
        """
        获取录音时长
        :return: 录音时长
        """
        return self._duration

