import math

def distance_squared(point1, point2):
    """Calcul de la distance euclidienne au carré entre deux points."""
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

def point_plus_proche_cercle(point, centre, rayon):
    """Trouve le point le plus proche sur ou à l'intérieur du cercle."""
    distance_centre_point = math.sqrt(distance_squared(point, centre))

    if distance_centre_point <= rayon:
        return round(point[0], 1), round(point[1], 1)  # Si le point est à l'intérieur du cercle, on le retourne

    # Si le point est à l'extérieur du cercle, on trouve le point sur le contour du cercle le plus proche
    x_centre, y_centre = centre
    dx = point[0] - x_centre
    dy = point[1] - y_centre
    angle = math.atan2(dy, dx)
    x_sur_cercle = x_centre + rayon * math.cos(angle)
    y_sur_cercle = y_centre + rayon * math.sin(angle)

    return round(x_sur_cercle, 1), round(y_sur_cercle, 1)  # Arrondir les coordonnées du point à 1 chiffre après la virgule

