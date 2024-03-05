class Polygon:
    def __init__(self, points):
        if len(points) < 3:
            raise ValueError("Un polygone doit avoir au moins 3 points.")
        self.points = points  # Utilisation d'une variable protégée _points
    
    def get_coord(self):
        return self.points

