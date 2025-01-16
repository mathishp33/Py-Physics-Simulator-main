import numpy as np

def normalize(x: np.array) -> np.array:
    len_ = np.linalg.norm(x)
    if len_ == 0:
        return x
    return x / len_

def find_point_polygon(objectA: object, objectB: object) -> int:
    result = 0
    min_dist = 100000
    
    for k in range(len(objectA.vertices)):
        dist = np.hypot(objectA.vertices[k][0] - objectB.x, objectA.vertices[k][1] - objectB.y)
        if dist < min_dist:
            min_dist = dist
            result = k
    return result

def project_vertices(vertices: np.array, axis: np.array) -> tuple[float, float]:
    min_ = 100000
    max_ = 0
    for k in vertices:
        proj = np.dot(k, axis)
        if proj < min_: min_ = proj
        if proj > max_: max_ = proj
    return min_, max_

def project_circle(center: tuple, radius: int, axis: tuple) -> tuple[float, float]:
    dir_ = normalize(axis)
    dir_radius = dir_ * radius

    p1 = (center[0] + dir_radius[0], center[1]  + dir_radius[1])
    p2 = (center[0] - dir_radius[0], center[1]  - dir_radius[1])
    
    min_ = np.dot(p1, axis)
    max_ = np.dot(p2, axis)
    
    if min_ > max_:
        max_, min_ = min_, max_
        
    return min_, max_       

def intersect_rect_rect(a: object, b: object) -> tuple[bool, tuple, float]:
    dir_ = (b.x-a.x, b.y-a.y)
    normal = (0, 0)
    depth = 100000

    for j in range(len(a.vertices)):
        va = a.vertices[j]
        vb = a.vertices[(j+1) % len(a.vertices)]

        edge = (vb[0]-va[0], vb[1]-va[1])
        axis = np.array((-edge[1], edge[0]))
        axis = normalize(axis)
        
        min_A, max_A = project_vertices(a.vertices, axis)
        min_B, max_B = project_vertices(b.vertices, axis)
        
        if (min_A >= max_B or min_B >= max_A):
            return False, normal, depth
        
        depth_axis = min(max_B - min_A, max_A - min_B)
        if depth > depth_axis:
            depth = depth_axis
            normal = axis
        
    for j in range(len(b.vertices)):
        va = b.vertices[j]
        vb = b.vertices[(j+1) % len(b.vertices)]
        edge = (vb[0]-va[0], vb[1]-va[1])
        axis = np.array((-edge[1], edge[0]))
        axis = normalize(axis)
        
        min_A, max_A = project_vertices(a.vertices, axis)
        min_B, max_B = project_vertices(b.vertices, axis)
        
        if (min_A >= max_B or min_B >= max_A):
            return False, normal, depth
        
        depth_axis = min(max_B - min_A, max_A - min_B)
        if depth > depth_axis:
            depth = depth_axis
            normal = axis
          
        depth = depth / np.hypot(normal[0], normal[1]+0.0001)
        normal = normalize(normal)
        if np.dot(dir_, normal) < 0:
            normal = (-normal[0], -normal[1])

    return True, normal, depth

def intersect_circle_circle(objectA: object, objectB: object) -> tuple[bool, tuple, float]:
    normal = (0, 0)
    depth = 100000
    dist = np.hypot((objectA.x-objectB.x), (objectA.y-objectB.y))
    radiusAB = objectA.radius+objectB.radius
    
    if dist < radiusAB:

        depth =  radiusAB - dist
        normal = (objectB.x-objectA.x), (objectB.y-objectA.y)
        normal = normalize(normal)

        return True, normal, depth
    
    return False, normal, depth

def intersect_circle_rect(objectA: object, objectB: object) -> tuple[bool, tuple, float]:
    dir_ = (objectB.x-objectA.x, objectB.y-objectA.y)
    normal = (0, 0)
    depth = 100000
    for j in range(len(objectB.vertices)):
        edge = (objectB.vertices[(j+1) % len(objectB.vertices)][0]-objectB.vertices[j][0], objectB.vertices[(j+1) % len(objectB.vertices)][1]-objectB.vertices[j][1])
        axis = (-edge[1], edge[0])
        axis = normalize(axis)
        
        min_A, max_A = project_vertices(objectB.vertices, axis)
        min_B, max_B = project_circle((objectA.x, objectA.y), objectA.radius, axis)
        
        if (min_A >= max_B or min_B >= max_A):
            return False, normal, depth
        
        depth_axis = min(max_B - min_A, max_A - min_B)
        if depth > depth_axis:
            depth = depth_axis
            normal = axis
            
    try:
        cp_index = find_point_polygon(objectB, objectA)
        cp = objectB.vertices[cp_index]
    except:
        return False, normal, depth
    axis = (cp[0] - objectB.x, cp[1] - objectB.y)
    
    min_A, max_A = project_vertices(objectB.vertices, axis)
    min_B, max_B = project_circle((objectA.x, objectA.y), objectA.radius, axis)
    
    if (min_A >= max_B or min_B >= max_A):
        return False, normal, depth
    
    depth_axis = min(max_B - min_A, max_A - min_B)
    if depth > depth_axis:
        depth = depth_axis
        normal = axis

        depth = depth / np.hypot(normal[0], normal[1])
        normal = normalize(normal)
        if np.dot(dir_, normal) < 0:
            normal = (-normal[0], -normal[1])
            
    return True, normal, depth
    
def intersect_rect_circle(objectA: object, objectB: object) -> tuple[bool, tuple, float]:
    dir_ = (objectB.x-objectA.x, objectB.y-objectA.y)
    normal = (0, 0)
    depth = 100000
    for j in range(len(objectA.vertices)):
        edge = (objectA.vertices[(j+1) % len(objectA.vertices)][0]-objectA.vertices[j][0], objectA.vertices[(j+1) % len(objectA.vertices)][1]-objectA.vertices[j][1])
        axis = (-edge[1], edge[0])
        axis = normalize(axis)
        
        min_A, max_A = project_vertices(objectA.vertices, axis)
        min_B, max_B = project_circle((objectB.x, objectB.y), objectB.radius, axis)
        
        if (min_A >= max_B or min_B >= max_A):
            return False, normal, depth
        
        depth_axis = min(max_B - min_A, max_A - min_B)
        if depth > depth_axis:
            depth = depth_axis
            normal = axis

    try:     
        cp_index = find_point_polygon(objectA, objectB)
        cp = objectA.vertices[cp_index]
    except:
        return False, normal, depth
    axis = (cp[0] - objectA.x, cp[1] - objectA.y)
    
    min_A, max_A = project_vertices(objectA.vertices, axis)
    min_B, max_B = project_circle((objectB.x, objectB.y), objectB.radius, axis)
    
    if (min_A >= max_B or min_B >= max_A):
        return False, normal, depth
    
    depth_axis = min(max_B - min_A, max_A - min_B)
    if depth > depth_axis:
        depth = depth_axis
        normal = axis

        depth = depth / np.hypot(normal[0], normal[1])
        normal = normalize(normal)
        if np.dot(dir_, normal) < 0:
            normal = (-normal[0], -normal[1])
            
    return True, normal, depth
