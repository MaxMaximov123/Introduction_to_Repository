import sqlite3
import sys

from PyQt5.QtWidgets import *


class Example(QWidget):
	def __init__(self):
		self.btns = []
		super().__init__()
		self.initUI()

	def initUI(self):
		self.con = sqlite3.connect('coffee.sqlite')
		self.cur = self.con.cursor()
		self.setGeometry(0, 0, 1000, 800)
		self.setWindowTitle('')
		self.tableWidget = QTableWidget(self)
		self.tableWidget.move(10, 40)
		self.tableWidget.resize(980, 720)

		data = self.cur.execute("""SELECT * FROM coffee""").fetchall()
		data = [list(i) for i in data]
		if data:
			self.tableWidget.setColumnCount(len(data[0]))
			self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки(1 - 5)",
														'молотый(1)/в зернах(0)', 'описание вкуса', 'цена(руб)',
														'объем упаковки(г)'])
			self.tableWidget.setRowCount(len(data))
			for i in range(len(data)):
				for j in range(len(data[0])):
					self.tableWidget.setItem(
						i, j, QTableWidgetItem(str(data[i][j])))

			self.tableWidget.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.excepthook = except_hook
	ex.show()
	sys.exit(app.exec())
