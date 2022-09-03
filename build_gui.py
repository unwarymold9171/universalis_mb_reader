from PyQt5 import QtCore, QtGui, QtWidgets
import gui
import universalisAPI as uapi
import fetchItemIDs as fetch
import sys

class GUI(object):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(MainWindow)

        self._set_custom_action()
        self._hide_shortcuts()

        MainWindow.show()
        sys.exit(app.exec_())

    def _set_custom_action(self):
        """
        This prevents problems that can be caused by copying the code created by pyqt convertion
        """
        self.ui.addButton.clicked.connect(self.add_item_by_id)
        self.ui.idList.itemClicked.connect(self.idList_selection)
        self.ui.nameList.itemClicked.connect(self.nameList_selection)

        # Hidden menubar items, because by default there can only be one shortcut assigned
        self.ui.actionAdd.triggered.connect(self.ui.addButton.click)
    
    def _hide_shortcuts(self):
        """
        When setting the title of a menubar title it 'disables' it, but if it is set invisable the items in it cannot be interacted with (even if they have shortcuts set up)
        """
        self.ui.menuShortcuts.setTitle('')

    def add_item_by_id(self):
        idnum = int(self.ui.itemIdAdd.text())
        try:
            item_name = fetch.get_item_name(idnum)
        except:
            # It is posible to enter a number out of the range of items
            return
        
        if item_name == '':
            return

        self.ui.idList.addItem(str(idnum))
        self.ui.nameList.addItem(item_name)
    
    def idList_selection(self):
        self.ui.nameList.clearSelection()
    
    def nameList_selection(self):
        self.ui.idList.clearSelection()

    def test(self):
        # selected = self.idList.selectedIndexes()[0].row()
        # print(selected)
        self.ui.dcComboBox.clear()
        self.ui.dcComboBox.addItem('All')
        # self.comboBox_2
        return

if __name__ == "__main__":
    ui = GUI()