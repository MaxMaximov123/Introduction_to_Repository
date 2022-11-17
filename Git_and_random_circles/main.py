import sys

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from random import randint
from UI import Ui_MainWindow

SCREEN_SIZE = [400, 400]



class Example(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		# uic.loadUi('UI.ui', self)
		self.setupUi(self)
		self.initUI()
		self.f = False

	def f1(self):
		self.f = True

	def colors(self):
		return randint(0, 255), randint(0, 255), randint(0, 255)

	def initUI(self):
		self.pushButton.clicked.connect(self.update)
		self.pushButton.clicked.connect(self.f1)

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.draw(qp)
		qp.end()

	def draw(self, qp):
		if self.f:
			qp.setBrush(QColor(*self.colors()))
			a = randint(1, 550)
			qp.drawEllipse(randint(1, 600 - a), randint(1, 600 - a), a, a)

def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.excepthook = except_hook
	ex.show()
	sys.exit(app.exec())
