from functools import partial
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import * # QApplication, QLabel, QMainWindow, QMenu
from PyQt5.QtGui import *


class Window(QMainWindow):
    '''Main window'''
    def __init__(self, parent=None):
        super().__init__(parent)
        

        self.setWindowIcon(QIcon('./icons-shadowless-24/logo.jpg'))
        #self.label = QLabel('JPII', self)
        #self.label.setStyleSheet('border: 0.5px solid black;')
        self.setWindowTitle('Plot fitting: Menus & Toolbars')
        self.resize(500, 300)
        self.centralWidget = QLabel('Hello user!')
        self.centralWidget.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

        self.label = QLabel(self)
        self.label.move(100,100)

        self._createActions()
        self._createMenuBar()
        self._createToolBars()
        self._createContextMenu()
        self._connectActions()
        self._createStatusBar()


    def _createMenuBar(self):
        ''''''
        menuBar = self.menuBar()
        #File menu
        fileMenu = QMenu('&File', self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
        self.openRecentMenu = fileMenu.addMenu('Open Recent')
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveAaction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        #Edit menu
        editMenu =menuBar.addMenu('&Edit')
        editMenu.addAction(self.changeAction)
        #Hepl menu 
        helpMenu = menuBar.addMenu('&Help')
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.aboutAction)


    def _createToolBars(self):
        ''''''
        #File toolbar
        fileToolBar = self.addToolBar('File')
        fileToolBar.addAction(self.openAction)
        fileToolBar.addAction(self.saveAaction)
        #Edit toolbar 
        editToolBar = QToolBar('Edit', self)
        self.addToolBar(editToolBar)
        editToolBar.addAction(self.changeAction)
        # Using a QToolBar object
        editToolBar = QToolBar("Edit", self)
        self.addToolBar(editToolBar)
        #Using a QToolBar object and a toolbar area
        helpToolBar = QToolBar('Help', self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, helpToolBar)


    def _createActions(self):
        ''''''
        # self.newAction = QAction('&New', self)
        self.openAction = QAction(QIcon("./icons-shadowless-24/plus.png"), '&Open...', self)
        self.saveAaction = QAction(QIcon("./icons-shadowless-24/tick.png"), '&Save', self)
        self.exitAction = QAction(QIcon("./icons-shadowless-24/prohibition.png"), '&Exit')
        self.changeAction = QAction(QIcon("./icons-shadowless-24/wand.png"), '&Change', self) #tutaj dodac to ręczne dopasowanie osi
        self.helpContentAction = QAction(QIcon("./icons-shadowless-24/book.png"), '&Help Content', self)
        self.aboutAction = QAction(QIcon("./icons-shadowless-24/yin-yang.png"), '&About', self)
        
        self.openAction.setShortcut('Ctrl+O')
        self.saveAaction.setShortcut('Ctrl+S')
        self.changeAction.setShortcut('Ctrl+L')
        self.exitAction.setShortcut('Ctrl+E')
        self.helpContentAction.setShortcut('Ctrl+H')
        self.aboutAction.setShortcut('Ctrl+A')

        open_tip = 'Open a new file'
        self.openAction.setStatusTip(open_tip)
        self.openAction.setToolTip(open_tip)
        save_tip = 'Save a create image'
        self.saveAaction.setStatusTip(save_tip)
        self.saveAaction.setToolTip(save_tip)
        #dodac o change, help i innych jezeli jest taka potrzeba, konstrukcja jak powyzej



    def _createContextMenu(self):
        #Setting contextMenuPolicy, menu po klikniecciu prawym przyciskiem myszy
        self.centralWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.centralWidget.addAction(self.openAction)
        self.centralWidget.addAction(self.saveAaction)
        self.centralWidget.addAction(self.changeAction)
        self.centralWidget.addAction(self.exitAction)


    def populateOpenRecent(self):
        self.openRecentMenu.clear()
        actions = list()
        filenames = [f"Plot-{i}" for i in range(4)]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.openRecentFile, filename))
            actions.append(action)
        self.openRecentMenu.addActions(actions)


    def openFile(self): # w tych funkcjach nalezy to robic to znaczy napisac zapisywanie itp 
        self.centralWidget.setText("<b>File > Open...</b> clicked")
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.*)")
        image_path = image[0]
        self.pixmap = QPixmap(image_path)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())
    
    def openRecentFile(self, filename):
        self.centralWidget.setText(f"<b>{filename}</b> opened")


    def saveFile(self):
        self.centralWidget.setText("<b>File > Save</b> clicked")



    def changeContent(self):
        self.centralWidget.setText("<b>Edit > Change</b> clicked")


    def helpContent(self):
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")


    def about(self):
        self.centralWidget.setText("<b>Help > About...</b> clicked")


    def _connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.saveAaction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit action
        self.changeAction.triggered.connect(self.changeContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)
        self.openRecentMenu.aboutToShow.connect(self.populateOpenRecent)
        

    
    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready', 3000) #po 3000 milisekund znika i czysci sie status 

    
    def load_image(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.*)")
        image_path = image[0]
        self.pixmap = QPixmap(image_path)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())