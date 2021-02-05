# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'k.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import face_recognition
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pymysql
import os
import pyttsx3
import pypinyin
import time
import csv

# 格式化成2016-03-20 11:45:39形式
# print (time.strftime("%Y-%m-%d%H:%M:%S", time.localtime()))


# conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='face', charset='utf8')
# cur = conn.cursor()


textIn = ""
nameX = ""

"""
这是数据库的，不过我的电脑配置承受相对不行
"""
# known_face_encodings = []
# known_face_names = []
# Inname = ['sddad', 'fasdfa']
#
# cur.execute('select * from users')
# for i in range(3):
#     values = cur.fetchone()
#     known_face_names.append(values[1])
#     known_face_encodings.append(np.frombuffer(values[2], dtype=np.float))
# print(known_face_names)
# print(known_face_encodings)
#
# cur.close()
# conn.close()

def write_csv(add, arr):
    with open(add, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(arr)
    f.close()

# 把中文转换成拼音，因为cv2的显示方式不支持中文
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


# 人脸编码
known_face_encodings = []
# 人脸名称（拼音）
known_face_names = []
# 对应拼音与中文，用于朗读
name_pinyin = {}
"""
    :param: 选择图片集地址
"""
path = r'image'
for photo in os.listdir(path):
    # print(os.path.join('name', photo))
    print(photo[0:-4])
    face_image = face_recognition.load_image_file(os.path.join(path, photo))
    known_face_encodings.append(face_recognition.face_encodings(face_image)[0])
    known_face_names.append(pinyin(photo[0:-4]))
    name_pinyin[pinyin(photo[0:-4])] = photo[0:-4]


unName = []

# 记录签到人员，按照要求应该可以写出，但我的代码会报错，显存不够
sign_name = ['签到']

# Initialize some variables
process_this_frame = True


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, camera):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(870, 567)
        # MainWindow.setStyleSheet("#MainWindow{border-color:red;}")
        # 首先设置无边框，其次设置背景透明
        # 背景透明后，可以在整体后方添加一个有色Label标签
        # 对该有色标签进行QSS圆角化！

        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # MainWindow.setWindowOpacity(0.9)  # 设置窗口透明度
        # MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # MainWindow.resize(711, 484)
        MainWindow.setStyleSheet("background-image: url(:/images/back1.png);\n""")
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TheTitle = QtWidgets.QLabel(self.centralwidget)
        self.TheTitle.setGeometry(QtCore.QRect(0, 0, 801, 51))
        self.TheTitle.setObjectName("TheTitle")
        self.VedioLabel = QtWidgets.QLabel(self.centralwidget)
        self.VedioLabel.setGeometry(QtCore.QRect(220, 60, 640, 480))
        self.VedioLabel.setMinimumSize(QtCore.QSize(640, 480))
        self.VedioLabel.setMaximumSize(QtCore.QSize(640, 480))
        self.VedioLabel.setObjectName("VedioLabel")

        self.VideoWindow(MainWindow, camera)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 332, 200, 206))
        self.label.setObjectName("label")
        self.TimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.TimeLabel.setGeometry(QtCore.QRect(10, -10, 205, 200))
        self.TimeLabel.setObjectName("TimeLabel")

        self.TimeWindow()

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 150, 200, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.InR)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 270, 200, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.getInf)
        # self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        # self.textEdit.setGeometry(QtCore.QRect(10, 270, 200, 250))
        # # self.textEdit.textChanged.connect(self.tc)
        # self.textEdit.setObjectName("textEdit")
        self.labelID = QtWidgets.QLabel(self.centralwidget)
        self.labelID.setGeometry(QtCore.QRect(10, 230, 60, 30))
        self.labelID.setText('Name:')
        self.labelID.setObjectName("labelID")
        self.labelIDF = QtWidgets.QLabel(self.centralwidget)
        self.labelIDF.setGeometry(QtCore.QRect(10, 310, 200, 20))
        self.labelIDF.setText('Check-in status:')
        self.labelIDF.setObjectName("labelID")
        self.IPHostnameEdit = QLineEdit(self.centralwidget)
        self.IPHostnameEdit.setGeometry(QtCore.QRect(60, 230, 150, 30))
        self.IPHostnameLayout = QHBoxLayout()

        # self.IPHostnameLayout.addWidget(self.IPHostnameEdit)
        # self.IPHostname = QLineEdit(self.centralwidget)
        # self.IPHostname.setGeometry(QtCore.QRect(10, 310, 200, 225))
        # self.IPHostnameLayout = QHBoxLayout()
        # self.IPHostnameLayout.addWidget(self.IPHostnameEdit)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 190, 200, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.OutR)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def tc(self, text):
        print(text)

    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.TheTitle.setText(self._translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; \
        font-weight:600;\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;上课\"快乐\"，下课\"快溜\"</span></p></body></html>"))
        self.label.setStyleSheet("background:white;border-width:1px;border-style: solid;border-color:black;\
        font-size:20px;")
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.pushButton.setText(self._translate("MainWindow", "签到"))
        self.pushButton_2.setText(self._translate("MainWindow", "新建"))
        self.pushButton_3.setText(self._translate("MainWindow", "退出"))

    def VideoWindow(self, MainWindow, camera):
        # print('1')
        self.camera = camera
        self.VW = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.VH = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # self.VedioLabel = QtWidgets.QLabel(self.centralwidget)
        # self.VedioLabel.setGeometry(QtCore.QRect(100, 50, self.VW, self.VH))
        # print(self.VW)
        # print(self.VH)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.play)
        # MainWindow.setStatusBar(self.VideoLanel)
        self._timer.start(100)

    def TimeWindow(self):
        self.Ttimer = QTimer()
        self.Ttimer.timeout.connect(self.showTime)
        self.Ttimer.start(1000)

    def showTime(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        # print(text)
        self.TimeLabel.setText(self._translate("MainWindow", "<html><head/><body><p><span style=\" font-size:23pt; \
        font-weight:1000;\">" + text[9:17] + "</span><br/><span font-size:15pt;  color:white;>&nbsp;"
                                               + text[0:2] + "&nbsp;&nbsp;" + text[3] + "/" + text[6:8] + "/" + text[
                                                                                                                18:22] + "</span></p></body></html>"))

    # @pyqtSlot()

    def getInf(self):
        global unName
        # conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='face', charset='utf8')
        # cur = conn.cursor()
        # cur.execute('insert users(ID,uname,ENCODING) values(%s,%s)', (1, 'sq', unName[0]))
        known_face_encodings.append(unName[0])
        name_pinyin[pinyin(self.IPHostnameEdit.text())] = self.IPHostnameEdit.text()
        known_face_names.append(pinyin(self.IPHostnameEdit.text()))

    def InR(self):
        # self.IPHostname.moveCursor(QTextCursor.End)
        global textIn
        # 念出姓名
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(name_pinyin[nameX])
        engine.runAndWait()
        engine.stop()

        if textIn == "":
            textIn += (name_pinyin[nameX] + " sign in!")
        else:
            textIn += ("\n" + name_pinyin[nameX] + " sign in!")
        print(textIn)
        sign_name.append(name_pinyin[nameX])
        self.label.setText(textIn)
        # print('x')

    def OutR(self):
        """
            :param: 可以选择退出并保存，但我的保存方式会爆显存，可能与我的电脑配置有关
        """
        # file_name = str(time.strftime("%Y-%m-%d%H:%M:%S", time.localtime())) + '.csv'
        # print(file_name)
        # write_csv(os.path.join('out', file_name), sign_name)
        Q = QApplication.instance()
        Q.quit()


    def play(self):
        global known_face_encodings
        global known_face_names
        global process_this_frame
        global unName
        global nameX
        face_locations = []
        face_encodings = []
        face_names = []

        ret, frame = self.camera.read()
        self.ret = ret
        self.frame = frame.copy()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                if name == 'Unknown':
                    unName = [face_encoding]
                nameX = name
                face_names.append(name)

        # process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 3
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if ret:
            # cv2.imshow('Video', frame)
            self.VedioLabel.setPixmap(QtGui.QPixmap.fromImage(
                QtGui.QImage(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), self.VW, self.VH, 13)))
