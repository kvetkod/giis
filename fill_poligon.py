from collections import defaultdict
from collections import deque

class Fill:
    def build_edge_table(self, vertices):
        edge_table = defaultdict(list)
        n = len(vertices)
        
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            
            if y1 == y2:
                continue 
            
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1
            
            edge_table[y1].append({
                'x': x1,
                'y_max': y2,
                'inv_slope': (x2 - x1) / (y2 - y1)
            })
        
        return edge_table

    def scanline_fill(self, vertices):
        edge_table = self.build_edge_table(vertices)
        active_edges = []
        
        y_min = min(y for _, y in vertices)
        y_max = max(y for _, y in vertices)
        
        scanline_points = []
        
        for y in range(y_min, y_max + 1):
            if y in edge_table:
                active_edges.extend(edge_table[y])
            
            active_edges = [e for e in active_edges if e['y_max'] > y]
            active_edges.sort(key=lambda e: e['x'])
            
            for i in range(0, len(active_edges), 2):
                if i + 1 < len(active_edges):
                    x1, x2 = int(round(active_edges[i]['x'])), int(round(active_edges[i + 1]['x']))
                    for x in range(x1, x2 + 1):
                        scanline_points.append((x, y))
            
            for edge in active_edges:
                edge['x'] += edge['inv_slope']
        
        return scanline_points
    

    def build_action_edge_table(self, vertices):
        edge_table = defaultdict(list)
        n = len(vertices)
        
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            
            if y1 == y2:
                continue  # Пропускаем горизонтальные ребра
            
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1
            
            edge_table[y1].append({
                'x': x1,
                'y_max': y2,
                'inv_slope': (x2 - x1) / (y2 - y1)
            })
        
        return edge_table

    def scanline_fill_action(self, vertices):
        edge_table = self.build_action_edge_table(vertices)
        active_edge_table = []
        
        y_min = min(y for _, y in vertices)
        y_max = max(y for _, y in vertices)
        
        scanline_points = []
        
        for y in range(y_min, y_max + 1):
            if y in edge_table:
                active_edge_table.extend(edge_table[y])
            
            active_edge_table = [e for e in active_edge_table if e['y_max'] > y]
            active_edge_table.sort(key=lambda e: e['x'])
            
            for i in range(0, len(active_edge_table), 2):
                if i + 1 < len(active_edge_table):
                    x1, x2 = int(round(active_edge_table[i]['x'])), int(round(active_edge_table[i + 1]['x']))
                    for x in range(x1, x2 + 1):
                        scanline_points.append((x, y))
            
            for edge in active_edge_table:
                edge['x'] += edge['inv_slope']
        
        return scanline_points
    
    def bresenham_line(self, x1, y1, x2, y2):
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return points

    def get_polygon_edges(self, vertices):
        edge_points = set()
        n = len(vertices)
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            edge_points.update(self.bresenham_line(x1, y1, x2, y2))
        return edge_points

    def flood_fill(self, seed, boundary_set):
        filled = set()
        queue = deque([seed])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        while queue:
            x, y = queue.popleft()
            if (x, y) in filled or (x, y) in boundary_set:
                continue
            filled.add((x, y))
            for dx, dy in directions:
                queue.append((x + dx, y + dy))
        
        return list(filled)

    def find_seed_point(self, polygon_points):
        x_coords = [x for x, y in polygon_points]
        y_coords = [y for x, y in polygon_points]
        centroid_x = sum(x_coords) // len(polygon_points)
        centroid_y = sum(y_coords) // len(polygon_points)
        return (centroid_x, centroid_y)

    def polygon_seed_fill(self, vertices):
        boundary_set = self.get_polygon_edges(vertices)
        seed = self.find_seed_point(vertices)

        
        if seed in boundary_set:
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    test_seed = (seed[0] + dx, seed[1] + dy)
                    if test_seed not in boundary_set:
                        seed = test_seed
                        break
                else:
                    continue
                break

        filled = self.flood_fill(seed, boundary_set)
        return filled

    def find_seed_point(self, polygon_points):
        x_coords = [x for x, y in polygon_points]
        y_coords = [y for x, y in polygon_points]
        centroid_x = sum(x_coords) // len(polygon_points)
        centroid_y = sum(y_coords) // len(polygon_points)
        return (centroid_x, centroid_y)

    def line_seed_fill(self, vertices):
        boundary = self.get_polygon_edges(vertices)
        filled = set()
        seed = self.find_seed_point(vertices)

        if seed in boundary:
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    test = (seed[0] + dx, seed[1] + dy)
                    if test not in boundary:
                        seed = test
                        break
                else:
                    continue
                break

        stack = deque([seed])
        
        while stack:
            x, y = stack.pop()

            if (x, y) in filled or (x, y) in boundary:
                continue

            x_left = x
            while (x_left - 1, y) not in boundary and (x_left - 1, y) not in filled:
                x_left -= 1

            x_right = x
            while (x_right + 1, y) not in boundary and (x_right + 1, y) not in filled:
                x_right += 1

            for xi in range(x_left, x_right + 1):
                filled.add((xi, y))

            for ny in [y - 1, y + 1]:
                xi = x_left
                while xi <= x_right:
                    span_start = None
                    while xi <= x_right and (xi, ny) not in boundary and (xi, ny) not in filled:
                        if span_start is None:
                            span_start = xi
                        xi += 1
                    if span_start is not None:
                        stack.append((span_start, ny))
                    while xi <= x_right and ((xi, ny) in filled or (xi, ny) in boundary):
                        xi += 1

        return list(filled)