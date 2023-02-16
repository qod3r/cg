from pprint import pprint
import sys
from PyQt5 import uic
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPainter, QPixmap, QColor, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QWidget
import random


X, Y = 0, 1


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('3.ui', self)
        
        self.colors = ["#BF616A", "#D08770", "#EBCB8B", "#A3BE8C", "#B48EAD", "#4C566A"]
        self.coords = (0, 0)
        pix = QPixmap(self.label.size())
        pix.fill(QColor("#2E3440"))
        self.label.setPixmap(pix)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.btn_circle.clicked.connect(self.set_shape)
        self.btn_square.clicked.connect(self.set_shape)
        self.btn_triangle.clicked.connect(self.set_shape)
        
        self.shape = "Circle"
        self.label_curr_figure.setText(self.shape)
        self.shapes = []
        
        self.setMouseTracking(True)
    
    def set_shape(self):
        self.shape = self.sender().text()
        self.label_curr_figure.setText(self.shape)
    
    def add_shape(self):
        boxes = {
            'Circle': 30,
            'Square': 20,
            'Triangle': 25
        }
        self.shapes.append({"name": self.shape,
                            "coords": self.coords,
                            "color": random.choice(self.colors),
                            "box": boxes[self.shape]})
        self.draw_shapes()
    

    def remove_shape(self):
        x = self.coords[X]
        y = self.coords[Y]
        for i, shape in enumerate(self.shapes[::-1]):
            if x <= shape['coords'][X] + shape['box'] \
                and x >= shape['coords'][X] - shape['box'] \
                and y <= shape['coords'][Y] + shape['box'] \
                and y >= shape['coords'][Y] - shape['box']:
                    self.shapes.pop(len(self.shapes) - 1 - i)
                    break
        self.draw_shapes()
        self.update()
    
    
    def draw_shapes(self):
        p = QPainter(self.label.pixmap())
        self.label.pixmap().fill(QColor("#2E3440"))
        for shape in self.shapes:
            if shape['name'] == "Circle":
                # print("circle", shape['coords'])
                pen = QPen()
                pen.setWidth(5)
                pen.setColor(QColor(shape['color']))
                # radius = random.randint(20, 60)
                radius = shape['box']
                p.setPen(pen)
                p.setBrush(QColor(shape['color']))
                p.drawEllipse(QPoint(shape['coords'][X], shape['coords'][Y]), radius, radius)
            elif shape['name'] == "Square":
                # print("square", shape['coords'])
                pen = QPen()
                # pen.setWidth(random.randint(20, 100))
                pen.setWidth(shape['box']*2)
                pen.setColor(QColor(shape['color']))
                p.setPen(pen)
                p.drawPoint(shape['coords'][X], shape['coords'][Y])
            elif shape['name'] == "Triangle":
                # print("triangle", shape['coords'])
                pen = QPen()
                pen.setWidth(5)
                pen.setColor(QColor(shape['color']))
                p.setPen(pen)
                p.setBrush(QColor(shape['color']))
                x = shape['coords'][X]
                y = shape['coords'][Y]
                # size = random.randint(20, 100)
                size = shape['box']*2
                poly = QPolygon([
                    QPoint(x - size//2, y - size//2),
                    QPoint(x + size//2 , y - size//2),
                    QPoint(x, y + size//2)
                ])
                p.drawPolygon(poly)
                
        p.end()
        self.update()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        self.coords = (event.x(), event.y())

    def mousePressEvent(self, event: QMouseEvent):
        if (event.button() == Qt.LeftButton):
            self.add_shape()
        elif (event.button() == Qt.RightButton):
            self.remove_shape()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())