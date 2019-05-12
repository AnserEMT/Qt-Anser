""" Displays sensor positions in real time """
import pyqtgraph.opengl as gl
import numpy as np
import utils.utils as utils
from stl import mesh
MAX_NUM_OF_SENSORS = 4


class PositionGraph(gl.GLViewWidget):
    """
    Displays sensor positions and a 3D model of the field generator board.
    """
    def __init__(self):
        super(PositionGraph, self).__init__()
        self.setWindowTitle('Anser Position')
        self.setBackgroundColor('w')
        # Import the STL of the transmitter board and transform it into a mesh item
        anser_mesh = mesh.Mesh.from_file(utils.resource_path('./app/resources/cad/mesh.stl'))
        anser_mesh = gl.MeshData(vertexes=anser_mesh.vectors)
        # re-center the transmitter board mesh item in the position graph
        m = gl.GLMeshItem(meshdata=anser_mesh, shader='shaded', color=(0,1,0,0.1))
        m.rotate(135, 0, 0, 1)
        m.translate(240, 0, -240)
        m.scale(1, 1, 1)
        self.addItem(m)
        # create a virtual grid representing the transmitter board
        gx = gl.GLGridItem()
        gx.setSize(7, 7, 7)
        gx.scale(45,45,45)
        gx.rotate(45,0,0,1)
        #self.addItem(gx)
        self.pos = np.empty((MAX_NUM_OF_SENSORS, 3))
        self.color = np.empty((MAX_NUM_OF_SENSORS, 4))
        size = np.empty(MAX_NUM_OF_SENSORS)
        for i in range(MAX_NUM_OF_SENSORS):
            self.pos[i] = (0, 0, 0)
            self.color[i] = (0, 0.0, 0.0, 0.0)
            size[i] = 8
        # create the 3D visualisation graph
        self.sp1 = gl.GLScatterPlotItem(pos=self.pos, size=size, color=self.color[0], pxMode=True)
        self.sp1.setGLOptions('translucent')
        self.addItem(self.sp1)
        # recenter camera position
        self.setCameraPosition(100, 800, 30)
        self.sp1.rotate(135,0,0,1)

    def updateGraph(self, positions):
        """ Draws a circle indicating the positions for each of the sensors

        :param positions: the given list of sensor positions
        """
        numSensors = len(positions)
        for i in range(numSensors):
            self.pos[i] = (positions[i][0], positions[i][1], positions[i][2])
            self.color[i] = (1, 0.0, 0.0, 1)
        self.sp1.setData(pos=self.pos, color=self.color, pxMode=True)


    def clearGraph(self):
        """ Clears the position graph """
        # no way to clear ScatterPlotItem - just hide points
        for i in range(MAX_NUM_OF_SENSORS):
            self.pos[i] = (0,0,0)
            self.color[i] = (1, 0.0, 0.0, 0.0)
        self.sp1.setData(pos=self.pos, color=self.color)
