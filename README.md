# 人脸识别 + 语音点名

## 库依赖

```
face_recognition==1.3.0
pypinyin==0.40.0
numpy==1.16.2
opencv_python==4.1.2.30
PyMySQL==0.9.3
pyttsx3==2.90
PyQt5==5.15.2
```

全部包含在 **requestments.txt** 中，目录下运行以下代码即可批量安装

```shell
pip install -r requirements.txt
```

## 使用流程

1. 运行**main.py**

   ```shell
   python main.py
   ```

2. 没有录入的人可以选择新建，已经录入的人点击签到可以播报姓名

## 提醒

将要识别的人脸图片放入**image**文件夹中，尽量五官清晰且无P图，有可能训练时会报错，删掉报错图片即可。

**k.py**是pyqt5的界面设置，主要的处理逻辑也在里面，因为当时写的比较着急，写得不是很美观。

文件夹下有**Demo新建，Demo识别**。

