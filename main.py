from stl_parser import parse_stl, get_all_vertices
from volume import compute_volume

STL_FILE = "DrucksShoe.stl"

# --- Parse ---
triangles = parse_stl(STL_FILE)
vertices  = get_all_vertices(triangles)

# --- Task 1: Volume ---
print("\n--- Task 1: Volume Computation ---")

volume_mm3 = compute_volume(triangles)

# Convert to cm³ and liters for intuition check
volume_cm3   = volume_mm3 / 1000.0
volume_liter = volume_mm3 / 1_000_000.0

print(f"Volume : {volume_mm3:,.2f}  mm³")
print(f"Volume : {volume_cm3:,.2f}  cm³")
print(f"Volume : {volume_liter:.4f}  liters")

# --- Sanity check ---
# A typical shoe is roughly 200–400 cm³
# If your number is wildly off, something is wrong
print(f"\nSanity check:")
print(f"  A real shoe is ~200–400 cm³")
if 100 <= volume_cm3 <= 1000:
    print(f"  {volume_cm3:.1f} cm³ looks reasonable for a shoe")
else:
    print(f"    {volume_cm3:.1f} cm³ seems off — check parser or formula")
