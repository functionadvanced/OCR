'''
The GUI made by PyQt6
'''
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton
from PyQt6 import QtCore
from PyQt6.QtCore import QCoreApplication, QBuffer, QIODevice
from PyQt6.QtGui import QPainter, QBrush, QColor, QImage
from PIL import Image
import sys
import io

import engine


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # set the title
        self.setWindowTitle("OCR for Math")
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.screen = QApplication.primaryScreen()
        # setting  the geometry of window
        # self.setGeometry(60, 60, 600, 400)

        # creating a label widget
        self.label = QLabel("figure", self)
        self.label_result = QLabel("result will be shown here", self)
        # moving position
        self.label.move(0, 100)
        self.label_result.move(0, 50)
        self.label_result.setWordWrap(True)

        # create button
        self.btn = QPushButton("exit", self)
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.exit_btn_clicked)

        self.btn_new_shot = QPushButton("New", self)
        self.btn_new_shot.clicked.connect(self.new_btn_clicked)
        self.btn_new_shot.move(100, 0)

        self.on_snip_flag = False
        # show all the widgets
        # self.show()
        self.GUI_normal()

    def GUI_normal(self):
        self.btn.show()
        self.btn_new_shot.show()
        self.label.show()
        self.label_result.show()
        self.setWindowOpacity(1)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowType.FramelessWindowHint)
        self.show()

    def GUI_snip(self):
        self.setWindowOpacity(0.5)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.btn_new_shot.hide()
        self.btn.hide()
        self.label.hide()
        self.label_result.hide()
        self.setGeometry(0, 0, self.screen.size().width(), self.screen.size().height())
        self.show()
        
        # self.setWindowState(QtCore.Qt.WindowState.WindowFullScreen)

    def paintEvent(self, event):
        if self.on_snip_flag:
            qp = QPainter(self)
            br = QBrush(QColor(100, 10, 10, 40))  
            qp.setBrush(br)   
            qp.drawRect(QtCore.QRect(self.begin, self.end))

    def exit_btn_clicked(self):
        QCoreApplication.quit()

    def new_btn_clicked(self):
        self.on_snip_flag = True
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.GUI_snip()

    def mouseMoveEvent(self, event):
        '''If mouse tracking is disabled (the default), 
        the widget only receives mouse move events 
        when at least one mouse button is pressed while the mouse is being moved.'''
        if self.on_snip_flag:
            self.end = event.pos()
            self.update()

    def mousePressEvent(self, event):
        if self.on_snip_flag:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.on_snip_flag:
            self.take_screenshot(self.begin, self.end)
            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def take_screenshot(self, start_point, end_point):
        a = min(start_point.x(), end_point.x())
        b = min(start_point.y(), end_point.y())
        c = max(start_point.x(), end_point.x())
        d = max(start_point.y(), end_point.y())

        # generate PIL image
        self.setWindowOpacity(0)
        self.screenshot = self.screen.grabWindow(0, a, b, c-a, d-b)     
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.ReadWrite)
        self.screenshot.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        buffer.close()
        result_str = " ".join(engine.identify(pil_im))
        self.label_result.setText(result_str)
        self.label_result.adjustSize()
        # print(engine.identify(pil_im))

        # restore the GUI
        self.GUI_normal()
        self.setWindowOpacity(1)
        self.setGeometry(60, 60, max(c-a, 200), 400)
        self.label.setPixmap(self.screenshot)
        self.label.adjustSize()
        self.on_snip_flag = False
        self.GUI_normal()
        


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()