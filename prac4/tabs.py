from tkinter import ttk
import tkinter
from tkinter.colorchooser import *
import xml.etree.cElementTree as et
import scipy.integrate
import numpy as np


class Tabs:
    def setXY(self, x, y):
        self.text1.delete(1.0, tkinter.END)
        self.text2.delete(1.0, tkinter.END)
        self.text1.insert(tkinter.INSERT, x)
        self.text2.insert(tkinter.INSERT, y)

    def getColor(self):
        color = (0, 0, 0)
        if self.color[0] != 0:
            color = (self.color[0][0]/255, self.color[0][1]/255, self.color[0][2]/255)
        return color

    def getRadius(self):
        return self.w.get()

    def saveFile(self):
        root = et.Element("root")
        axes = et.SubElement(root, "axes")
        xlim = et.SubElement(axes, "xlim")
        xmax = et.SubElement(axes, "xmax")
        ylim = et.SubElement(axes, "ylim")
        ymax = et.SubElement(axes, "ymax")
        currentAxes = self.mo.getCurrentAxes()
        xlim.text = str(currentAxes[0][0])
        xmax.text = str(currentAxes[0][1])
        ylim.text = str(currentAxes[1][0])
        ymax.text = str(currentAxes[1][1])
        color = et.SubElement(root, "color")
        r = et.SubElement(color, "r")
        g = et.SubElement(color, "g")
        b = et.SubElement(color, "b")
        c = (0, 0, 0)
        if self.color[0] != 0:
            c = (self.color[0][0] / 255, self.color[0][1] / 255, self.color[0][2] / 255)
        r.text = str(c[0])
        g.text = str(c[1])
        b.text = str(c[2])
        slider = et.SubElement(root, "slider")
        slider.text = str(self.w.get())
        circles = et.SubElement(root, "circles")
        circleList = self.mo.getCircleList()
        if len(circleList) != 0:
            for i in range(len(circleList)):
                circle = circleList[i]
                cir = et.SubElement(circles, "circle")
                x = et.SubElement(cir, "x")
                x.text = str(circle[0][0])
                y = et.SubElement(cir, "y")
                y.text = str(circle[0][1])
                radius = et.SubElement(cir, "radius")
                radius.text = str(circle[1])
                rcircle = et.SubElement(cir, "r")
                rcircle.text = str(circle[2][0])
                gcircle = et.SubElement(cir, "g")
                gcircle.text = str(circle[2][1])
                bcircle = et.SubElement(cir, "b")
                bcircle.text = str(circle[2][2])
        tree = et.ElementTree(root)
        tree.write(self.savefiledialog.get(1.0, tkinter.END)+".xml")

    def loadFile(self):
        tree = et.parse(self.openfiledialog.get(1.0, tkinter.END)+'.xml')
        root = tree.getroot()
        xlim = float(root[0][0].text)
        xmax = float(root[0][1].text)
        ylim = float(root[0][2].text)
        ymax = float(root[0][3].text)
        color = (float(root[1][0].text), float(root[1][1].text), float(root[1][2].text))
        self.defaultColor = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
        slider = float(root[2].text)
        circles = root.find('circles')
        circleList = []
        for circle in circles.findall('circle'):
            circleList.append(((float(circle[0].text), float(circle[1].text)), float(circle[2].text), (float(circle[3].text), float(circle[4].text), float(circle[5].text))))
        self.w.set(slider)
        self.mo.loadFromXml((xlim, xmax, ylim, ymax), circleList)

    def verlet(self):
        #for example: r1(0), r2(0), r3(0), v1(0), v2(0), v3(0)
        init = sum([list(map(float, self.text6.get(1.0, tkinter.END).split(" "))),
                    list(map(float, self.text7.get(1.0, tkinter.END).split(" ")))], [])
        m = list(map(float, self.text5.get(1.0, tkinter.END).split(" ")))
        n = int(self.text4.get(1.0, tkinter.END))
        G = 6.674
        t = np.linspace(0, 3, 300)
        dt = 3.0/300
        r = []
        for i in range(n):
            r.append(init[i])
        v = []
        for i in range(n):
            v.append(init[i+n])
        am = []
        for i in range(n):
            a = 0
            for f in range(n):
                if f!=i:
                    a+=m[f]*G*(r[f]-r[i])/abs(r[f]-r[i])**3
            am.append(a)
        for i in range(len(t)):
            if i != 0:
                for j in range(n):
                    a = 0
                    for f in range(n):
                        if f != j:
                            a += m[f]*G*(r[(i-1)*n+f]-r[(i-1)*n+j])/abs(r[(i-1)*n+f]-r[(i-1)*n+j])**3
                    am.append(a)
                    r.append(r[(i-1)*n+j] + v[(i-1)*n+j]*dt + 1.0/2*am[(i-1)*n+j]*(dt)**2)
                    v.append(v[(k - 1) * n + j] + 1.0 / 2 * dt * (a + am[(i-1)*n+j]))
        print(len(r),r)
        print(len(v),v)

    def scipySolve(self, init, x, n, m):
        G = 6.674
        r0 = []
        for i in range(n):
            r0.append(init[i])
        v0 = []
        for i in range(n):
            v0.append(init[i + n])
        result = []
        for i in range(n):
            result.append(v0[i])
            sum = 0
            for k in range(n-1):
                if k != i:
                    sum += G * m[k] * (r0[k] - r0[i])/abs((r0[k] - r0[i])**3)
            result.append(sum)
        return result


    def scipy(self):
        # for example: m1, m2, m3, r1(0), r2(0), r3(0), v1(0), v2(0), v3(0)
        init = sum([list(map(float, self.text6.get(1.0, tkinter.END).split(" "))), list(map(float, self.text7.get(1.0, tkinter.END).split(" ")))], [])
        t = np.linspace(0, 3, 300)
        result = scipy.integrate.odeint(self.scipySolve, init, t, args=(int(self.text4.get(1.0, tkinter.END)),
                                                                        list(map(float,
                                                                                 self.text5.get(1.0, tkinter.END).split(
                                                                                     " ")))))
        print(result)

    def verletThreading(self):
        print("verlet-threading")

    def verletMultipricessing(self):
        print("verlet-multiprocessing")

    def verletCython(self):
        print("verlet-cython")

    def verletOpencl(self):
        print("verlet-opencl")

    def __init__(self, root, mo):
        style = ttk.Style()
        self.mo = mo
        style.configure("TNotebook.Tab", background='gray', foreground="black", font=1)
        nb = ttk.Notebook(root)
        page1 = ttk.Frame(nb, height=150, width=50)
        self.text1 = tkinter.Text(page1, height=1, width=50)
        self.text1.pack()
        self.text2 = tkinter.Text(page1, height=1, width=50)
        self.text2.pack()
        self.defaultColor = (0, 0, 0)
        self.color = (0, 0, 0)

        #color
        def getColor():
            color = askcolor(self.defaultColor)
            self.color = color
            if color[0] is not None:
                self.defaultColor = (int(color[0][0]), int(color[0][1]), int(color[0][2]))

        tkinter.Button(page1, text='Select Color', command=getColor).pack(side='left')

        #slider
        def setText(value):
            self.text3.delete(1.0, tkinter.END)
            self.text3.insert(tkinter.INSERT, value)

        self.w = tkinter.Scale(page1, from_=1.0, to=100.0, orient=tkinter.HORIZONTAL, command=setText)
        self.w.pack(side='right')

        def setValue():
            self.w.set(self.text3.get(1.0, tkinter.END))
        tkinter.Button(page1, text='Set Slider', command=setValue).pack(side='right')

        self.text3 = tkinter.Text(page1, height=1, width=5)
        self.text3.pack(side='right')

        #radiobuttons
        page2 = ttk.Frame(nb)
        self.chooseRadiobutton = -1
        MODES = [
            ("scipy", "1"),
            ("verlet", "2"),
            ("verlet-threading", "3"),
            ("verlet-multiprocessing", "4"),
            ("verlet-cython", "5"),
            ("verlet-opencl", "6")
        ]
        options = {1: self.scipy,
                   2: self.verlet,
                   3: self.verletThreading,
                   4: self.verletMultipricessing,
                   5: self.verletCython,
                   6: self.verletOpencl,
        }
        v = tkinter.StringVar()
        v.set("L")  # initialize
        for text, mode in MODES:
            def command(mode=mode, text=text):
                self.chooseRadiobutton = mode
                options[int(mode)]()
            b = tkinter.Radiobutton(page2, text=text,
                            variable=v, value=mode, command=command)
            b.pack(anchor=tkinter.W)

        self.text4 = tkinter.Text(page2, height=1, width=20)
        self.text4.pack()
        self.text5 = tkinter.Text(page2, height=1, width=20)
        self.text5.pack()
        self.text6 = tkinter.Text(page2, height=1, width=20)
        self.text6.pack()
        self.text7 = tkinter.Text(page2, height=1, width=20)
        self.text7.pack()

        # xml-file
        page3 = ttk.Frame(nb)
        self.savefiledialog = tkinter.Text(page3, height=1, width=50)
        self.savefiledialog.pack()
        tkinter.Button(page3, text='save file', command=self.saveFile).pack()
        self.openfiledialog = tkinter.Text(page3, height=1, width=50)
        self.openfiledialog.pack()
        tkinter.Button(page3, text='load file', command=self.loadFile).pack()

        nb.add(page1, text='Edit')
        nb.add(page2, text='Model')
        nb.add(page3, text='Load/Save')
        nb.pack(side='left')