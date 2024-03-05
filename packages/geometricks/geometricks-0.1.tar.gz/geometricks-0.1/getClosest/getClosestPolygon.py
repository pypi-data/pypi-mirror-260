import math


def distance_squared(point1, point2):
    """Calcul de la distance euclidienne au carré entre deux points."""
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2


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
    x, y = point[0], point[1]
    n = len(polygone)
    inside = False
    
    polygone_ranger = ranger_points_sens_horaire(polygone)

    (p1x, p1y) = polygone_ranger[0].x, polygone_ranger[0].y
    for i in range(n+1):
        p2x, p2y = polygone_ranger[i % n].x, polygone_ranger[i % n].y
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
        
    return inside

def point_plus_proche_polygone(point, polygone):
    """Trouve le point le plus proche sur ou à l'intérieur du polygone."""
    if point_dans_polygone(point, polygone):
        return round(point[0], 1), round(point[1], 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule

    # Recherche du point le plus proche parmi les sommets du polygone
    distance_min = float('inf')
    point_plus_proche = None
    for sommet in polygone:
        distance = distance_squared(point, sommet)
        if distance < distance_min:
            distance_min = distance
            point_plus_proche = sommet

    # Recherche du point le plus proche sur le contour du polygone
    for i in range(len(polygone)):
        p1 = polygone[i]
        p2 = polygone[(i + 1) % len(polygone)]
        # Projection orthogonale du point sur le segment p1-p2
        p_projetee = projection_orthogonale(point, p1, p2)
        # Si la projection est sur le segment, on vérifie la distance
        if est_sur_segment(p_projetee, p1, p2):
            distance = distance_squared(point, p_projetee)
            if distance < distance_min:
                distance_min = distance
                point_plus_proche = p_projetee

    return round(point_plus_proche[0], 1), round(point_plus_proche[1], 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule


def projection_orthogonale(point, p1, p2):
    """Calcule la projection orthogonale du point sur le segment p1-p2."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    u = ((point[0] - x1) * dx + (point[1] - y1) * dy) / (dx * dx + dy * dy)
    x_proj = x1 + u * dx
    y_proj = y1 + u * dy
    return x_proj, y_proj

def est_sur_segment(point, p1, p2):
    """Vérifie si le point est sur le segment défini par p1 et p2."""
    return min(p1[0], p2[0]) <= point[0] <= max(p1[0], p2[0]) and \
           min(p1[1], p2[1]) <= point[1] <= max(p1[1], p2[1])


