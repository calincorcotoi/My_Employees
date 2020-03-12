from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys,os
import sqlite3
from PIL import Image
##test
con = sqlite3.connect("employees.db")
cur = con.cursor()
defaultImg = "images/person.png"
class Main(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("My Employees")
		self.setGeometry(450,150,750,600)
		self.UI()
		self.layout()
		self.show()

	def UI(self):
		self.mainDesing()
		self.layouts()
		self.getEmployees()
		self.displayFirstRecord()

	def mainDesing(self):
		self.employeeList = QListWidget()

		self.btnNew    = QPushButton("New")
		self.btnUpdate = QPushButton("Update")
		self.btnDelete = QPushButton("Delete")

		self.btnNew.clicked.connect(self.addEmployee)
		self.employeeList.itemClicked.connect(self.singleClick)
		self.btnDelete.clicked.connect(self.deleteEmployee)
		self.btnUpdate.clicked.connect(self.updateEmployee)

	def layouts(self):
		self.setStyleSheet("font-size:14pt;font-family:Arial Bold;")
		########################Layout######################
		self.mainLayout = QHBoxLayout()
		self.leftLayout = QFormLayout()
		self.rightMainLayout = QVBoxLayout()
		self.rightTopLayout = QHBoxLayout()
		self.rightBottomLayout = QHBoxLayout()
		########################Adding child  layout to main layout#############
		self.rightMainLayout.addLayout(self.rightTopLayout)
		self.rightMainLayout.addLayout(self.rightBottomLayout)
		self.mainLayout.addLayout(self.leftLayout,40) #40% din cat ocupa din layout!!!!!!
		self.mainLayout.addLayout(self.rightMainLayout,60) #60% din cat ocupa din layout!!!!
		########################adding widgets##################
		self.rightTopLayout.addWidget(self.employeeList)
		self.rightBottomLayout.addWidget(self.btnNew)
		self.rightBottomLayout.addWidget(self.btnUpdate)
		self.rightBottomLayout.addWidget(self.btnDelete)
		#########################setting main window layout#########################
		self.setLayout(self.mainLayout)

	def addEmployee(self):
		self.newEmployee = AddEmployee()
		self.close()

	def getEmployees(self):
		query = "SELECT id,name,surname FROM employees"
		employees = cur.execute(query).fetchall()
		for employee in employees:
			self.employeeList.addItem(str(employee[0])+"-"+employee[1]+" "+employee[2])

	def displayFirstRecord(self):
		query = "SELECT * FROM employees ORDER BY ROWID ASC LIMIT 1"
		employee = cur.execute(query).fetchone()
		img = QLabel()
		img.setPixmap(QPixmap("images/"+employee[5]))
		name = QLabel(employee[1])
		surname = QLabel(employee[2])
		phone = QLabel(employee[3])
		email = QLabel(employee[4])
		address = QLabel(employee[6])
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SPATIU PE VERTICALA INTRE RANDURI 
		self.leftLayout.setVerticalSpacing(20)
		#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SPATIU PE VERTICALA INTRE RANDURI 

		self.leftLayout.addRow("",img)
		self.leftLayout.addRow("Name:",name)
		self.leftLayout.addRow("Surname:", surname)
		self.leftLayout.addRow("Email:", email)
		self.leftLayout.addRow("Phone:",phone)
		self.leftLayout.addRow("Address:",address)

	def singleClick(self):
		##DELETE THE OLD WIDGETS , to display the new information
		for i in reversed(range(self.leftLayout.count())):
			widget = self.leftLayout.takeAt(i).widget()
			if widget is not None:
				widget.deleteLater()

		employee = self.employeeList.currentItem().text()
		id_name = employee.split("-")
		id = id_name[0]
		query = ("SELECT * FROM employees WHERE id=?")
		person = cur.execute(query,(id,)).fetchone() #WE NEED TO USE TUPLE , SINGLE ITEM TUPLE EX = (1,)
		img = QLabel()
		img.setPixmap(QPixmap("images/"+person[5]))
		name = QLabel(person[1])
		surname = QLabel(person[2])
		phone = QLabel(person[3])
		email = QLabel(person[4])
		address = QLabel(person[6])
		self.leftLayout.addRow("",img)
		self.leftLayout.addRow("Name:",name)
		self.leftLayout.addRow("Surname:", surname)
		self.leftLayout.addRow("Email:", email)
		self.leftLayout.addRow("Phone:",phone)
		self.leftLayout.addRow("Address:",address)

	def deleteEmployee(self):
		if self.employeeList.selectedItems():
			person = self.employeeList.currentItem().text()
			id = person.split('-')[0]
			mbox = QMessageBox.question(self,"Warning","Are you sure to delete this person?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
			if mbox == QMessageBox.Yes:
				try:
					query = "DELETE FROM employees WHERE id=?"
					cur.execute(query,(id,))
					con.commit()
					QMessageBox.information(self,"Infi!!","Person has been deleted")
					self.close()
					self.main = Main()
				except:
					QMessageBox.information(self,"Warning!!","Person has not been deleted")
		else:
			QMessageBox.information(self,"Warning!!","Please select a person to delete")

	def updateEmployee(self):


class AddEmployee(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Add Employee")
		self.setGeometry(450, 150, 350, 600)
		self.UI()
		self.show()

	def UI(self):
		self.mainDesing()
		self.layouts()

	def closeEvent(self, event):
		self.main = Main()


	def mainDesing(self):
		#####################Top Layout widgets############################
		self.setStyleSheet("background-color:white;font-size:14pt;font-family:Times")

		self.title = QLabel("Add Person")

		#METODA PENTRU A SCHIMBA FONTUL LA TEXT FARA QFONT
		self.title.setStyleSheet("font-size:24pt;font-family:Arial Bold;background-color:red")

		self.imgAdd = QLabel()
		self.imgAdd.setPixmap(QPixmap("icons/person.png"))

		#####################Bottom Layout widgets############################
		self.nameLbl = QLabel("Name :")
		self.nameEntry = QLineEdit()
		self.nameEntry.setPlaceholderText("Enter Employee Name")

		self.surnameLbl = QLabel("Surname :")
		self.surnameEntry = QLineEdit()
		self.surnameEntry.setPlaceholderText("Enter Employee Surname")

		self.phoneLbl = QLabel("Phone :")
		self.phoneEntry = QLineEdit()
		self.phoneEntry.setPlaceholderText("Enter Employee Phone")

		self.emailLbl = QLabel("Email :")
		self.emailEntry = QLineEdit()
		self.emailEntry.setPlaceholderText("Enter Employee Email")

		self.imgLbl = QLabel("Picture :")
		self.imgButton = QPushButton("Browse")
		self.imgButton.setStyleSheet("background-color:orange;font-size:10pt")
		self.imgButton.clicked.connect(self.uploadImage)

		self.addressLbl = QLabel("Address :")
		self.addressEditor = QTextEdit()
		self.addButton = QPushButton("Add")
		self.addButton.setStyleSheet("background-color:orange;font-size:10pt")
		self.addButton.clicked.connect(self.addEmployee)
	def layouts(self):
		#################creating main layout################
		self.mainLayout = QVBoxLayout()
		self.topLayout = QVBoxLayout()
		self.bottomLayout = QFormLayout()

		###################adding child layouts to main layout########
		self.mainLayout.addLayout(self.topLayout)
		self.mainLayout.addLayout(self.bottomLayout)

		###################adding widgets to layouts#################
		##TOP Layout
		self.topLayout.addStretch()
		self.topLayout.addWidget(self.title)
		self.topLayout.addWidget(self.imgAdd)
		self.topLayout.addStretch()
		self.topLayout.setContentsMargins(110,20,10,30)	#left,top,right,bottom
		##BOTTOM Layout
		self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
		self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
		self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
		self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
		self.bottomLayout.addRow(self.imgLbl, self.imgButton)
		self.bottomLayout.addRow(self.addressLbl, self.addressEditor)
		self.bottomLayout.addRow("",self.addButton)#"" SIMULEAZA CA SI CUM AR FI UN LABEL FARA NUME CA SA SE PUNA PE COL 2

		#######################setting main layout for window#########
		self.setLayout(self.mainLayout)

	def uploadImage(self):
		global defaultImg
		size = (128,128)
		self.fileName,ok = QFileDialog.getOpenFileName(self,'Upload Image', "", "Image Files (*.jpg *.png)")

		if ok:
			print(self.fileName)
			defaultImg = os.path.basename(self.fileName)
			img = Image.open(self.fileName)
			img = img.resize(size)
			img.save("Imagess/{}".format(defaultImg))

	def addEmployee(self):
		global defaultImg
		name = self.nameEntry.text()
		surname = self.surnameEntry.text()
		phone = self.phoneEntry.text()
		email = self.emailEntry.text()
		img = defaultImg
		address = self.addressEditor.toPlainText()
		if (name and surname and phone != ""):
			try:
				query = "INSERT INTO employees (name,surname,phone,email,img,address) VALUES(?,?,?,?,?,?)"
				cur.execute(query, (name,surname,phone,email,img,address))
				con.commit()
				QMessageBox.information(self,"Success","Person has been added")
				self.close()
				self.main = Main()
			except:
				QMessageBox.warning(self,"Warning","Person has not been added")
		else:
			QMessageBox.warning(self,"Warning","Fields can not be empty")

def main():
	APP = QApplication(sys.argv)
	window = Main()
	sys.exit(APP.exec_())

if __name__ == "__main__":
	main()