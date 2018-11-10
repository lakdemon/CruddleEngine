#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import json

import signal

def sigint_handler():
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()


class jsonFile(object):
	"""docstring for testobject"""
	
	def __init__(self):
		self.is_usable = False
		self.is_solid  = False
		self.is_transparent = False

obj = jsonFile()


class TITLE(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		lbl = QLabel("Название:")
		inp = QLineEdit()

		hbox = QHBoxLayout()
		hbox.addWidget(lbl)
		hbox.addWidget(inp)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox)
        
		self.setLayout(vbox) 


class TEXTURE(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):

        lbl = QLabel("Текстура")
        self.openButton = QPushButton("")
        self.openButton.setMaximumWidth(50)
        self.url = QLineEdit()

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addWidget(lbl)
        hbox.addWidget(self.url)
        hbox.addWidget(self.openButton)

        vbox = QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        #self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()


class USABLE(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.rightFrame = QFrame(self)
		self.rightFrame.setFrameShape(QFrame.Box)
		self.rightFrame.setFrameShadow(QFrame.Sunken)

		self.check = QCheckBox("Usable?")
		self.check.setStyleSheet("font-weight: 550")
		self.check.stateChanged.connect(self.Clicked)
		self.addP  = QPushButton("Добавить точку")
		vbox  = QVBoxLayout(self.rightFrame)

		hhbox = QHBoxLayout()
		self.lbl = QLabel("Текстура(usable):")
		self.inpt  = QLineEdit()
		self.openButton = QPushButton("") 
		
		hhbox.addWidget(self.lbl)
		hhbox.addWidget(self.inpt)
		hhbox.addWidget(self.openButton)


		self.lbl.hide()
		self.inpt.hide()
		self.openButton.hide()
		self.addP.hide()
		#self.line = QHLine()

		vbox.addWidget(self.check)
		vbox.addLayout(hhbox)
		vbox.addWidget(self.addP)
		

		hbox = QHBoxLayout()

		#vbox.addStretch(1)
		hbox.addLayout(vbox)
		hbox.addWidget(self.rightFrame)
        
		self.setLayout(hbox) 

	def Clicked(self,state):
		if state == Qt.Checked:
			self.lbl.show()
			self.inpt.show()
			self.openButton.show()
			self.addP.show()
			self.hidden = False
			obj.is_usable = True
		else:
			self.lbl.hide()
			self.inpt.hide()
			self.openButton.hide()
			self.addP.hide()			
			self.hidden = True
			obj.is_usable = False		
				


class TRANSPARENT(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.rightFrame = QFrame(self)
		self.rightFrame.setFrameShape(QFrame.Box)
		self.rightFrame.setFrameShadow(QFrame.Sunken)

		self.check = QCheckBox("Transparent?")
		self.check.setStyleSheet("font-weight: 550")
		self.check.stateChanged.connect(self.Clicked)
		self.addP  = QPushButton("Добавить точку")
		self.vbox  = QVBoxLayout(self.rightFrame)
		self.hhbox = QHBoxLayout()
		self.lbl = QLabel("Текстура(transparent):")
		self.inpt  = QLineEdit()
		self.openButton = QPushButton("") 
		
		self.lbl.hide()
		self.inpt.hide()
		self.openButton.hide()
		self.addP.hide()

		self.hhbox.addWidget(self.lbl)
		self.hhbox.addWidget(self.inpt)
		self.hhbox.addWidget(self.openButton)

		self.vbox.addWidget(self.check)
		self.vbox.addLayout(self.hhbox)
		self.vbox.addWidget(self.addP)

		self.hbox = QHBoxLayout()
		#vbox.addStretch(1)
		self.hbox.addLayout(self.vbox)
		self.hbox.addWidget(self.rightFrame)
        
		self.setLayout(self.hbox) 

	def Clicked(self,state):
		if state == Qt.Checked:
			self.lbl.show()
			self.inpt.show()
			self.openButton.show()
			self.addP.show()
			self.hidden = False
			obj.is_transparent = True
		else:
			self.lbl.hide()
			self.inpt.hide()
			self.openButton.hide()
			self.addP.hide()			
			self.hidden = True
			obj.is_transparent = False	


class SOLID(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.rightFrame = QFrame(self)
		self.rightFrame.setFrameShape(QFrame.Box)
		self.rightFrame.setFrameShadow(QFrame.Sunken)
		self.check = QCheckBox("Solid?")
		self.check.stateChanged.connect(self.Clicked)
		self.check.setStyleSheet("font-weight: 550")
		self.addP  = QPushButton("Добавить точку")
		self.addP.hide()
		vbox  = QVBoxLayout(self.rightFrame)
		

		vbox.addWidget(self.check)
		vbox.addWidget(self.addP)

		hbox = QHBoxLayout()
		#vbox.addStretch(1)
		hbox.addLayout(vbox)
		hbox.addWidget(self.rightFrame)
        
		self.setLayout(hbox) 

	def Clicked(self,state):
		if state == Qt.Checked:
			self.addP.show()
			obj.is_solid = True
		else:
			self.addP.hide()			
			obj.is_solid = False	


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.spacer = QLabel()

        self.tex  = TEXTURE()
        self.usbl = USABLE() 
        self.titl = TITLE()
        self.trns = TRANSPARENT()
        self.sld  = SOLID()
        self.none1= QLabel()
        self.none2= QLabel()
        self.final= QPushButton("Создать")
        self.lasth= QHBoxLayout()

        self.lasth.addWidget(self.none1)
        self.lasth.addWidget(self.final)
        self.lasth.addWidget(self.none2)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.titl)
        self.vbox.addWidget(self.tex)
        self.vbox.addWidget(self.spacer)

        self.vbox.addWidget(self.usbl)
        self.vbox.addWidget(self.trns)
        self.vbox.addWidget(self.sld)
        self.vbox.addLayout(self.lasth)

        self.hbox = QHBoxLayout()
        #hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        
        self.final.clicked.connect(self.buttonClicked)
        self.tex.openButton.clicked.connect(self.setTexture)

        self.setLayout(self.hbox)    
        
        #self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()


    def buttonClicked(self):
    	s = json.dumps(obj, default=lambda x: x.__dict__)
    	print(s)

    def setTexture(self):
    	fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
    	self.tex.url.setText(fname)
    	print(fname)

             
if __name__ == '__main__':
    
    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    #signal.signal(signal.S)
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())