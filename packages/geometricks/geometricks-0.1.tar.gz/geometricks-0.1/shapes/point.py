import math
import sys
from polygon import Polygon


class Point: 
        def __init__(self, x, y):
                self.x = x
                self.y = y
                
        def get_coord(self):
            return (self.x, self.y)
        

        #####-Distance between a point and something-#####

        def getDistance(self, point):
                # get the distance between two points
                x1, y1 = point.get_coord()
                x2, y2 = self.x, self.y
                return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        def getDistance(self, droite):
                # get the distance between a point and a line
                x, y = self.x, self.y
                return abs((droite.a * x + droite.b * y + droite.c) / math.sqrt(droite.a**2 + droite.b**2))

        def getDistance(self, segment):
                # get the distance between a point and a segment
                x1, y1 = segment.p1.x, segment.p1.y
                x2, y2 = segment.p2.x, segment.p2.y
                x, y = self.x, self.y
                dx = x2 - x1
                dy = y2 - y1
                if dx == dy == 0:  #from getClosest.getClosestPolygon import point_plus_proche_polygone If points p1 and p2 are the same
                        return math.sqrt((x - x1)**2 + (y - y1)**2)
                t = ((x - x1) * dx + (y - y1) * dy) / (dx**2 + dy**2)
                t = max(0, min(1, t))  # Limit t between 0 and 1 to be on the segment
                proj_x = x1 + t * dx
                proj_y = y1 + t * dy
                return math.sqrt((x - proj_x)**2 + (y - proj_y)**2)


        def getDistance(self, polygon):
                # get the distance between a point and a polygon
                #tabPoly doit être égal au tableau de points du polygone
                tabPoly = polygon.get_coord()
                
                point = Point(0, 0)
                point.x, point.y = self.point_plus_proche_polygone(polygon)
                return self.getDistance(point)
                
        def ranger_points_sens_horaire(self, points):
                # Trouver le point le plus bas (le plus à gauche en cas d'égalité)
                point_de_depart = min(points, key=lambda p: (p.x, p.y))

                # Trier les points en fonction de l'angle par rapport au point de départ
                def angle_par_rapport_au_point_de_depart(p):
                        x, y = p.x - point_de_depart.x, p.y - point_de_depart.y
                        return (math.atan2(y, x) + 2 * math.pi) % (2 * math.pi)

                points_tries = sorted(points, key=angle_par_rapport_au_point_de_depart)

                return points_tries


        def point_dans_polygone(self, polygone):
                n = len(polygone.points)
                inside = False
                
                polygone_ranger = self.ranger_points_sens_horaire(polygone.points)

                p1 = polygone_ranger[0]
                for i in range(n + 1):
                        p2 = polygone_ranger[i % n]
                        if self.y > min(p1.y, p2.y):
                                if self.y <= max(p1.y, p2.y):
                                        if self.x <= max(p1.x, p2.x):
                                                if p1.y != p2.y:
                                                        xinters = (self.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                                                if p1.x == p2.x or self.x <= xinters:
                                                        inside = not inside
                                        p1 = p2
                        
                return inside


        def point_plus_proche_polygone(self, polygone):
                """Trouve le point le plus proche sur ou à l'intérieur du polygone."""
                if self.point_dans_polygone(polygone):
                        return round(self.x, 1), round(self.y, 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule

                # Recherche du point le plus proche parmi les sommets du polygone
                distance_min = float('inf')
                point_plus_proche = None
                for sommet in polygone.points:
                        distance = self.distance_squared(sommet) # ->> c quoi cette fonction alexx
                        if distance < distance_min:
                                distance_min = distance
                                point_plus_proche = sommet

                # Recherche du point le plus proche sur le contour du polygone
                for i in range(len(polygone.points)):
                        p1 = polygone.points[i]
                        p2 = polygone.points[(i + 1) % len(polygone.points)]
                        # Projection orthogonale du point sur le segment p1-p2
                        p_projetee = self.projection_orthogonale(self, p1, p2)
                        # Si la projection est sur le segment, on vérifie la distance
                        if self.est_sur_segment(p_projetee, p1, p2):
                                distance = self.distance_squared(p_projetee)
                                if distance < distance_min:
                                        distance_min = distance
                                        point_plus_proche = p_projetee

                return round(point_plus_proche.x, 1), round(point_plus_proche.y, 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule


        def projection_orthogonale(self, p1, p2):
                """Calcule la projection orthogonale du point sur le segment p1-p2."""
                x1, y1 = p1.x, p1.y
                x2, y2 = p2.x, p2.y
                dx, dy = x2 - x1, y2 - y1
                u = ((self.x - x1) * dx + (self.y - y1) * dy) / (dx * dx + dy * dy)
                x_proj = x1 + u * dx
                y_proj = y1 + u * dy
                return Point(x_proj, y_proj)


        def est_sur_segment(self, p1, p2):
                """Vérifie si le point est sur le segment défini par p1 et p2."""
                return min(p1.x, p2.x) <= self.x <= max(p1.x, p2.x) and \
                        min(p1.y, p2.y) <= self.y


####################!!!ZONE DE DEBUG!!!##########################et

# test de la fonction getDistance avec un point et un polygon
point = Point(1, 1)
polygon = Polygon([Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)])
print("test py")
print(point.getDistance(polygon))  

