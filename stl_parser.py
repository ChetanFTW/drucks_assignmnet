import struct
import os

def parse_stl(filepath):
    """
    Reads a binary STL file and returns a list of triangles.
    Each triangle is a tuple of 3 vertices: ((x1,y1,z1), (x2,y2,z2), (x3,y3,z3))
    """

    triangles = []

    with open(filepath, 'rb') as f:   # 'rb' = read binary

        # --- HEADER ---
        # First 80 bytes are a description string, we don't need it
        header = f.read(80)

        # --- TRIANGLE COUNT ---
        # Next 4 bytes = number of triangles as unsigned 32-bit int
        num_triangles_data = f.read(4)
        num_triangles = struct.unpack('<I', num_triangles_data)[0]
        # '<' = little endian, 'I' = unsigned int

        print(f"Header: {header[:40]}")        # print first 40 chars of header
        print(f"Triangle count: {num_triangles}")

        # --- VERIFY FILE SIZE ---
        # Binary STL must be exactly: 80 + 4 + (num_triangles * 50) bytes
        expected_size = 80 + 4 + (num_triangles * 50)
        actual_size = os.path.getsize(filepath)

        if actual_size != expected_size:
            raise ValueError(
                f"File size mismatch. Expected {expected_size} bytes, "
                f"got {actual_size} bytes. File may be ASCII or corrupted."
            )

        # --- READ EACH TRIANGLE ---
        for i in range(num_triangles):

            # Normal vector: 3 floats × 4 bytes = 12 bytes (we skip this)
            f.read(12)

            # Vertex 1: 3 floats = 12 bytes
            v1 = struct.unpack('<fff', f.read(12))

            # Vertex 2: 3 floats = 12 bytes
            v2 = struct.unpack('<fff', f.read(12))

            # Vertex 3: 3 floats = 12 bytes
            v3 = struct.unpack('<fff', f.read(12))

            # Attribute byte count: 2 bytes (always ignore)
            f.read(2)

            # Store triangle as tuple of 3 vertices
            triangles.append((v1, v2, v3))

    return triangles

def get_all_vertices(triangles):
    """
    Flattens all triangles into a single list of vertices.
    Input:  list of triangles → each is ((x1,y1,z1), (x2,y2,z2), (x3,y3,z3))
    Output: list of all vertices → each is (x, y, z)
    
    Note: vertices are repeated (each vertex appears in multiple triangles)
    That is fine — we need all of them for min/max calculations.
    """
    vertices = []
    for triangle in triangles:
        for vertex in triangle:       # each triangle has 3 vertices
            vertices.append(vertex)
    return vertices
