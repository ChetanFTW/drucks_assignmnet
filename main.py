from stl_parser import parse_stl, get_all_vertices
from volume import compute_volume
from bounding_box import compute_bounding_box, compute_layer_count, print_bounding_box_report

STL_FILE = "DrucksShoe.stl"

# --- Parse ---
triangles = parse_stl(STL_FILE)
vertices  = get_all_vertices(triangles)

# --- Task 1: Volume ---
print("\n--- Task 1: Volume Computation ---")
volume_mm3 = compute_volume(triangles)
print(f"Volume : {volume_mm3:,.2f}  mm³")
print(f"Volume : {volume_mm3/1000:,.2f}  cm³")

# --- Task 2: Bounding Box + Layer Count ---
bbox                      = compute_bounding_box(vertices)
model_height, layer_count = compute_layer_count(bbox, layer_height=0.2)
print_bounding_box_report(bbox, model_height, layer_count)
