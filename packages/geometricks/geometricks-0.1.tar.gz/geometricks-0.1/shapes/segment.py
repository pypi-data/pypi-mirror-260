from point import Point
import math


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        

    def get_coord(self):
        return (self.p1.x, self.p1.y, self.p2.x, self.p2.y)

    def getDistance(self, point):
        # get the distance between a point and a segment
        x1, y1, x2, y2 = get_coord(self)

        x, y = point.x, point.y
        dx = x2 - x1
        dy = y2 - y1
        if dx == dy == 0:  #from getClosest.getClosestPolygon import point_plus_proche_polygone If points p1 and p2 are the same
                return math.sqrt((x - x1)**2 + (y - y1)**2)
        t = ((x - x1) * dx + (y - y1) * dy) / (dx**2 + dy**2)
        t = max(0, min(1, t))  # Limit t between 0 and 1 to be on the segment
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.sqrt((x - proj_x)**2 + (y - proj_y)**2)
    