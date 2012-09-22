# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog
from PyQt4.QtCore import QThread
from imagepro import *

class Ui_MainWindow(QtGui.QMainWindow):	
	
	def setupUi(self,path):
		self.setWindowTitle("Gnome-BAXC")
		self.resize(560, 512)
		self.centralwidget = QtGui.QWidget(self)
		self.mainLayout = QtGui.QGridLayout(self.centralwidget)
		self.subLayout = QtGui.QGridLayout()

		self.selectImageLabel = QtGui.QLabel("Select Images :", self.centralwidget)
		self.subLayout.addWidget(self.selectImageLabel, 0, 0, 1, 1)
		
		self.durationSplitter = QtGui.QSplitter(self.centralwidget)
		self.durationSplitter.setOrientation(QtCore.Qt.Horizontal)
		self.durationLabel = QtGui.QLabel("Duration (in min) :", self.durationSplitter)
		self.doubleSpinBox = QtGui.QDoubleSpinBox(self.durationSplitter)
		self.doubleSpinBox.setMinimum(1.00)
		self.doubleSpinBox.setValue(30.00)
		self.doubleSpinBox.setSingleStep (5.00)
		self.subLayout.addWidget(self.durationSplitter, 2, 0, 1, 1)


		self.btnSplitter = QtGui.QSplitter(self.centralwidget)
		self.btnSplitter.setOrientation(QtCore.Qt.Horizontal)
		self.markAllBtn = QtGui.QPushButton("Mark All", self.btnSplitter)
		self.unmarkAllBtn = QtGui.QPushButton("Unmark All", self.btnSplitter)
		self.loadBtn = QtGui.QPushButton("Load images", self.btnSplitter)
		self.setBackgrdBtn = QtGui.QPushButton("Set Background" ,self.btnSplitter)
		self.cancelBtn = QtGui.QPushButton("Cancel",self.btnSplitter)
		self.subLayout.addWidget(self.btnSplitter, 2, 1, 1, 1)
			

		self.imageScrollArea = QtGui.QScrollArea(self.centralwidget)
		self.imageScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)		
		self.imageScrollArea.setWidgetResizable(True)
		self.scrollAreaContents = QtGui.QWidget()
		self.scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 521, 396))
		
		self.imageGrid = QtGui.QGridLayout(self.scrollAreaContents)
		self.setcheckbox(path)
		self.imageScrollArea.setWidget(self.scrollAreaContents)
		self.subLayout.addWidget(self.imageScrollArea, 1, 0, 1, 2)
		
		self.mainLayout.addLayout(self.subLayout, 0, 0, 1, 1)
		
		self.setCentralWidget(self.centralwidget)
		
		self.menubar = QtGui.QMenuBar(self)
		self.menuFile = QtGui.QMenu("&File", self.menubar)
		self.menuHelp = QtGui.QMenu("&Help", self.menubar)
		self.setMenuBar(self.menubar)

		self.actionQuit = QtGui.QAction("&Quit", self)
		self.actionQuit.setShortcut( "Ctrl+Q")
		self.actionAbout = QtGui.QAction("About", self)
		self.menuFile.addAction(self.actionQuit)
		self.menuHelp.addAction(self.actionAbout)
		
		self.menubar.addMenu(self.menuFile)
		self.menubar.addMenu(self.menuHelp)
		
		self.statusbar = QtGui.QStatusBar(self)
		self.setStatusBar(self.statusbar)

		self.setConnections()




	def __init__(self,path):
		super(Ui_MainWindow, self).__init__()
		self.xmlcreator = xmlCreator()
		self.initImageThread()
		self.setupUi(path)
		self.show()	

	def setConnections(self):
		QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.close)
		QtCore.QObject.connect(self.setBackgrdBtn, QtCore.SIGNAL("clicked()"), self.getselected)
		QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("activated(int)"), self.close)
		QtCore.QObject.connect(self.actionAbout,QtCore.SIGNAL("activated()"),self.About)
		QtCore.QObject.connect(self.loadBtn, QtCore.SIGNAL("clicked()"), self.dirsel)
		QtCore.QObject.connect(self.markAllBtn, QtCore.SIGNAL("clicked()"), self.markall)
		QtCore.QObject.connect(self.unmarkAllBtn, QtCore.SIGNAL("clicked()"), self.unmarkall)
		QtCore.QMetaObject.connectSlotsByName(self)

	def initImageThread(self):
		self.thread  = ReadTImage()
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL('started()'), self.startimageload)
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL('imageloaded(const QString&,QImage)'), self.imageloaded)
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL('finished()'), self.endimageload)


	def setcheckbox(self,path):
		self.image=list()
		self.path=path+'/'
		self.thread.setPath(self.path)
		self.thread.start()


	def imageloaded(self,text,icon_image):
		index = len(self.image)
		pix = QtGui.QPixmap.fromImage(icon_image)
		icon = QtGui.QIcon(pix)
		self.image.append(QtGui.QCheckBox(self.scrollAreaContents))
		self.image[index].setText(text)
		self.image[index].setIcon(icon)
		self.image[index].setIconSize(QtCore.QSize(150, 150))
		self.imageGrid.addWidget(self.image[index], index+1, 0, 1, 1)

	def getselected(self):
		time=self.doubleSpinBox.value()
		outfile=self.path+"background.xml"
		for image in self.image:
			if image.checkState():
				self.xmlcreator.addimage(self.path + image.text())

		xml = self.xmlcreator.create_xml((time*60.0)-5)
		try:	
			f=open(outfile,'w')
			f.write(xml)
			f.close()
			self.xmlcreator.close(outfile)
		except IOError as e:
			QtGui.QMessageBox.critical(self,"IOError",str(e))
		if self.xmlcreator.getimagecount()!=0:
			QtGui.QMessageBox.about(self,"XML File Created",finalmsg(outfile,self.xmlcreator.getimagecount()))
			self.close()

				
	def markall(self):
		for i in self.image:
			i.setCheckState(True)

	def unmarkall(self):
		for i in self.image:
			i.setCheckState(False)

	def About(self):
		QtGui.QMessageBox.about(self,"About",aboutmsg)

	def dirsel(self):
		dirs = QFileDialog.getExistingDirectory(self, "Open Directory","/home",QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks)
		if dirs !="":
			dirs = dirs+"/"
			print (dirs)
			for i in range(self.imageGrid.count()):
				self.imageGrid.itemAt(i).widget().close()
			self.image[:] = []
			self.setcheckbox(dirs)

	def startimageload(self):
		self.statusbar.clearMessage()
		self.statusbar.showMessage("Image loading ......")


	def endimageload(self):
		self.statusbar.clearMessage()
		self.statusbar.showMessage("Image loading finished",1000)


class ReadTImage(QThread): 
	def __init__(self, path = None): 
		super().__init__() 
		self.exiting = False
		self.path = path

	def setPath(self,path):
		self.exiting = False
		self.path = path

	def run(self): 
		dirs = os.listdir(self.path)
		dirs.sort()
		for filename in dirs:
			if isimage(filename):
				image = QtGui.QImage(self.path+filename)
				self.emit(QtCore.SIGNAL('imageloaded(const QString&, QImage)'), filename, image)
			else:
				pass


	def stop(self):
		pass

	def __del__(self):
		self.exiting = True
		self.wait()