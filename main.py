from stl_parser import parse_stl, get_all_vertices

STL_FILE = "DrucksShoe.stl"

# --- Parse ---
triangles = parse_stl(STL_FILE)

# --- Extract vertices ---
vertices = get_all_vertices(triangles)

# --- Sanity checks ---
print(f"\n--- Parser Verification ---")
print(f"Total triangles  : {len(triangles)}")
print(f"Total vertices   : {len(vertices)}")   # must be triangles × 3
print(f"Expected vertices: {len(triangles) * 3}")

# --- Quick coordinate check ---
# Grab all x, y, z values separately to spot-check
all_x = [v[0] for v in vertices]
all_y = [v[1] for v in vertices]
all_z = [v[2] for v in vertices]

print(f"\n--- Coordinate Ranges (raw check) ---")
print(f"X  →  min: {min(all_x):.3f}   max: {max(all_x):.3f}")
print(f"Y  →  min: {min(all_y):.3f}   max: {max(all_y):.3f}")
print(f"Z  →  min: {min(all_z):.3f}   max: {max(all_z):.3f}")

