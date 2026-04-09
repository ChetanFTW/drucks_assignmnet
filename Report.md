# Drucks Technical Assessment

## AI Tool Declaration
I used Claude (claude.ai) throughout this assessment for:
- Understanding signed tetrahedra math
- Navigating OrcaSlicer codebase
- Structuring this report

The complete conversation has been exported and submitted 
as a PDF alongside this report as required.

---

## Results Summary

| Task | Metric | Our Result | OrcaSlicer | Difference |
|---|---|---|---|---|
| Task 1 | Volume | 406,550.65 mm³ | 406,547 mm³ | 0.0009% |
| Task 2 | X width | 289.563 mm | 289.563 mm | 0.000% |
| Task 2 | Y width | 109.030 mm | 109.030 mm | 0.000% |
| Task 2 | Z height | 116.247 mm | 116.247 mm | 0.000% |
| Task 2 | Layers | 581 | 581 | 0 |
| Task 3 | Print time | 1h 53m 32s | 1h 57m (outer wall) | ~3% |

---

## Task 1: Volume Computation

### Method — Signed Tetrahedra Decomposition

For every triangle on the surface with vertices v1, v2, v3,
a tetrahedron is formed using the origin (0,0,0) as the 
fourth point. The signed volume of each tetrahedron is:
V = (v1 · (v2 × v3)) / 6

Triangles facing outward contribute positive volume.
Triangles facing inward contribute negative volume.
Summed across all triangles of a closed mesh, signed volumes
cancel correctly and produce the true enclosed volume.
Absolute value is taken at the end.

### Why It Works

The scalar triple product v1 · (v2 × v3) gives the volume
of the parallelepiped formed by three vectors. A tetrahedron
is exactly 1/6 of that. This is mathematically equivalent
to integrating volume over the entire mesh — provable via
the divergence theorem.

The sign of each tetrahedron depends on whether the triangle
faces toward or away from the origin. For a closed watertight
mesh, all signs cancel correctly regardless of where the
origin is placed.

### Results

| Metric | Value |
|---|---|
| Our computed volume | 406,550.65 mm³ |
| OrcaSlicer volume | 406,547.00 mm³ |
| Absolute difference | 3.65 mm³ |
| Percentage difference | **0.0009%** |

### Why The Tiny Difference Exists

Floating point arithmetic across 373,632 triangles accumulates
rounding error at the ~3 mm³ scale. This is expected. 
OrcaSlicer uses the same signed tetrahedra method internally,
confirmed by the near-identical result.

---

## Task 2: Bounding Box and Layer Count

### Bounding Box

| Axis | Min (mm) | Max (mm) | Width (mm) |
|---|---|---|---|
| X | -6.953 | 282.610 | 289.563 |
| Y | -62.764 | 46.267 | 109.030 |
| Z | -6.377 | 109.869 | 116.247 |

OrcaSlicer reported: 289.563 × 109.03 × 116.247 mm ✅ exact match

### Layer Count
Model height = 116.247 mm
Layer height = 0.2 mm
Layer count  = floor(116.247 / 0.2) = 581 complete layers

### Print Orientation Discussion

The shoe model as loaded has Z as its tallest dimension
(116.247 mm). However a shoe is an organic shape — it does
not sit flat on its own. Two natural orientations exist:

**Current orientation (sole facing down):**
- Z height = 116.247 mm → 581 layers
- Sole is flat on print bed ✅
- Upper part of shoe has overhangs → needs support

**Rotated (shoe on its side):**
- Z height would become ~109 mm → ~545 layers
- Fewer layers but worse surface quality on sides
- More overhangs overall

**Conclusion:** The current orientation (sole flat on bed)
is the natural print orientation and gives the most 
meaningful layer count of 581. Rotating changes both
layer count and print quality significantly.

---

## Task 3: Print Time Estimation

### Formula
Print Time = Σ perimeter(z_i) / print_speed
where:
z_i            = Z height of layer i
perimeter(z_i) = Σ lengths of triangle-plane
intersection segments at z_i
print_speed    = 60 mm/s
layer_height   = 0.2 mm
wall count     = 1

### Method

For each layer at height Z, every triangle straddling that
Z plane produces a line segment — the intersection of the
horizontal plane with the triangle surface.

For each intersecting triangle:
t = (z - v_a.z) / (v_b.z - v_a.z)
x = v_a.x + t × (v_b.x - v_a.x)
y = v_a.y + t × (v_b.y - v_a.y)
segment_length = sqrt(dx² + dy²)

Summing all segment lengths at each Z gives the perimeter.
Summing all perimeters gives total path length.

### Results

| Metric | Value |
|---|---|
| Total layers | 581 |
| Total path length | 408,752.6 mm (408.75 m) |
| Average perimeter/layer | 703.5 mm |
| **Our estimated time** | **1h 53m 32s (6813s)** |
| OrcaSlicer outer wall | 1h 57m (7020s) |
| OrcaSlicer total time | 6h 14m (22440s) |
| Difference vs outer wall | ~3% |

### Why Our Estimate Closely Matches Outer Wall Time

Our formula computes exactly what OrcaSlicer's outer wall
timer measures — time spent tracing perimeter outlines at
constant speed. The ~3% gap comes from minor acceleration
effects and seam handling OrcaSlicer applies even on 
straight walls.

### Why OrcaSlicer Total Time Is Much Larger

From OrcaSlicer's detailed breakdown:

