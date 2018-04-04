
from socketClient import SocketHandler
import time

from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication)
from PyQt5 import QtGui
import sys

import os
ip = os.environ['HANDLER_IP']
zip_path=str()
program = os.environ.get('ProgramFiles')
programx86 = os.environ.get('ProgramFiles(x86)')
if os.path.exists(os.path.join(program, '7-Zip')):
    zip_path = os.path.join(program, '7-Zip','7z')
elif os.path.exists(os.path.join(programx86, '7-Zip')):
    zip_path = os.path.join(programx86, '7-Zip','7z')
else:
    print('Install 7-Zip')
zip_path = r'"{}"'.format(zip_path)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.showDialog()

    def showDialog(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        dlg.exec_()
        fname = dlg.selectedFiles()
        if len(fname)==0:print('Upload Canceled') & exit(0)
        for i in fname:
            if i != '':
                self.send_file(i)
        sys.exit(0)

    @staticmethod
    def send_file(file_path):
        path_0 = file_path

        for i in list(os.walk(path_0))[0][1]:
            path = path_0 + '\{}'.format(i)
            string = r'{} a -r {}.zip {}/*'.format(zip_path, path, path)
            print(string)
            os.system(string)

        string = r'{} a -r {}.zip {}'.format(zip_path, path_0, os.path.join(path_0, '*.zip'))
        print(string)
        os.system(string)

        os.system('del {}\*.zip'.format(path_0))

        file_path = path_0 + ".zip"

        print(file_path)

        ip = r"192.168.0.158"
        ws = SocketHandler("ws://{}:1111/upload".format(ip))

        file_time = time.time()
        f = open(file_path, 'rb+')
        string = f.read()
        f.close()
        file_name = file_path.split('\\')[-1]
        size = len(string)
        pack_size = int(2 ** 14)
        packs = int(size / pack_size) + 1

        ws.send(None, {'init_file': [{'file_name': file_name, 'file': [i for i in string]}]})
        print('Upload successful')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())




