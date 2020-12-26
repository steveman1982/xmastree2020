from simtree import Simtree


def xmaslight():
    debug = False
    # This is the code from my

    #NOTE THE LEDS ARE GRB COLOUR (NOT RGB)

    # Here are the libraries I am currently using:
    import time

    import re
    import math

    # You are welcome to add any of these:
    import random
    # import numpy
    # import scipy
    # import sys

    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])

    # IMPORT THE COORDINATES (please don't break this bit)

    coordfilename = "coords.txt"

    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()

    coords_bits = [i.split(",") for i in coords_raw]

    coords = []

    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)

    simtree = Simtree(coords)

    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500

    pixels = []
    for _ in coords:
        # init lights off
        pixels.append([0, 0, 0])

    # YOU CAN EDIT FROM HERE DOWN
    slow = 0     # pause between cycles (normally zero as it is already quite slow)
    orbAm = 15      # amount of orbs
    orbMaxRadius = 250
    orbBrightness = 0.7
    orbSpd = 80
    bouncePow = 30  # " push" amount when orbs moves out of range

    import colorsys

    xs = []
    ys = []
    zs = []
    for i in coords:
        xs.append(i[0])
        ys.append(i[1])
        zs.append(i[2])
    dimensions = [[min(xs), max(xs)], [min(ys), max(ys)], [min(zs), max(zs)]]

    pixelRGBs = []
    for i in range(PIXEL_COUNT):
        pixelRGBs.append([0, 0, 0])

    def resetPixels():
        for i in range(len(pixelRGBs)):
            pixelRGBs[i] = [0, 0, 0]

    currTime = time.time()
    dt = 0
    lastCalc = currTime

    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))

    def isInDimensions(val, dims):
        if val[0] < dims[0][0]:
            return False
        if val[0] > dims[0][1]:
            return False
        if val[1] < dims[1][0]:
            return False
        if val[1] > dims[1][1]:
            return False
        if val[2] < dims[2][0]:
            return False
        if val[2] > dims[2][1]:
            return False
        return True

    class orb:
        def __init__(self, radius, spd, hue, bri):
            self.radius = radius
            self.hue = hue
            self.bri = bri
            self.xPos = random.uniform(dimensions[0][0], dimensions[0][1])
            self.yPos = random.uniform(dimensions[1][0], dimensions[1][1])
            self.zPos = random.uniform(dimensions[2][0], dimensions[2][1])
            self.xSpd = random.uniform(-spd, spd)
            self.ySpd = random.uniform(-spd, spd)
            self.zSpd = random.uniform(-spd, spd)

        def move(self):
            self.hue += 5 * dt
            if self.hue >= 360:
                self.hue -= 360

            self.xPos += self.xSpd * dt
            self.yPos += self.ySpd * dt
            self.zPos += self.zSpd * dt

            if self.xPos < dimensions[0][0]:
                self.xSpd += bouncePow * dt
            elif self.xPos > dimensions[0][1]:
                self.xSpd -= bouncePow * dt

            if self.yPos < dimensions[1][0]:
                self.ySpd += bouncePow * dt
            elif self.yPos > dimensions[1][1]:
                self.ySpd -= bouncePow * dt

            if self.zPos < dimensions[2][0]:
                self.zSpd += bouncePow * dt
            elif self.zPos > dimensions[2][1]:
                self.zSpd -= bouncePow * dt

        def render(self):
            x1 = constrain(self.xPos - self.radius,
                           dimensions[0][0], dimensions[0][1])
            x2 = constrain(self.xPos + self.radius,
                           dimensions[0][0], dimensions[0][1])
            y1 = constrain(self.yPos - self.radius,
                           dimensions[1][0], dimensions[1][1])
            y2 = constrain(self.yPos + self.radius,
                           dimensions[1][0], dimensions[1][1])
            z1 = constrain(self.zPos - self.radius,
                           dimensions[2][0], dimensions[2][1])
            z2 = constrain(self.zPos + self.radius,
                           dimensions[2][0], dimensions[2][1])
            orbDimensions = [[x1, x2], [y1, y2], [z1, z2]]

            # print("")
            # print("{:.2f}".format(self.xPos),"{:.2f}".format(self.yPos),"{:.2f}".format(self.zPos))
            for i in range(PIXEL_COUNT):
                led = coords[i]
                if not isInDimensions(led, orbDimensions):
                    continue

                dist = math.sqrt(
                    ((self.xPos-led[0])**2)+((self.yPos-led[1])**2)+((self.zPos-led[2])**2))
                bri = self.radius - dist
                bri = bri / self.radius
                if bri <= 0:
                    continue

                col = colorsys.hsv_to_rgb(self.hue/360, 1, bri*self.bri)
                col = [element * 255 for element in col]
                pixelRGBs[i] = [min(255, pixelRGBs[i][0]+col[0]), min(255, pixelRGBs[i][1]+col[1]), min(255, pixelRGBs[i][2]+col[2])]


    orbs = []
    for i in range(orbAm):
        orbs.append(orb(random.uniform(orbMaxRadius*0.3, orbMaxRadius), orbSpd, (i*137.508) % 360, orbBrightness))

    # yes, I just run which run is true
    run = 1
    while run == 1:

        time.sleep(slow)

        currTime = time.time()
        dt = (currTime - lastCalc)  # calculate factor for variable framerate compensation
        lastCalc = currTime

        resetPixels()
        for orb in orbs:
            orb.move()
        for orb in orbs:
            orb.render()

        if not debug:
            for i in range(PIXEL_COUNT):
                pixels[i] = pixelRGBs[i]
            # pixels.show()

        # print a quickndirty visualization for debugging
        if debug:
            pixStr = ""
            for i in range(PIXEL_COUNT):
                pixStr += "{:.0f}".format(pixelRGBs[i][0]).zfill(3)+","
            print(pixStr)

        simtree.update(pixels)
    return 'DONE'


# yes, I just put this at the bottom so it auto runs
xmaslight()