from math import dist

class Pkt():
    def __init__(self, endpoints, lightModel, plnp, time, timeStart, protocol):
        self.endpoints = endpoints
        self.lightModel = lightModel
        self.plnp = plnp
        self.currPos = endpoints[0]
        self.counter = 0
        self.time = time
        self.timeStart = timeStart
        self.protocol = protocol

        self.setup()
        
        #self.path = self.calcPath()

    def setup(self):
        start = self.endpoints[0]
        end = self.endpoints[1]
        
        xi = start[0]
        xf = end[0]

        yi = start[1]
        yf = end[1]

        self.delta = self.time*75

        self.inc_x = (xf-xi)/(self.delta)
        self.inc_y = (yf-yi)/(self.delta)

        #print(self.inc_x, self.inc_y)

    # This functions calculates the full path of the packet
    def trajetoria(self):
        start = self.endpoints[0]
        end = self.endpoints[1]
        xi = start[0]
        xf = end[0]

        yi = start[1]
        yf = end[1]

        delta = self.time*75

        inc_x = (xf-xi)/(delta)
        inc_y = (yf-yi)/(delta)

        print(inc_x, inc_y)

        points = []
        cp = start

        for _ in range(delta):
            cp = (cp[0] + inc_x, cp[1] + inc_y)
            points.append(cp)

        return points

    # Returns the next position
    def nextPos(self):

        if self.counter < self.delta:
            self.currPos = (self.currPos[0] + self.inc_x, self.currPos[1] + self.inc_y)
            self.counter += 1
        else:
            self.currPos = None
        
        return self.currPos