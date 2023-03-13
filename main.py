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


class mainWindow(QtWidgets.QMainWindow,ui_mainform.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.file_list = []


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



if __name__=='__main__':
    app=QtWidgets.QApplication()
    mw = mainWindow()
    mw.show()
    app.exec()

