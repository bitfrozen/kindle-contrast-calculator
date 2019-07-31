import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QDialog, QColorDialog
from PySide2.QtGui import QColor

class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setWindowTitle("Kindle contrast calc")
        self.resize(400, 200)
        # Set variables
        self.currentColor = QColor(0,0,0,255)
        # Creating widgets
        self.colorDisplayLabel = QtWidgets.QLabel()
        self.colorDisplayLabel.setStyleSheet("QLabel {background-color : rgb(255,255,255);}")
        self.colorDisplayLabel.setFixedHeight(40)
        self.colorInfoLabel = QtWidgets.QLabel()
        self.colorInfoLabel.setText("No color selected")
        self.colorButton = QtWidgets.QPushButton()
        self.colorButton.setText("Select color")
        # Create layout and add widgets to it
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.colorDisplayLabel)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.colorInfoLabel)
        mainLayout.addStretch()
        mainLayout.addWidget(self.colorButton)
        self.setLayout(mainLayout)
        # Setup form connections
        self.colorButton.clicked.connect(self.onClicked)

    def contrastCalc(self, color):
        contrast = (0.2126 * color.red()) + (0.7152 * color.green()) + (0.0722 * color.blue())
        return contrast

    def onClicked(self):
        self.currentColor = QColorDialog.getColor(self.currentColor, self, 'Select color', QColorDialog.ColorDialogOption.DontUseNativeDialog)
        contrastValue = self.contrastCalc(self.currentColor)
        self.updateColorLabel(self.currentColor)
        self.updateInfoLabel(contrastValue)

    def updateColorLabel(self, color):
        styleString = "QLabel {{background-color : rgb({},{},{});}}".format(color.red(), color.green(), color.blue())
        self.colorDisplayLabel.setStyleSheet(styleString)

    def updateInfoLabel(self, contrastValue):
        contrastText = ''

        if contrastValue < 102:
            if (102 - contrastValue) > 10:
                contrastText = 'way '
            contrastText = contrastText + 'too dark'
        elif contrastValue > 153:
            if (contrastValue - 153) > 10:
                contrastText = 'way '
            contrastText = contrastText + 'too bright'
        else:
            contrastText = 'right'

        self.colorInfoLabel.setText("Selected color is {}".format(contrastText))


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MainForm()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