| Feature | Time | In Our Model? |
|---|---|---|
| Outer wall | 1h 57m | ✅ Yes (our estimate) |
| Overhang wall | 39m 3s | ❌ No |
| Sparse infill | 2h 20m | ❌ No |
| Travel moves | 1h 15m | ❌ No |
| Brim | 42s | ❌ No |
| Retract/Wipe | counted | ❌ No |
| Prepare time | 4m 40s | ❌ No |

### Limitations

1. **No acceleration modelling** — constant 60mm/s assumed.
   Real printers decelerate at every corner.
2. **No travel moves** — nozzle movement between outlines
   adds 1h 15m alone (from OrcaSlicer breakdown).
3. **No retraction/z-hop** — small per-layer overhead
   across 581 layers accumulates significantly.
4. **No overhang detection** — overhangs print slower;
   we treat all perimeters at equal speed.
5. **No seam handling** — extra moves at loop start/end.

Our formula gives a **lower bound** — it captures pure
extrusion-path time with zero overhead.

---

## Task 4: OrcaSlicer Codebase — Layer Height Call Chain

### Search Strategy

Started broad with:
```bash
grep -rl "layer_height" src/libslic3r/
```
This identified 63 files. Narrowed by searching key files:
PrintConfig.hpp for declaration, Slicing.cpp for parameter
conversion, Print.cpp for orchestration, PrintObjectSlice.cpp
for actual slicing. Followed data flow from config → params
→ layer objects → mesh slicer.

### Complete Call Chain

**① Config Declaration**
`src/libslic3r/PrintConfig.hpp` Lines 904, 1599
```cpp
((ConfigOptionFloat, layer_height))
```
layer_height stored as typed float. User's 0.2mm lives here.

**② SlicingParameters**
`src/libslic3r/Slicing.cpp` Lines 81-82
```cpp
params.layer_height = object_config.layer_height.value;
```
Copied into self-contained SlicingParameters struct passed
down the pipeline.

**③ Z List Generation**
`src/libslic3r/Slicing.cpp` Line 742
```cpp
std::vector<coordf_t> generate_object_layers(
    slicing_params, layer_height_profile, precise_z_height)
```
Converts layer_height into flat list of Z coordinates:
[0.2, 0.4, 0.6 ... 116.2]. Called from PrintObjectSlice.cpp
Line 800 and Print.cpp Line 1296.

**④ Layer Object Creation**
`src/libslic3r/PrintObjectSlice.cpp` Lines 31-37
```cpp
coordf_t slice_z = 0.5 * (lo + hi);
Layer *layer = new Layer(id++, print_object,
                         hi - lo,      // height = 0.2mm
                         hi + zmin,    // print_z
                         slice_z);     // cutting Z
```
Each Z interval becomes a Layer object.

**⑤ Layer Object**
`src/libslic3r/Layer.hpp` Lines 132, 251-253
```cpp
coordf_t print_z;  // absolute Z position
coordf_t height;   // layer thickness = 0.2mm
```

**⑥ Mesh Slicing**
`src/libslic3r/PrintObjectSlice.cpp` Lines 1140-1145
```cpp
std::vector<float> slice_zs = zs_from_layers(m_layers);
slice_mesh_ex(its, slice_zs, params, callback);
```
All Z heights passed to slice_mesh_ex simultaneously.

**⑦ Triangle Intersection**
`src/libslic3r/PrintObjectSlice.cpp` Lines 52-63
```cpp
layers = slice_mesh_ex(its, zs, params2, callback);
```
Cuts mesh at every Z — identical operation to our
triangle_plane_intersection() in slicer.py. OrcaSlicer
assembles results into closed ExPolygon contours for
wall path generation.

### Key Files Table

| File | Line | Role |
|---|---|---|
| PrintConfig.hpp | 904, 1599 | layer_height declaration |
| Slicing.cpp | 81-82 | Copy to SlicingParameters |
| Slicing.cpp | 742 | generate_object_layers() |
| PrintObjectSlice.cpp | 800 | Create layer objects |
| PrintObjectSlice.cpp | 31-37 | Assign print_z per layer |
| Layer.hpp | 132, 251 | Layer stores print_z, height |
| PrintObjectSlice.cpp | 1140-1145 | Extract zs, call slicer |
| PrintObjectSlice.cpp | 52-63 | slice_mesh_ex cuts mesh |

### Connection To Our Implementation

Our triangle_plane_intersection() in slicer.py implements
the same geometric operation as slice_mesh_ex — finding
where a horizontal plane cuts each triangle. OrcaSlicer
goes further by assembling segments into ordered closed
polygons, detecting inner vs outer contours, and generating
wall toolpaths. Our implementation stops at raw segment
lengths, sufficient for perimeter estimation.

---

## What I Would Improve

1. **Performance** — current slicer.py is O(n×layers).
   Pre-sorting triangles by Z range would skip most
   triangles per layer. Expected 10-50× speedup.

2. **Proper contour assembly** — currently we sum raw
   segment lengths. Assembling into ordered polygons
   would enable proper perimeter calculation and
   detect holes/islands per layer.

3. **Adaptive layer height** — instead of fixed 0.2mm,
   use finer layers on curved regions and coarser on
   flat regions. OrcaSlicer does this via
   SlicingAdaptive.cpp.

4. **Multi-shell support** — current code assumes 1 wall.
   Extending to N walls means offsetting the contour
   inward by nozzle_diameter × wall_index.

5. **ASCII STL support** — current parser handles binary
   only. A fallback ASCII parser would be more robust.
