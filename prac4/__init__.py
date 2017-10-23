import tkinter
from lesson4.program1.cursor import Cursor
from lesson4.program1.matplotlibobject import MatplotlibObject
from lesson4.program1.scalebutton import ScaleButton
from lesson4.program1.tabs import Tabs

if __name__ == "__main__":
    root = tkinter.Tk()

    mo = MatplotlibObject(root)
    cursor = Cursor(mo, 'spyAxes')
    scb1 = ScaleButton(root, mo, "-")
    scb2 = ScaleButton(root, mo, "+")
    tabs = Tabs(root, mo)
    cursor.setTabs(tabs)

    root.mainloop()