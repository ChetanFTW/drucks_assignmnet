# Drucks Technical Assessment
**Candidate:** Chetan 
**Date:** 09 April 2026  
**Language:** Python 3  

---

## Overview

This project implements a minimal 3D printing pipeline analyzer
for the Drucks technical assessment. It operates on a binary STL
file of a shoe model and computes:

- **Task 1:** Volume via signed tetrahedra decomposition
- **Task 2:** Axis-aligned bounding box and layer count
- **Task 3:** Perimeter-based print time estimation
- **Task 4:** OrcaSlicer codebase analysis (documented in [REPORT.md](https://github.com/ChetanFTW/drucks_assignmnet/blob/master/Report.md))

All core geometry is implemented from first principles.
No geometry libraries are used — only Python's built-in
`struct`, `math`, and `os` modules.

---
## Project Structure

```bash
drucks_assessment/
│
├── main.py          → Entry point, runs all tasks
├── stl_parser.py    → Binary STL file parser
├── volume.py        → Signed tetrahedra volume computation
├── bounding_box.py  → Bounding box + layer count
├── slicer.py        → Triangle-plane intersection + print time
├── REPORT.md        → Full write-up with results and analysis
└── README.md        → This file
```
---

## Requirements

- Python 3.10
- No external libraries required
- Standard library only: `struct`, `math`, `os`

---

## Setup

```bash
# Clone the repository
git clone https://github.com/ChetanFTW/drucks_assignmnet.git
cd drucks_assessment


```

---

## Usage

```bash
python main.py
```

This runs all three computational tasks against `DrucksShoe.stl`
and prints a full report to stdout.

---

## Expected Output

```bash
Header: b'Rhinoceros Binary STL ( Aug  5 2025 )\r\n '
Triangle count: 373632
--- Task 1: Volume ---
Volume : 406,550.65 mm³  (406.55 cm³)
--- Task 2: Bounding Box ---
X  →  min:     -6.953 mm    max:   282.610 mm    width : 289.563 mm
Y  →  min:    -62.764 mm    max:    46.267 mm    width : 109.030 mm
Z  →  min:     -6.377 mm    max:   109.869 mm    height: 116.247 mm
--- Task 2: Layer Count ---
Model height : 116.247 mm
Layer height : 0.2 mm
Layer count  : 581 complete layers
--- Sanity Check vs OrcaSlicer ---
OrcaSlicer reported: 289.563 x 109.03 x 116.247 mm
Our computation    : 289.563 x 109.030 x 116.247 mm
--- Task 3: Print Time Estimation ---
Settings: speed=60mm/s  layer=0.2mm  walls=1  infill=0%
Slicing layers............ done (581 layers)
Total layers       : 581
Total path length  : 408,752.6 mm
Total path length  : 408.75 m
Avg perimeter/layer: 703.5 mm
⏱  Estimated print time: 1h 53m 32s
(6813 seconds total)

```
---

## Results vs OrcaSlicer

| Task | Metric | Ours | OrcaSlicer | Difference |
|---|---|---|---|---|
| Task 1 | Volume | 406,550.65 mm³ | 406,547 mm³ | 0.0009% |
| Task 2 | X width | 289.563 mm | 289.563 mm | 0.000% |
| Task 2 | Y width | 109.030 mm | 109.030 mm | 0.000% |
| Task 2 | Z height | 116.247 mm | 116.247 mm | 0.000% |
| Task 2 | Layers | 581 | 581 | 0 |
| Task 3 | Print time | 1h 53m 32s | 1h 57m (outer wall) | ~3% |

---

## How It Works

### STL Parser (`stl_parser.py`)
Reads binary STL format directly using Python's `struct` module.
Each triangle is 50 bytes: 12 bytes normal (ignored) +
3 × 12 bytes vertices + 2 bytes
