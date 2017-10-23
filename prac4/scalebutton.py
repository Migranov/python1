import tkinter


class ScaleButton:
    def __init__(self, parent, matPlot, text):
        def act():
            if text == "+":
                matPlot.scaleAxes(2 / 3)
            else:
                matPlot.scaleAxes(1.5)
        a = tkinter.Button(parent, text=text, font=1, command=act, height=10, width=10)
        a.pack(side="right")