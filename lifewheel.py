import Tkinter as tk
import math

class LifeWheel (tk.Frame):

    def __init__(self, parent, labels):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=400,  height=400, background="gray")
        self.canvas.pack(fill="both", expand=True)
        self.numPieSlices = len(labels)

        #constants
        extent = 360.0 / self.numPieSlices #portion in grades (real)
        levels = 10
        bbox = (100,100,500,500) #bbox = square bouncing box
        colors = ["pink", "red", "yellow", "blue", "cyan", "green", "magenta", "orange", "brown", "gray"]

        for i in range(0, self.numPieSlices):
            c = ((len(colors) + i) % len(colors)) -1  #select the color
            PieSlice(bbox, i, extent, levels, labels[i], colors[c]).draw(self.canvas)


class PieSlice (object):

    def __init__(self, bbox, position, extent, levels, label, color):
        print "\nInit PieSlice %d" % (position)
        self.bbox = bbox
        self.position = position
        self.extent = extent
        self.levels = levels
        self.name = label.replace(" ","").replace("\n","") #remove spaces/newlines
        self.label = label
        self.color = color
        self.slices = []

    def draw(self, canvas):
        start = self.position * self.extent
        x0,y0,x1,y1 = self.bbox

        #offset to resize the bbox according to the levels
        offsetX = (x1 - x0)/(2 * self.levels)
        offsetY = (y1 - y0)/(2 * self.levels)

        #creating slice levels into the pieslice
        for i in range(0, self.levels):
            sliceName = self.name + "slice" + str(i)
            #(i == 0) doesn't need to recalculate with offsets
            if (i > 0):
                x0 += offsetX
                y0 += offsetY
                x1 -= offsetX
                y1 -= offsetY

            tempBbox = x0, y0, x1, y1

            print "Coord slice: %s" % (tempBbox,)
            self.slices.append(Slice(tempBbox, start, self.extent, sliceName, level=i, color=self.color))
            self.slices[i].draw(canvas)
            self.slices[i].registerNotifier(self.turnOnLevel)

        #write pie slice text
        self.writeText(canvas, self.label)

    def turnOnLevel(self, canvas, level):
        #levels are inverted... center is 9, external area is 0
        for i in range(0, self.levels):
            self.slices[i].turnOff(canvas)
        for i in range(level, self.levels):
            self.slices[i].turnOn(canvas)

    def writeText(self, canvas, text):
        #calculating the (x,y) coordinates where to set the text
        #surrounding circumference over the pieslice
        x0,y0,x1,y1 = self.bbox
        xcenter = (x1 - x0)/2 + x0
        ycenter = (y1 - y0)/2 + y0
        #
        radius = xcenter - x0 + (x0/2) # (x0/2) pixels bigger than the slice radius
        alpha_degrees = (self.extent/2) + self.position * self.extent
        alpha_radians = (math.pi * alpha_degrees) / 180.0
        xrelative = radius * math.cos(alpha_radians)
        yrelative = radius * math.sin(alpha_radians)
        print "r:%d, ar:%.2f, xr:%d, yr:%d" % (radius, alpha_radians, xrelative, yrelative)
        #
        x = xcenter + xrelative
        y = ycenter + yrelative * (-1) # yrelative is reversed
        print "text(%d,%d)" % (x, y)
        canvas.create_text(x, y, text=text)


class Slice (object):
    def __init__(self, bbox, start, extent, name, level, color="blue"):
        print "Init Slice %s" % (name)
        self.coords = bbox
        self.start = start
        self.extent = extent
        self.name = name
        self.level = level
        self.color = color
        self.notifier = None #reference to parent method

    def draw(self, canvas, outline="black", fill="white"):
        item = canvas.create_arc(self.coords, start=self.start, extent=self.extent, tags=self.name, outline=outline, fill=fill)
        canvas.tag_bind(item, "<1>", self.mouse_click)

    def mouse_click(self, event):
        print "I got a mouse click (%s)" % self.name
        #call to notifier() == PieSlice.turnOnLevel(canvas, level)
        self.notifier(event.widget, self.level)

    def registerNotifier(self, func):
        #this function will be use to notify parent PieSlice object
        self.notifier = func 

    def turnOn(self, canvas):
        self.green = False
        canvas.itemconfig(self.name, fill=self.color)

    def turnOff(self, canvas):
        self.green = True
        canvas.itemconfig(self.name, fill="white")


if __name__ == "__main__":
    root = tk.Tk()
    labels = ["Finances", "Career", "Health", "Spirituality", "Community", "Physical\nEnvironment", "Fun", "Friends", "Family", "Partner/Lover"]
    LifeWheel(root, labels).pack(fill="both", expand=True)
    root.mainloop()

