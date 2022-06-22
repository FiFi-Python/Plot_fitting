from shutil import move
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
import  sys
import przyklad


class Window(QMainWindow):
    '''Klasa definiująca okno'''
    def __init__(self):
        QMainWindow.__init__(self)
    
        self.setGeometry(500, 500, 700, 700) #parametry okna
        self.setWindowTitle("Application: Plot fitting")
        self.UiComponents() # funkcja z komponentami jak na przyklad przycisk 
        self.show()


    def UiComponents(self):

        menuBar = self.menuBar()
        fileMenu = QMenu('&File', self)
        menuBar.addMenu(fileMenu)
        editMenu = menuBar.addMenu('&Edit')
        helpMenu = menuBar.addMenu('&Help')

        fileToolBar = self.addToolBar('File')
        editToolBar = QToolBar('Edit', self)

        self.button_1 = QPushButton('Load image', self) #nazwa 
        self.button_1.setToolTip('This is load picture button') #opis po najechaniu
        self.button_1.setGeometry(10, 15, 100, 40) #rozmiar przycisku
        self.button_1.move(100, 100) #gdzie ma byc przycisk
        self.button_1.clicked.connect(self.load_image) #co ma robic

        self.button_2 = QPushButton('File', self)
        self.button_2.move(200, 200)

        file = QMenu(self)
        file.addAction('Load image')
        file.addSeparator()
        file.addAction('Save image')
        self.button_2.setMenu(file)

        self.label = QLabel(self)
        self.label.move(10,50)
        self.show()

    @pyqtSlot()
    def load_image(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.*)")
        image_path = image[0]
        self.pixmap = QPixmap(image_path)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
        print(image_path)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())