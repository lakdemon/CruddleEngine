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
        openButton = QPushButton("")
        openButton.setMaximumWidth(50)
        url = QLineEdit()

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addWidget(lbl)
        hbox.addWidget(url)
        hbox.addWidget(openButton)

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
				
	def HLine(self):
		toto = QFrame()
		toto.setFrameShape(QFrame.HLine)
		toto.setFrameShadow(QFrame.Sunken)
		return toto


class TRANSPARENT(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		check = QCheckBox("Transparent?")
		addP  = QPushButton("Добавить точку")
		vbox  = QVBoxLayout()
		addP.setEnabled(False)

		hhbox = QHBoxLayout()
		lbl = QLabel("Текстура(transparent):")
		inpt  = QLineEdit()
		openButton = QPushButton("") 
		lbl.setEnabled(False)
		inpt.setEnabled(False)
		openButton.setEnabled(False)

		hhbox.addWidget(lbl)
		hhbox.addWidget(inpt)
		hhbox.addWidget(openButton)

		vbox.addWidget(check)
		vbox.addLayout(hhbox)
		vbox.addWidget(addP)

		hbox = QHBoxLayout()
		#vbox.addStretch(1)
		hbox.addLayout(vbox)
        
		self.setLayout(hbox) 


class SOLID(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		check = QCheckBox("Solid?")
		addP  = QPushButton("Добавить точку")
		vbox  = QVBoxLayout()
		addP.setEnabled(False)

		vbox.addWidget(check)
		vbox.addWidget(addP)

		hbox = QHBoxLayout()
		#vbox.addStretch(1)
		hbox.addLayout(vbox)
        
		self.setLayout(hbox) 


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        tex  = TEXTURE()
        usbl = USABLE() 
        titl = TITLE()
        trns = TRANSPARENT()
        sld  = SOLID()
        none1= QLabel()
        none2= QLabel()
        final= QPushButton("Создать")
        lasth= QHBoxLayout()

        lasth.addWidget(none1)
        lasth.addWidget(final)
        lasth.addWidget(none2)

        vbox = QVBoxLayout()
        vbox.addWidget(titl)
        vbox.addWidget(tex)

        vbox.addWidget(usbl)
        vbox.addWidget(trns)
        vbox.addWidget(sld)
        vbox.addLayout(lasth)

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addLayout(vbox)
        
        final.clicked.connect(self.buttonClicked)

        self.setLayout(hbox)    
        
        #self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()


    def buttonClicked(self):
    	s = json.dumps(obj, default=lambda x: x.__dict__)
    	print(s)

        
        
if __name__ == '__main__':
    
    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    #signal.signal(signal.S)
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())