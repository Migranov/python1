class Cursor(object):

    def __init__(self, mo, name):
        self.ax = mo.getAxes()
        self.name = name
        mo.getCanvas().mpl_connect('motion_notify_event', self)

        def callback(event):
            mo.drawCircle((event.xdata, event.ydata), self.tabs.getRadius(), self.tabs.getColor())
        mo.getCanvas().mpl_connect('button_press_event', callback)

    def __call__(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            self.tabs.setXY(x, y)

    def setTabs(self, tabs):
        self.tabs = tabs