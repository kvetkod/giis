import matplotlib.pyplot as plt
from collections import defaultdict

class Delone:
    def circumcircle(self, tri):
        (ax, ay), (bx, by), (cx, cy) = tri

        A = bx - ax
        B = by - ay
        C = cx - ax
        D = cy - ay

        E = A * (ax + bx) + B * (ay + by)
        F = C * (ax + cx) + D * (ay + cy)
        G = 2 * (A * (cy - by) - B * (cx - bx))

        if G == 0:
            return ((0, 0), float('inf'))  

        cx = (D * E - B * F) / G
        cy = (A * F - C * E) / G
        center = (cx, cy)
        radius_sq = (cx - ax) ** 2 + (cy - ay) ** 2
        return center, radius_sq

    def is_in_circle(self, p, center, radius_sq):
        dx = p[0] - center[0]
        dy = p[1] - center[1]
        return dx * dx + dy * dy < radius_sq

    def edges_from(self, tri):
        a, b, c = tri
        return {(a, b), (b, c), (c, a)}

    def delaunay_triangulation(self, points):
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)

        dx = max_x - min_x
        dy = max_y - min_y
        delta_max = max(dx, dy)
        mid_x = (min_x + max_x) / 2
        mid_y = (min_y + max_y) / 2

        p1 = (mid_x - 20 * delta_max, mid_y - delta_max)
        p2 = (mid_x, mid_y + 20 * delta_max)
        p3 = (mid_x + 20 * delta_max, mid_y - delta_max)

        triangles = [(p1, p2, p3)]

        for point in points:
            bad_triangles = []
            for tri in triangles:
                center, radius_sq = self.circumcircle(tri)
                if self.is_in_circle(point, center, radius_sq):
                    bad_triangles.append(tri)

            edge_count = {}
            for tri in bad_triangles:
                for edge in self.edges_from(tri):
                    edge = tuple(sorted(edge))
                    if edge in edge_count:
                        edge_count[edge] += 1
                    else:
                        edge_count[edge] = 1

            polygon = [edge for edge, count in edge_count.items() if count == 1]
            triangles = [t for t in triangles if t not in bad_triangles]

            for edge in polygon:
                triangles.append((edge[0], edge[1], point))

        
        def contains_super(p):
            return p in (p1, p2, p3)

        final_triangles = []
        for tri in triangles:
            if any(contains_super(p) for p in tri):
                continue
            final_triangles.append(tri)

        return final_triangles

class VoronoiDiagram:
    def __init__(self, delaunay):
        self.delaunay = delaunay

    def construct_voronoi(self, points):
        triangles = self.delaunay.delaunay_triangulation(points)

        circumcenters = []
        point_regions = defaultdict(list)

        for tri in triangles:
            center, _ = self.delaunay.circumcircle(tri)
            circumcenters.append((tri, center))

        for (tri, center) in circumcenters:
            for vertex in tri:
                point_regions[vertex].append(center)

        return point_regions



