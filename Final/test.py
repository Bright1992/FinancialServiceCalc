import sys
from PyQt4 import QtGui


class GridLayout(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.setWindowTitle('grid layout')

        names = ['1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16',
            '17', '18', '19', '20']

        grid = QtGui.QGridLayout()

        j = 0
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 0), (3, 1), (3, 2), (3, 3 ),
                (4, 0), (4, 1), (4, 2), (4, 3)]

        for i in names:
            bsr = QtGui.QTextBrowser()
            grid.addWidget(bsr, pos[j][0], pos[j][1])
            j = j + 1

        self.setLayout(grid)

app = QtGui.QApplication(sys.argv)
ex = GridLayout()
ex.show()
sys.exit(app.exec_())