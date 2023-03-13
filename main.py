# -*- encoding: utf-8 -*-
'''
    @Time    :   2023/03/13 22:30:54
    @Author  :   Tomas
    @Version :   1.0
    @Contact :   tomaswu@qq.com
    Desc     :    
'''


from PySide6 import QtCore,QtWidgets,QtGui
import dump
import os
import ui_mainform
import time

class cvtThread(QtCore.QThread):
    def __init__(self,flist,output_dir,sig):
        super().__init__()
        self.file_list=flist
        self.output_dir=output_dir
        self.sig=sig
        self.flag=True

    def run(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        n=len(self.file_list)
        for idx,i in enumerate(self.file_list):
            if not self.flag:
                return
            dump.dump(i,self.output_dir)
            p = round((idx+1)/n*100)
            self.sig.emit(p)
    
    def stop(self):
        self.flag=False


class mainWindow(QtWidgets.QMainWindow,ui_mainform.Ui_MainWindow):
    evaluate = QtCore.Signal(int)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.file_list = []
        self.output_dir = './meta'
        self.thread=None
        
        self.progressBar.setValue(0)

        self.actionset_output_path.triggered.connect(self.set_output_dir)
        self.pushButton.clicked.connect(self.startConvert)
        self.evaluate.connect(self.updateStatus)

    def dragEnterEvent(self,event:QtGui.QDragEnterEvent):
        event.accept()

    def dropEvent(self,event:QtGui.QDropEvent):
        urls = event.mimeData().urls()
        for i in urls:
            path = i.path()
            if os.path.isfile(path):
                if path.endswith('.ncm') and path not in self.file_list:
                    self.file_list.append(path)
            else:
                for rootdir,dirs,files in os.walk(path,False):
                    for j in files:
                        if j.endswith('.ncm'):
                            self.file_list.append(os.path.abspath(os.path.join(rootdir,j)))
        self.refreshList()
    

    def refreshList(self):
        names = [os.path.basename(i) for i in self.file_list]
        self.listView.setModel(QtCore.QStringListModel(names))

    
    def set_output_dir(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(caption='设置输出目录',dir='./')
        if os.path.exists(path):
            self.output_dir=path

    def startConvert(self):
        if self.thread is None:
            self.thread = cvtThread(self.file_list,self.output_dir,self.evaluate)
            self.thread.start()
            self.pushButton.setText('停止')
        else:
            self.thread.stop()
            self.thread=None
            self.pushButton.setText('转换')
    
    def updateStatus(self,n):
        self.progressBar.setValue(n)
        if n==100:
            self.thread.quit()
            self.thread=None
            self.pushButton.setText('转换')

            


if __name__=='__main__':
    app=QtWidgets.QApplication()
    mw = mainWindow()
    mw.show()
    app.exec()

