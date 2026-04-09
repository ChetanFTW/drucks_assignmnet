from stl_parser import parse_stl, get_all_vertices
from volume import compute_volume
from bounding_box import compute_bounding_box, compute_layer_count, print_bounding_box_report
from slicer import compute_print_time

STL_FILE = "DrucksShoe.stl"

# --- Parse ---
triangles = parse_stl(STL_FILE)
vertices  = get_all_vertices(triangles)

# --- Task 1: Volume ---
print("\n--- Task 1: Volume ---")
volume_mm3 = compute_volume(triangles)
print(f"Volume : {volume_mm3:,.2f} mm³  ({volume_mm3/1000:.2f} cm³)")

# --- Task 2: Bounding Box + Layer Count ---
bbox = compute_bounding_box(vertices)
model_height, layer_count = compute_layer_count(bbox, layer_height=0.2)
print_bounding_box_report(bbox, model_height, layer_count)

# --- Task 3: Print Time ---
print("\n--- Task 3: Print Time Estimation ---")
print(f"  Settings: speed=60mm/s  layer=0.2mm  walls=1  infill=0%")

results = compute_print_time(
    triangles,
    min_z        = bbox['min_z'],
    max_z        = bbox['max_z'],
    layer_height = 0.2,
    print_speed  = 60.0
)

print(f"\n  Total layers       : {results['layer_count']}")
print(f"  Total path length  : {results['total_path_mm']:,.1f} mm")
print(f"  Total path length  : {results['total_path_mm']/1000:,.2f} m")
print(f"  Avg perimeter/layer: {results['avg_perimeter_mm']:.1f} mm")
print(f"\n  ⏱  Estimated print time: {results['time_formatted']}")
print(f"     ({results['time_seconds']:.0f} seconds total)")
