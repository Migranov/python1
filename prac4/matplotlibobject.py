import tkinter
import numpy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MatplotlibObject():
    def getAxes(self):
        return self.axes

    def getCanvas(self):
        return self.canvas

    def getCurrentAxes(self):
        return (self.axes.get_xlim(), self.axes.get_ylim())

    def getCircleList(self):
        return self.circleList

    def loadFromXml(self, xy, circleList):
        self.axes.clear()
        self.axes.set_xlim(xy[0], xy[1])
        self.axes.set_ylim(xy[2], xy[3])
        for i in range(len(circleList)):
            self.drawCircle(circleList[i][0], circleList[i][1], circleList[i][2])
        self.canvas.show()


    def scaleAxes(self, scale):
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        self.axes.clear()
        self.axes.set_xlim(xlim[0] * scale, xlim[1] * scale)
        self.axes.set_ylim(ylim[0] * scale, ylim[1] * scale)
        if len(self.circleList) != 0:
            for i in range(len(self.circleList)):
                self.drawCircle(self.circleList[i][0], self.circleList[i][1], self.circleList[i][2])
        self.canvas.show()

    def drawCircle(self, xy, r, color):
        self.curXY = xy
        self.curR = r
        self.curColor = color

        circle = matplotlib.patches.Circle(xy=self.curXY, radius=self.curR,
                                          fill=True,
                                          visible=True,
                                          color=self.curColor)
        self.circleList.append((self.curXY, self.curR, self.curColor))
        self.axes.add_patch(circle)
        self.canvas.show()

    def __init__(self, parent):
        self.circleList = []
        self.curXY = (0, 0)
        self.curR = 1
        self.curColor = (0, 0, 0)

        self.figure = Figure(figsize=(5, 5))
        self.axes = self.figure.add_subplot(111, xlim=[-100, 100], ylim=[-100, 100])

        self.canvas = FigureCanvasTkAgg(self.figure, parent)

        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)