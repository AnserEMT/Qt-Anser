""" Displays a grid of test points representing the calibration test points on the baseplate of field generator board """
from pyqtgraph import GraphicsView, GraphItem, TextItem, ViewBox
import numpy as np
import app.utilities.guiutils as guiutils

class GridGraph(GraphicsView):
    """ A virtual representation of the *field generator board* displaying the grid of test points used during calibration"""
    def __init__(self):
        super().__init__()
        viewbox = ViewBox()
        self.graph = GridItem()
        viewbox.setAspectLocked()
        viewbox.addItem(self.graph)
        self.setBackground('w')
        self.setCentralItem(viewbox)


class GridItem(GraphItem):
    """ Subclass of GridGraph """
    def __init__(self):
        self.x, self.y = guiutils.get_board_dimensions()
        self.num_points = self.x * self.y
        self.textItems = []
        GraphItem.__init__(self)
        self.currentPosition = 1
        self.completedColor = [0, 153, 51]
        self.currentColor = [0, 102, 255]
        self.uncompletedColor = [153, 51, 51]
        self.calibratedColor = [102, 102, 255]

        self.text = ["%d" % i for i in range(1, self.num_points+1)]
        self.symbols = ['o'] * self.num_points
        self.pos = []
        self.colours = [self.uncompletedColor] * self.num_points
        self.generatePos()
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def generatePos(self):
        """Generates the positions for the grid of test points"""
        self.pos = np.zeros((self.num_points, 2), dtype='int32')
        self.pos[:, 1] = np.repeat(list(reversed(np.arange(1, self.x*2, 2))), self.y)
        self.pos[:, 0] = np.tile(np.arange(1, self.x*2, 2), self.y)

    def moveToPosition(self, pos):
        """Changes the colours of the test points (current=blue, captured=green, uncaptured=red)

        :param pos: the given test point number
        """
        if pos != 1:
            prevPos = pos - 1
            self.setPointColor(prevPos, self.completedColor)
        if pos != self.num_points+1:
            self.setPointColor(pos, self.currentColor)

    def flash(self):
        """ Changes the colours of all test points (indicating the calibration procedure has finished)"""
        self.colours = [self.calibratedColor]* self.num_points
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def resetGraph(self):
        """ Resets the colours of all test points """
        self.colours = [self.uncompletedColor] * self.num_points
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def setPointColor(self, pointNo, colour):
        """ Sets the colour for a single test point

        :param pointNo: the given test point number
        :param colour: the given colour
        """
        self.colours[pointNo - 1] = colour
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def setData(self, **kwds):
        """ Creates the grid of circular test points """
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()

    def setTexts(self, text):
        """ Generates the text (number) associated with each test point

        :param text: the numbers of all test points
        """
        for i in self.textItems:
            try:
                i.scene().removeItem(i)
            except Exception as e:
                pass
        self.textItems = []
        for t in text:
            item = TextItem(t)
            item.setColor([255, 255, 255])
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):
        """ Refreshes/redraws the grid of test points """
        GraphItem.setData(self, **self.data)
        for i, item in enumerate(self.textItems):
            pos = self.data['pos'][i] + [-.3, .3]
            #item.setPos(*self.data['pos'][i])
            item.setPos(*pos)
