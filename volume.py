def compute_signed_tetrahedron_volume(v1, v2, v3):
    """
    Computes the signed volume of a tetrahedron formed by
    one triangle (v1, v2, v3) and the origin (0, 0, 0).

    Formula: V = (v1 · (v2 × v3)) / 6

    Each vertex is a tuple (x, y, z)
    """

    # --- Step 1: Cross product of v2 × v3 ---
    # Result is a vector perpendicular to both v2 and v3
    cross_x = v2[1]*v3[2] - v2[2]*v3[1]
    cross_y = v2[2]*v3[0] - v2[0]*v3[2]
    cross_z = v2[0]*v3[1] - v2[1]*v3[0]

    # --- Step 2: Dot product of v1 · (v2 × v3) ---
    # Result is a single scalar number
    dot = v1[0]*cross_x + v1[1]*cross_y + v1[2]*cross_z

    # --- Step 3: Divide by 6 ---
    return dot / 6.0


def compute_volume(triangles):
    """
    Computes total volume of a closed mesh using
    signed tetrahedra decomposition.

    Input:  list of triangles, each = ((x1,y1,z1), (x2,y2,z2), (x3,y3,z3))
    Output: volume in mm³ (positive)
    """

    total_signed_volume = 0.0

    for triangle in triangles:
        v1, v2, v3 = triangle[0], triangle[1], triangle[2]
        total_signed_volume += compute_signed_tetrahedron_volume(v1, v2, v3)

    # Absolute value because sign depends on model orientation
    return abs(total_signed_volume)
