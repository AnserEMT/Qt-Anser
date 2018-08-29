from pyqtgraph import GraphicsView, GraphItem, TextItem, ViewBox
from PyQt5.QtCore import Qt, pyqtSlot
import numpy as np


class GridGraph(GraphicsView):
    '''
    A virtual representation of the field generator board used during calibration.
    '''
    def __init__(self):
        super().__init__()
        viewbox = ViewBox()
        self.graph = GridItem()
        viewbox.setAspectLocked()
        viewbox.addItem(self.graph)
        self.setBackground('w')
        self.setCentralItem(viewbox)


class GridItem(GraphItem):
    def __init__(self):
        self.x = 7
        self.y = 7
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
        self.pos = np.zeros((self.num_points, 2), dtype='int32')
        self.pos[:, 1] = np.repeat(list(reversed(np.arange(1, self.x*2, 2))), self.y)
        self.pos[:, 0] = np.tile(np.arange(1, self.x*2, 2), self.y)

    def moveToPosition(self, pos):
        if pos != 1:
            prevPos = pos - 1
            self.setPointColor(prevPos, self.completedColor)
        if pos != self.num_points+1:
            self.setPointColor(pos, self.currentColor)

    def flash(self):
        self.colours = [self.calibratedColor]* self.num_points
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def resetGraph(self):
        self.colours = [self.uncompletedColor] * self.num_points
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def setPointColor(self, pointNo, colour):
        self.colours[pointNo - 1] = colour
        self.setData(pos=self.pos, symbolBrush=self.colours, size=1, symbol=self.symbols, pxMode=False, text=self.text)

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()

    def setTexts(self, text):
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
        GraphItem.setData(self, **self.data)
        for i, item in enumerate(self.textItems):
            pos = self.data['pos'][i] + [-.3, .3]
            #item.setPos(*self.data['pos'][i])
            item.setPos(*pos)
