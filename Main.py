import sys
from typing import Optional
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel
import PyQt6.QtWidgets as QtWidgets
from matplotlib.backend_bases import FigureCanvasBase
from KnapsackUI import Ui_MainWindow
from Algorithm import *
import asyncio
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool, QCoreApplication
import qtinter
import asyncio
import random
import numpy as np
import pyqtgraph as pg
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class AlertDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setFixedWidth(350)
        self.setFixedHeight(100)
        self.setModal(True)
        self.layout = QVBoxLayout()
        if message == None:
            self.message = QLabel("Error")
        else:
            self.message = QLabel(message)
        self.layout.addWidget(self.message)
        self.setLayout(self.layout)

class Core(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isRunning = False
        self.KnapsackUI = Ui_MainWindow()
        self.KnapsackUI.setupUi(self)
        self.KnapsackUI.btStart.clicked.connect(self.start)
        self.KnapsackUI.btStop.clicked.connect(self.stop)
        self.task = None
        self.G = None
    
    def start(self):
        if self.isRunning == False:
            if ((int(self.KnapsackUI.num_items.value()) != 0) and (int(self.KnapsackUI.max_value.value()) != 0) and (int(self.KnapsackUI.max_weight.value()) != 0)):
                self.isRunning = True
                self.KnapsackUI.canvaFrame.setVisible(True)
                print("Start")
                if (int(self.KnapsackUI.capacity.value()) == 0):
                    Solution = [0 for i in range(int(self.KnapsackUI.num_items.value()))]
                    text = "Giải pháp tốt nhất = " + str(Solution) + "\n"
                    text += "Value của giải pháp tốt nhất: 0"
                    self.KnapsackUI.tbResult.setText(text)
                    # print("Giải pháp tốt nhất: ",Solution)
                    # print("Value của giải pháp tốt nhất: ", 0)
                else:
                    Hill = HillClimbing(int(self.KnapsackUI.num_items.value()), int(self.KnapsackUI.capacity.value()), int(self.KnapsackUI.max_value.value()), int(self.KnapsackUI.max_weight.value()))
                    result, current_solution, values, iterPro = Hill.solve()
                    self.KnapsackUI.tbResult.setText(result)
                    self.KnapsackUI.canvaFrame.canvas.axes.clear()
                    plt.xticks(np.arange(0, 100 + 10, 10), fontsize=5)
                    plt.yticks(np.arange(0, 1000+100,100), fontsize=5)
                    plt.plot(*zip(*iterPro.items()))
                    plt.xlabel('Restarts', fontsize=7)
                    plt.ylabel('Optimal choice', fontsize=7)
                    plt.title('Solving Knapsack using HillClimbing', fontsize=8)
                    self.KnapsackUI.canvaFrame.canvas.draw()
            else:
                dlg = AlertDialog("Vui lòng nhập đủ đầu vào cần thiết")
                dlg.exec()
        else:
            dlg = AlertDialog("Vui lòng dừng quá trình hiện tại")
            dlg.exec()
    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            print("Stop")
            self.KnapsackUI.tbResult.setText("")
            self.KnapsackUI.canvaFrame.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Core()
    plt.axis('off')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    with qtinter.using_qt_from_asyncio():
        window.show()
        sys.exit(app.exec())
