import math
from point import Point
from segment import Segment

class Circle:
    def __init__(self, p1, r):
        self.centre = p1
        self.rayon = r

    def get_coord(self):
        return (self.centre.x, self.centre.y)

    def getDistance(self, point):
        # Distance entre le centre du cercle et le point
        distance = math.sqrt((self.centre.x - point.x) ** 2 + (self.centre.y - point.y) ** 2)
        # Distance est la différence entre le rayon et la distance
        distance = abs(distance - self.rayon)
        return distance

    def getDistance(self, droite):
        # Calcul de la distance entre le centre du cercle et la droite
        distance = abs((droite.p1.y - droite.p2.y) * self.centre.x + (droite.p2.x - droite.p1.x) * self.centre.y + (droite.p1.x * droite.p2.y - droite.p2.x * droite.p1.y)) / math.sqrt((droite.p2.x - droite.p1.x) ** 2 + (droite.p2.y - droite.p1.y) ** 2)
        distance = abs(distance - self.rayon)
        return distance

    def getDistance(self, segment):
        # Calcul de la distance entre le centre du cercle et le segment
        AB = segment.p2.x - segment.p1.x
        AC = segment.p2.y - segment.p1.y
        BC = math.sqrt(AB ** 2 + AC ** 2)
        # Calcul de la distance entre le centre et le point projeté sur la droite du segment
        distance = abs((AC * self.centre.x - AB * self.centre.y + segment.p2.x * segment.p1.y - segment.p2.y * segment.p1.x) / BC)
        distance = abs(distance - self.rayon)
        return distance

    def getDistance(self, polygon):
        # Calcul de la distance entre le centre du cercle et le polygone
        distances = []
        for i in range(len(polygon.points)):
            # Pour chaque segment du polygone, calculer la distance au cercle
            segment = Segment(polygon.points[i], polygon.points[(i+1) % len(polygon.points)])
            distances.append(self.getDistance(segment))
        # La distance minimale est la distance minimale entre le centre du cercle et les segments du polygone
        distance = min(distances)
        return distance

