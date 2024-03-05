import math
import sys

sys.path.append('../shapes/')

from point import Point

def ranger_points_sens_horaire(points):
    # Trouver le point le plus bas (le plus à gauche en cas d'égalité)
    point_de_depart = min(points, key=lambda p: (p.x, p.y))

    # Trier les points en fonction de l'angle par rapport au point de départ
    def angle_par_rapport_au_point_de_depart(p):
        x, y = p.x - point_de_depart.x, p.y - point_de_depart.y
        return (math.atan2(y, x) + 2 * math.pi) % (2 * math.pi)

    points_tries = sorted(points, key=angle_par_rapport_au_point_de_depart)

    return points_tries


def point_dans_polygone(point, polygone):
    n = len(polygone.points)
    inside = False
    
    polygone_ranger = ranger_points_sens_horaire(polygone.points)

    p1 = polygone_ranger[0]
    for i in range(n + 1):
        p2 = polygone_ranger[i % n]
        if point.y > min(p1.y, p2.y):
            if point.y <= max(p1.y, p2.y):
                if point.x <= max(p1.x, p2.x):
                    if p1.y != p2.y:
                        xinters = (point.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                    if p1.x == p2.x or point.x <= xinters:
                        inside = not inside
        p1 = p2
        
    return inside


def point_plus_proche_polygone(point, polygone):
    """Trouve le point le plus proche sur ou à l'intérieur du polygone."""
    if point_dans_polygone(point, polygone):
        return round(point.x, 1), round(point.y, 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule

    # Recherche du point le plus proche parmi les sommets du polygone
    distance_min = float('inf')
    point_plus_proche = None
    for sommet in polygone.points:
        distance = point.distance_squared(sommet)
        if distance < distance_min:
            distance_min = distance
            point_plus_proche = sommet

    # Recherche du point le plus proche sur le contour du polygone
    for i in range(len(polygone.points)):
        p1 = polygone.points[i]
        p2 = polygone.points[(i + 1) % len(polygone.points)]
        # Projection orthogonale du point sur le segment p1-p2
        p_projetee = projection_orthogonale(point, p1, p2)
        # Si la projection est sur le segment, on vérifie la distance
        if est_sur_segment(p_projetee, p1, p2):
            distance = point.distance_squared(p_projetee)
            if distance < distance_min:
                distance_min = distance
                point_plus_proche = p_projetee

    return round(point_plus_proche.x, 1), round(point_plus_proche.y, 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule


def projection_orthogonale(point, p1, p2):
    """Calcule la projection orthogonale du point sur le segment p1-p2."""
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    dx, dy = x2 - x1, y2 - y1
    u = ((point.x - x1) * dx + (point.y - y1) * dy) / (dx * dx + dy * dy)
    x_proj = x1 + u * dx
    y_proj = y1 + u * dy
    return Point(x_proj, y_proj)


def est_sur_segment(point, p1, p2):
    """Vérifie si le point est sur le segment défini par p1 et p2."""
    return min(p1.x, p2.x) <= point.x <= max(p1.x, p2.x) and \
           min(p1.y, p2.y) <= point.y

