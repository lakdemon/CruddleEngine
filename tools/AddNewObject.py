#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
import signal

def sigint_handler():
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()


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
		check = QCheckBox("Usable?")
		addP  = QPushButton("Добавить точку")
		vbox  = QVBoxLayout()

		hhbox = QHBoxLayout()
		lbl = QLabel("Текстура(usable):")
		inpt  = QLineEdit()
		openButton = QPushButton("") 
		
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

        vbox = QVBoxLayout()
        vbox.addWidget(titl)
        vbox.addWidget(tex)
        vbox.addWidget(usbl)
        vbox.addWidget(trns)
        vbox.addWidget(sld)

        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        hbox.addLayout(vbox)
        
        self.setLayout(hbox)    
        
        #self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()
        
        
if __name__ == '__main__':
    
    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    #signal.signal(signal.S)
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())