import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from pprint import pprint
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from functools import partial



class AddFilmWindow(QMainWindow):
	def __init__(self, func, add=True):
		super().__init__()
		self.add1 = add
		self.sum1 = 0
		self.draw = func
		uic.loadUi('addEditCoffeeForm.ui', self)
		self.f = False
		self.initUI()


	def initUI(self):
		self.con = sqlite3.connect('coffee.sqlite')
		self.cur = self.con.cursor()
		if self.add1:
			max_id = self.cur.execute("""SELECT id FROM coffee ORDER BY id""").fetchall()[-1][0]
			self.spinBox_4.setValue(max_id + 1)
		if not self.add1:
			self.pushButton.setText('Изменить')
		self.pushButton.clicked.connect(self.add)

	def add(self):
		id = self.spinBox_4.value()
		variety = self.lineEdit.text()
		roasting = self.spinBox_2.value()
		ground = self.spinBox_3.value()
		taste = self.lineEdit_2.text()
		price = self.doubleSpinBox_2.value()
		volume = self.doubleSpinBox.value()
		self.status.setText('')
		if variety == '': variety = None
		if taste == '': taste = None
		params = [id, variety, roasting, ground, taste, price, volume]


		if self.add1:
			self.spinBox_4.setReadOnly(True)
			try:
				assert all([True if i is not None else False for i in params])
				self.cur.execute(f"""INSERT INTO coffee(id, variety, roasting, ground, taste, price, volume) 
				VALUES(?, ?, ?, ?, ?, ?, ?)""", tuple(params))
				self.con.commit()
				self.draw.draw()
				self.status.setText('Успешно')
				self.close()
			except Exception as e:
				self.status.setText('Неверные данные')
				print(e)

		else:
			params.reverse()
			try:
				print(params)
				assert all([True if i is not None else False for i in params])
				self.cur.execute(f"""UPDATE coffee SET volume = ?, price = ?,
				taste = ?, ground = ?, roasting = ?, variety = ? WHERE id = ?""", tuple(params))
				self.con.commit()
				self.draw.draw()
				self.status.setText('Успешно')
				self.close()
			except Exception as e:
				self.status.setText('Неверные данные')
				print(e)


class Example(QMainWindow):
	def __init__(self):
		super().__init__()
		self.sum1 = 0
		uic.loadUi('1.ui', self)
		self.f = False
		self.initUI()

	def initUI(self):
		self.con = sqlite3.connect('coffee.sqlite')
		self.cur = self.con.cursor()
		self.draw()

		self.pushButton.clicked.connect(partial(self.push, True))
		self.pushButton_2.clicked.connect(partial(self.push, False))

	def draw(self):
		data = self.cur.execute(f"""SELECT * FROM coffee""").fetchall()

		data = [list(i) for i in data]
		self.tableWidget.setColumnCount(len(data[0]))
		self.tableWidget.setRowCount(len(data))
		self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки(1 - 5)",
														'молотый(1)/в зернах(0)', 'описание вкуса', 'цена(руб)',
														'объем упаковки(г)'])
		for i in range(len(data)):
			for j in range(len(data[0])):
				self.tableWidget.setItem(
					i, j, QTableWidgetItem(str(data[i][j])))
		self.tableWidget.resizeColumnsToContents()

	def push(self, add=True):
		self.addwin = AddFilmWindow(self, add=add)
		self.addwin.show()


def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.excepthook = except_hook
	ex.show()
	sys.exit(app.exec())
