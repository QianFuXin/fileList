# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app
   Description : 用flask实现类似nginx静态文件列表
   Author :       FXQ
   date：          2023/2/16
-------------------------------------------------
   Change Activity:
                   2023/2/16 8:44:
-------------------------------------------------
"""
import os.path
import time
from flask import Flask, abort, send_file, render_template, redirect, url_for, request

app = Flask(__name__)

# 将字节转换成适当的单位
def bytes_to_human(byteNumber):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if byteNumber >= prefix[s]:
            value = float(byteNumber) / prefix[s]
            return '%.1f%s' % (value, s)
    return '%sB' % byteNumber

# 将时间戳转换成特定的格式
def timeStamp_to_human(timeStamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))

# 根目录
@app.route("/")
def index():
    return redirect(url_for("filePath", filePath="file"))

# 路径处理的路由
@app.route("/<path:filePath>")
def filePath(filePath):
    # 首先判断路径是否存在
    if not os.path.exists(filePath):
        abort(404)
    # 然后判断是文件还是目录
    if os.path.isfile(filePath):
        return send_file(filePath)
    # 存放列表详细的html
    trs = ""
    # 返回当前文件夹的详情
    for i in os.listdir(filePath):
        # 文件名
        fileName = i
        # 当前文件夹或文件的路径
        thisPath = os.path.join(filePath, i)
        # 是否是文件
        fileType = "文件" if os.path.isfile(filePath) else "文件夹"
        # 文件大小
        fileSize = bytes_to_human(os.path.getsize(filePath))
        # 最后访问时间
        fileAtime = timeStamp_to_human(os.path.getatime(filePath))
        # 最后修改时间
        fileMtime = timeStamp_to_human(os.path.getmtime(filePath))
        # 创建时间
        fileCtime = timeStamp_to_human(os.path.getctime(filePath))
        # 列表展示模版
        tr = f"""
                    <tr>
                    <td><a href="{"/" + thisPath}">{fileName}</a></td>
                    <td>{fileType}</td>
                    <td>{fileSize}</td>
                    <td>{fileCtime}</td>
                    <td>{fileMtime}</td>
                    <td>{fileAtime}</td>
                </tr>
                    """
        trs += tr
    # 上一层文件夹的地址
    lastDir = "/" + os.path.dirname(filePath)
    return render_template("fileList.html", trs=trs, lastDir=lastDir)

# 处理路径错误
@app.errorhandler(404)
def error404(error):
    return "路径错误", 404
