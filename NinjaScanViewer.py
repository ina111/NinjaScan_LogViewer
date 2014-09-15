#!/usr/bin/python
# -*- coding: utf-8 -*-
#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import font_manager
#import matplotlib.text as text
#from matplotlib.backends.backend_pdf import PdfPages
import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *
import NinjaScanLogViewer as nslv
 
class Form(QDialog):
   
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("NinjaScan Log Viewer")
        self.setFixedSize(350, 300)
        # ウィジェットを作成
        self.edit_dir = QLabel("Log Dir Path")
        self.edit_path = QLabel("File Path")
        self.button_path = QPushButton("Select LOG File (csv)")
        self.button_path.setStyleSheet("font: 12pt")
        self.button_path.setIcon(self.style().standardIcon(QStyle.SP_FileDialogStart))
        self.label_start = QLabel("Start gps time [msec]:")
        self.edit_start = QSpinBox()
        self.edit_start.setMaximum(1000000000)
        self.label_startmin = QLabel("Unknown")
        self.label_end = QLabel("End gps time [msec]:")
        self.edit_end = QSpinBox()
        self.edit_end.setMaximum(1000000000)
        self.label_endmax = QLabel("Unknown")
        self.label_launch = QLabel("Launch gps time [msec]:")
        self.edit_launch = QSpinBox()
        self.edit_launch.setMaximum(1000000000)
        self.label_launchrange = QLabel("Unknown")
        self.label_press = QLabel("zero alt. pressure [hPa]:")
        self.edit_press = QDoubleSpinBox()
        self.edit_press.setMaximum(1100)
        self.edit_press.setValue(1013.0)
        self.button_check = QPushButton("Date Check")
        self.button_check.setEnabled(False)
        self.button_check.setStyleSheet("font: 12pt")    
        self.button_check.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.button_plot = QPushButton("Plot")
        self.button_plot.setEnabled(False)
        self.button_plot.setStyleSheet("font: 12pt")
        self.button_plot.setIcon(self.style().standardIcon(QStyle.SP_DialogYesButton))
        
        # レイアウトを作成しウィジェットを追加します
        toplayout = QVBoxLayout()
        
        sublayout1 = QGridLayout()
        sublayout1.addWidget(self.edit_dir, 1, 0)
        sublayout1.addWidget(self.edit_path, 2, 0)
        sublayout1.addWidget(self.button_path, 0, 0)
        
        sublayout3 = QGridLayout()
        sublayout3.addWidget(self.label_start, 0, 0, Qt.AlignRight)
        sublayout3.addWidget(self.edit_start, 0, 1)
        sublayout3.addWidget(self.label_startmin, 0, 3, Qt.AlignLeft)
        sublayout3.addWidget(self.label_end, 1, 0, Qt.AlignRight)
        sublayout3.addWidget(self.edit_end, 1, 1)
        sublayout3.addWidget(self.label_endmax, 1, 3, Qt.AlignLeft)
        sublayout3.addWidget(self.label_launch, 2, 0, Qt.AlignRight)
        sublayout3.addWidget(self.edit_launch, 2, 1)
        sublayout3.addWidget(self.label_launchrange, 2, 3, Qt.AlignLeft)
        sublayout3.addWidget(self.label_press, 3, 0, Qt.AlignRight)
        sublayout3.addWidget(self.edit_press, 3, 1)
        
        toplayout.addLayout(sublayout1)
        toplayout.addSpacing(10)
        toplayout.addWidget(self.button_check)
        toplayout.addSpacing(10)
        toplayout.addLayout(sublayout3)
        toplayout.addWidget(self.button_plot)

        # ダイアログのレイアウトを設定します
        self.setLayout(toplayout)
        # ボタンのシグナルを関数と接続します
        self.button_path.clicked.connect(self.open_path)
        self.button_check.clicked.connect(self.check)
        self.button_plot.clicked.connect(self.plot)
        
    def open_path(self):
        (path_file, type) = QFileDialog.getOpenFileName(self, "Open File",filter="NinjaScan Log data(*.csv)")
        if len(path_file) == 0:
            self.edit_path.setText("<font color=red>Select File<\font>")
        else:
            path_dir = os.path.dirname(path_file)
            self.edit_dir.setText(path_dir)
            path_log = os.path.basename(path_file)
            path_log = path_log[:-6]
            self.edit_path.setText(path_log)
            self.button_check.setEnabled(True)
            
    def check(self):
        # ファイルが良いかどうか確認。一回確認したらそのままplotボタンを有効化
        # 確認したら、最大値などを設定するように仕向ける
        self.path = self.edit_dir.text() + "\\" + self.edit_path.text()
        print self.path
        try:
            widget = WaitDialog()
            self.button_check.setEnabled(False)
            self.viewer = nslv.NinjaScanLogViewer(self.path, 338460000, 338600000, 338476000)

            [self.time_min, self.time_max] = self.viewer.check_time()
            self.label_startmin.setText("%d ~" % (self.time_min))
            self.label_endmax.setText("~ %d" % (self.time_max))
            self.label_launchrange.setText("%d ~ %d" % (self.time_min, self.time_max))
            self.edit_start.setRange(self.time_min, self.time_max-500)
            self.edit_end.setRange(self.time_min+500, self.time_max)
            self.edit_launch.setRange(self.time_min+500, self.time_max-500)
            self.button_check.setEnabled(True)
            self.button_plot.setEnabled(True)
        except:
            msgBox = QMessageBox()
            msgBox.setText("This file is NOT correct!")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.exec_()
            print "Error!"
            self.button_check.setEnabled(True)
            return
        finally:
            widget.close()
            
        
    def plot(self):
        self.viewer.filename = self.path
        self.viewer.time_start = self.edit_start.value()
        self.viewer.time_end = self.edit_end.value()
        self.viewer.time_launch = self.edit_launch.value()
        self.viewer.press0 = self.edit_press.value()
        self.viewer.plot()

class WaitDialog(QDialog):
# 読み込み中は時間がかかるので、ダイアログを出してごまかす
    def __init__(self, parent=None):
        super(WaitDialog, self).__init__(parent)

        label1 = QLabel("Please wait...")

        layout = QVBoxLayout()
        layout.addWidget(label1)
        self.setLayout(layout)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Work in progress")
        self.resize(200, 100)
        self.setModal(True)
        self.show()
        self.raise_()
        QApplication.processEvents()
 
 
if __name__ == '__main__':
    # Qt Applicationを作ります
    app = QApplication(sys.argv)
    # formを作成して表示します
    form = Form()
    form.show()
    # Qtのメインループを開始します
    sys.exit(app.exec_())