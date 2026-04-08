import math

def compute_bounding_box(vertices):
    """
    Computes axis-aligned bounding box from all mesh vertices.
    
    Input:  list of vertices, each = (x, y, z)
    Output: dictionary with min/max for each axis
    """

    # Start with first vertex as initial min/max
    min_x = max_x = vertices[0][0]
    min_y = max_y = vertices[0][1]
    min_z = max_z = vertices[0][2]

    # Loop every vertex and track min/max per axis
    for v in vertices:
        # X axis
        if v[0] < min_x: min_x = v[0]
        if v[0] > max_x: max_x = v[0]

        # Y axis
        if v[1] < min_y: min_y = v[1]
        if v[1] > max_y: max_y = v[1]

        # Z axis
        if v[2] < min_z: min_z = v[2]
        if v[2] > max_z: max_z = v[2]

    return {
        'min_x': min_x, 'max_x': max_x,
        'min_y': min_y, 'max_y': max_y,
        'min_z': min_z, 'max_z': max_z,
    }


def compute_layer_count(bbox, layer_height=0.2):
    """
    Computes number of complete layers from Z extent.

    Formula: floor((max_z - min_z) / layer_height)
    Partial top layer is NOT counted (floor, not ceil)
    """

    model_height = bbox['max_z'] - bbox['min_z']
    layer_count  = math.floor(model_height / layer_height)

    return model_height, layer_count


def print_bounding_box_report(bbox, model_height, layer_count):
    """
    Prints a clean formatted report for Task 2.
    """

    print("\n--- Task 2: Bounding Box ---")
    print(f"  X  →  min: {bbox['min_x']:10.3f} mm    max: {bbox['max_x']:10.3f} mm    width : {bbox['max_x']-bbox['min_x']:.3f} mm")
    print(f"  Y  →  min: {bbox['min_y']:10.3f} mm    max: {bbox['max_y']:10.3f} mm    width : {bbox['max_y']-bbox['min_y']:.3f} mm")
    print(f"  Z  →  min: {bbox['min_z']:10.3f} mm    max: {bbox['max_z']:10.3f} mm    height: {bbox['max_z']-bbox['min_z']:.3f} mm")

    print(f"\n--- Task 2: Layer Count ---")
    print(f"  Model height : {model_height:.3f} mm")
    print(f"  Layer height : 0.2 mm")
    print(f"  Layer count  : {layer_count} complete layers")

    # Sanity check against OrcaSlicer bounding box
    print(f"\n--- Sanity Check vs OrcaSlicer ---")
    print(f"  OrcaSlicer reported: 289.563 x 109.03 x 116.247 mm")
    print(f"  Our computation    : {bbox['max_x']-bbox['min_x']:.3f} x {bbox['max_y']-bbox['min_y']:.3f} x {bbox['max_z']-bbox['min_z']:.3f} mm")
