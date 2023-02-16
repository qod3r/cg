import sys
from math import sin, cos
from PyQt5 import uic
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap, QColor, QPen, QPolygon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('rotate.ui', self)
        
        pix = QPixmap(self.label.size())
        pix.fill(QColor("white"))
        self.label.setPixmap(pix)
        
        self.btn_cw.clicked.connect(self.rotate)
        self.btn_ccw.clicked.connect(self.rotate)
        
        self.angle = 0
        self.draw_tri()
    
    def rotate(self):
        btn = self.sender().text()
        if btn == "-->":
            self.angle += 0.785398
        if btn == "<--":
            self.angle -= 0.785398
        self.draw_tri()
    
    def draw_tri(self):
        painter = QPainter(self.label.pixmap())
        self.label.pixmap().fill(QColor("white"))
        pen = QPen()
        pen.setWidth(5)
        painter.setPen(pen)
        
        cx = 320
        cy = 200
        size = 100
        a = self.angle
        
        self.points = [
            QPoint(cx - size//2, cy - size//2),
            QPoint(cx + size//2 , cy - size//2),
            QPoint(cx, cy + size//2)
        ]
        for i, p in enumerate(self.points):
            self.points[i] = QPoint(
                int((p.x() - cx) * cos(a) - (p.y() - cy) * sin(a) + cx),
                int((p.x() - cx) * sin(a) + (p.y() - cy) * cos(a) + cy)
            )

        painter.drawPolygon(QPolygon(self.points))
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())