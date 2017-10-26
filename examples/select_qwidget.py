import sys
from PyQt5.QtWidgets import *

class Window(QWidget):

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        label1 = QLabel(self.tr("Hello world!"))
        label2 = QLabel(self.tr("ABC DEF GHI"))
        label3 = QLabel(self.tr("Hello PyQt!"))
        
        label1.mouseReleaseEvent = self.showText1
        label2.mouseReleaseEvent = self.showText2
        label3.mouseReleaseEvent = self.showText3
        
        layout = QHBoxLayout(self)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
    
    def showText1(self, event):
        print("Label 1 clicked")
    
    def showText2(self, event):
        print("Label 2 clicked")
    
    def showText3(self, event):
        print("Label 3 clicked")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())