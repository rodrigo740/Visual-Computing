from math import dist

class Pkt():
    def __init__(self, endpoints, lightModel, plnp, time):
        self.endpoints = endpoints
        self.lightModel = lightModel
        self.plnp = plnp
        self.currPos = endpoints[0]
        self.i = -1
        self.time = time
        self.path = self.calcPath()


    """
    This function calculates the sequence of coordinates the packet will take, taking into account the time and velocity.
    There are 3 cases:
        - straight vertical path (x remains the same, e.g. x=3)
        - straight horizontal path (y remains the same, e.g. y=3)
        - path that can be modeled by y=mx+b
    
    time = delay measured in the capture
    velocity is calculated following the quation v=d/t, with d = distance between the start and end point (assuming a straight line) and t = time

    return the list of coordinates calculated.
    """
    def calcPath(self):

        start = self.endpoints[0]
        end = self.endpoints[1]

        totalD = dist(start, end)
        v = totalD/self.time
        points = [start]

        # Case 1, straight vertical path
        if start[0] == end[0]:
            print("Case 1: Vertical path - x = " + str(start[0]) + " , totalD = " + str(totalD))
            y1 = start[1]
            y2 = end[1]
            t = 1/75
            d = v*t
            cd = 0
            k = 1
            if y1 > y2:
                k = -1
            rd = k * d
            while(cd < totalD):
                for _ in range(75):
                    cd += d
                    points.append((points[-1][0], points[-1][1] + rd))
                    if cd >= totalD: break
        # Case 1, straight horizontal path
        elif start[1] == end[1]:
            print("Case 2: Horizontal path - y = " + str(start[1]) + " , totalD = " + str(totalD))
            x1 = start[0]
            x2 = end[0]
            t = 1/75
            d = v*t
            cd = 0
            k = 1
            if x1 > x2:
                k = -1
            rd = k * d
            while(cd < totalD):
                for _ in range(75):
                    cd += d
                    points.append((points[-1][0] + rd, points[-1][1]))
                    if cd >= totalD: break
        # Case 3, y=mx+b path
        elif (start[0] != end[0]) and (start[1] != end[1]):
            # m = (y2-y1)/(x2-x1)
            m = (end[1] - start[1])/(end[0] - start[0])
            # b = y-mx
            b = end[1] - m * end[0]

            x1 = start[0]
            x2 = end[0]
            t = 1/75
            d = v*t
            cd = 0
            k = 1
            if m < 0:
                k = -1
            rd = k * d
            while(cd < totalD):
                for _ in range(75):
                    cd += d
                    x = points[-1][0] + rd
                    #print(x)
                    points.append((x, m * x + b))
                    if cd >= totalD: break
                    elif x >= end[0]: 
                        cd = totalD
                        break
            print("Case 3: y=mx+b path - y = " + str(m) + "x + " + str(b) + " , totalD = " + str(totalD))
        else:
            print("Not a valid path!, exiting....")
            exit(1)

        #print(points[-1])
        #print(totalD)
        #print(self.endpoints)
        #print(len(points))

        return points

    def nextPos(self):
        """
        self.currPos = (self.currPos[0], self.currPos[1]+self.i)
        #print("Paths: " + str(self.path))
        
        if (self.currPos[0] > self.endpoints[1][0]) or (self.currPos[1] < self.endpoints[1][1]):
            self.i = 1
        if (self.currPos[0] > self.endpoints[1][0]) or (self.currPos[1] > self.endpoints[0][1]):
            self.i = -1

        if self.currPos[1] < self.endpoints[1][1]:
            self.i = 1

        #if self.currPos[1] > 350:
        #    self.i = -1
        #if self.currPos[1] < 280:
        #    self.i = 1
        #print(self.currPos)
        """
        if len(self.path) != 0:
            nextPos = self.path.pop(0)
        else:
            nextPos = None
        #print(nextPos)
        return nextPos