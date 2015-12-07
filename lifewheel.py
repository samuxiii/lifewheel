import Tkinter as tk

class LifeWheel (tk.Frame):

    def __init__(self, parent, numPieSlices):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=400,  height=400, background="bisque")
        self.canvas.pack(fill="both", expand=True)
        self.numPieSlices = numPieSlices

        extent = 360.0 / numPieSlices #portion in grades (real)
        levels = 1

        for i in range(0, numPieSlices):
            bbox = (100,100,300,300) #bbox = bouncing box
            PieSlice(bbox, i, extent, levels).draw(self.canvas)


class PieSlice (object):

    def __init__(self, bbox, position, extent, levels):
        print "\nInit PieSlice %d" % (position)
        self.bbox = bbox
        self.position = position
        self.extent = extent
        self.levels = levels
        self.name = "pieslice" + str(position)
        self.slices = []

    def draw(self, canvas):
        start = self.position * self.extent
        #TODO: refactor loop to allow several levels
        #      now this is not working properly
        for i in range(0, self.levels):
            sliceName = self.name + "slice" + str(i)
            self.slices.append(Slice(self.bbox, start, self.extent, sliceName))
            item = self.slices[i].draw(canvas)
            canvas.tag_bind(item, "<1>", self.slices[i].mouse_click)


class Slice (object):
    def __init__(self, bbox, start, extent, name=None):
        print "Init Slice %s" % (name)
        self.coords = bbox
        self.start = start
        self.extent = extent
        self.name = name
        self.green = False

    def draw(self, canvas, outline="black", fill="white"):
        return canvas.create_arc(self.coords, start=self.start, extent=self.extent, tags=self.name, outline=outline, fill=fill)

    def mouse_click(self, event):
        print "I got a mouse click (%s)" % self.name
        if self.green:
                self.green = False
                event.widget.itemconfig(self.name, fill="blue") #change color
        else:
                self.green = True
                event.widget.itemconfig(self.name, fill="green")


if __name__ == "__main__":
    root = tk.Tk()
    LifeWheel(root,7).pack(fill="both", expand=True)
    root.mainloop()

