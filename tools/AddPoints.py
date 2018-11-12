import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

points = []

class AddPoint(QWidget):
    def __init__(self):
        super().__init__()
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        #fname = "test.png"
        self.pixmap = QPixmap(fname)
        #self.setGeometry(30, 30, 500, 300)
        print(self.pixmap.size().width(),self.pixmap.size().height())
        self.setGeometry(30,30,self.pixmap.size().width(),self.pixmap.size().height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

        pen = QPen(Qt.red, 5)
        painter.setPen(pen)
        #painter.drawLine(10, 10, self.rect().width() -10 , 10)
        
        for i in range(1,len(points)):
        	pen = QPen(Qt.red, 2)
        	pen.setStyle(Qt.DotLine)
        	painter.setPen(pen)
        	try:
        		painter.drawLine(points[i][0],points[i][1],points[i-1][0],points[i-1][1],)
        	except Exception as e:
        		pass

        pen = QPen(Qt.green, 5)
        painter.setPen(pen)
        
        for point in points:
            painter.drawPoint(*point)

    def mouseMoveEvent(self, event):
        self.pos = event.pos()
        self.update()
        #print(self.pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:        
            print(event.pos().x(),event.pos().y())
            points.append([event.pos().x(),event.pos().y()])
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddPoint()
    ex.show()
    sys.exit(app.exec_())