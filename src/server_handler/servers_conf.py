
handler = {'ip': '138.4.94.29:1111'}

model3D = {'ip': '138.4.94.29:1112'}

CFD = {'ip':  '138.4.94.29:1113'}

design = {'ip': '138.4.94.29:1114'}

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        label_Handler = QLabel()
        label_Handler.setText("Handler")
        input_Handler = QLineEdit()

        grid.addWidget(label_Handler, 0,0)
        grid.addWidget(input_Handler, 0, 1)

        label_Design = QLabel()
        label_Design.setText("Design")
        input_Design = QLineEdit()

        grid.addWidget(label_Design, 1, 0)
        grid.addWidget(input_Design, 1, 1)

        label_Simulation = QLabel()
        label_Simulation.setText("Simulation")
        input_Simulation = QLineEdit()

        grid.addWidget(label_Simulation, 2, 0)
        grid.addWidget(input_Simulation, 2, 1)

        label_model3D = QLabel()
        label_model3D.setText("model3D")
        input_model3D = QLineEdit()

        grid.addWidget(label_model3D, 3, 0)
        grid.addWidget(input_model3D, 3, 1)

        btn = QPushButton('Button', self)
        btn.resize(btn.sizeHint())

        grid.addWidget(btn, 4,0)

        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())