
def point_plus_proche_segment(point, p1, p2):
    """Trouve le point le plus proche sur le segment défini par les points p1 et p2."""
    x1, y1 = p1
    x2, y2 = p2

    # Calcul des coordonnées du vecteur entre p1 et p2
    dx, dy = x2 - x1, y2 - y1

    # Si les deux points sont identiques, retourner simplement l'un d'eux
    if dx == 0 and dy == 0:
        return p1

    # Paramètre de la projection orthogonale du point sur la droite
    t = ((point[0] - x1) * dx + (point[1] - y1) * dy) / (dx * dx + dy * dy)

    # Si la projection est en dehors du segment, comparer les distances aux extrémités du segment
    if t < 0:
        return p1
    elif t > 1:
        return p2
    else:
        # Point projeté sur le segment
        x_proj = x1 + t * dx
        y_proj = y1 + t * dy
        return x_proj, y_proj
