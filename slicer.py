import math

def triangle_plane_intersection(triangle, z):
    """
    Finds the line segment where a horizontal plane at height Z
    cuts through a triangle.

    A triangle has 3 edges. If the plane cuts the triangle,
    exactly 2 edges will cross the plane → giving 2 points → 1 segment.

    Input:  triangle = ((x1,y1,z1), (x2,y2,z2), (x3,y3,z3))
            z        = height of the cutting plane
    Output: (point_a, point_b) or None if no intersection
    """

    v1, v2, v3 = triangle

    # All 3 edges of the triangle
    edges = [(v1, v2), (v2, v3), (v3, v1)]

    intersection_points = []

    for v_a, v_b in edges:

        za = v_a[2]   # z of first vertex
        zb = v_b[2]   # z of second vertex

        # Check if this edge crosses the plane at height z
        # One vertex must be below z, other must be above z
        if (za < z <= zb) or (zb < z <= za):

            # Linear interpolation to find crossing point
            # t = how far along the edge the crossing happens (0.0 to 1.0)
            t = (z - za) / (zb - za)

            # Interpolate x and y at that t value
            x = v_a[0] + t * (v_b[0] - v_a[0])
            y = v_a[1] + t * (v_b[1] - v_a[1])

            intersection_points.append((x, y))

    # We need exactly 2 points to form a segment
    if len(intersection_points) == 2:
        return (intersection_points[0], intersection_points[1])

    return None   # Triangle doesn't cross this Z plane


def segment_length(point_a, point_b):
    """
    2D Euclidean distance between two points.
    We only need x,y because both points are at the same Z.

    Formula: sqrt((x2-x1)² + (y2-y1)²)
    """
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    return math.sqrt(dx*dx + dy*dy)


def compute_layer_perimeter(triangles, z):
    """
    Computes the total perimeter of all cross-section outlines
    at a given Z height.

    Finds all triangles that cross height z,
    computes their intersection segments,
    sums all segment lengths.

    Input:  triangles = full mesh triangle list
            z         = layer height to slice at
    Output: total perimeter in mm at this layer
    """

    total_perimeter = 0.0

    for triangle in triangles:

        # Quick check: does this triangle even reach height z?
        zs = [triangle[0][2], triangle[1][2], triangle[2][2]]

        if min(zs) > z or max(zs) < z:
            continue    # Triangle entirely above or below → skip

        # Find intersection segment
        segment = triangle_plane_intersection(triangle, z)

        if segment is not None:
            length = segment_length(segment[0], segment[1])
            total_perimeter += length

    return total_perimeter


def compute_print_time(triangles, min_z, max_z,
                       layer_height=0.2, print_speed=60.0):
    """
    Estimates total print time for a hollow shell (1 wall, no infill).

    Steps:
      1. For each layer Z, compute perimeter of cross-section
      2. Sum all perimeters → total nozzle path length
      3. Divide by print speed → time in seconds

    Input:  triangles   = full mesh
            min_z       = lowest Z in mesh
            max_z       = highest Z in mesh
            layer_height= 0.2 mm
            print_speed = 60 mm/s
    Output: dict with full results
    """

    total_path_length = 0.0
    layer_perimeters  = []
    layer_count       = 0

    # Generate all Z heights we will slice at
    # Start at min_z + layer_height (first complete layer)
    z = min_z + layer_height

    print(f"\n  Slicing layers", end="", flush=True)

    while z <= max_z:

        perimeter = compute_layer_perimeter(triangles, z)
        layer_perimeters.append(perimeter)
        total_path_length += perimeter
        layer_count += 1
        z += layer_height

        # Progress indicator (dots every 50 layers)
        if layer_count % 50 == 0:
            print(f".", end="", flush=True)

    print(f" done ({layer_count} layers)")

    # Time = distance / speed
    total_time_seconds = total_path_length / print_speed

    # Convert to hours and minutes
    hours   = int(total_time_seconds // 3600)
    minutes = int((total_time_seconds % 3600) // 60)
    seconds = int(total_time_seconds % 60)

    return {
        'layer_count'       : layer_count,
        'total_path_mm'     : total_path_length,
        'time_seconds'      : total_time_seconds,
        'time_formatted'    : f"{hours}h {minutes}m {seconds}s",
        'avg_perimeter_mm'  : total_path_length / layer_count if layer_count else 0,
        'layer_perimeters'  : layer_perimeters,
    }
