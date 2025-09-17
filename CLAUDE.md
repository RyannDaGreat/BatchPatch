# Web Mask Animator

This project contains tools for video frame analysis and spacetime convex hull visualization.

## Files

### `first_try.html` - Spacetime Hull Visualization
Interactive tool that lets users click on video frames to create 3D points (x, y, time) and visualizes the convex hull cross-section at the current time.

**Key Components:**
- **3D Convex Hull Algorithm**: Builds hull faces from spacetime points using facet enumeration
- **MP4 Frame Counter**: Parses MP4 metadata to get exact frame count from `stsz` atom
- **Video Controls**: Frame-accurate scrubbing with proper FPS detection
- **Interactive Canvas**: Click to add points, see hull visualization overlay

**Technical Details:**
- Uses `requestVideoFrameCallback` for perfect video/canvas sync when available
- Calculates actual FPS from `totalFrames / duration` after MP4 parsing
- Hull slicing algorithm finds intersection of 3D hull with time plane
- Points are stored as `{x, y, t}` where `t` is time in seconds

### `experiments/num_frame_detector.html` - Frame Counter Utility
Minimal tool to instantly get frame count from MP4 files using metadata parsing.

**Functions:**
- `find(v, atom, start)` - Locates MP4 atoms by type
- `hasVideo(v, start)` - Checks for video track handler
- `getFrames(v, start)` - Extracts sample count from `stsz` atom
- `parseMP4Frames(file)` - Main parser function

**Usage:**
```javascript
const frameCount = await parseMP4Frames(videoFile);
```

## MP4 Parsing Implementation

Both tools use a compact MP4 parser that:
1. Finds the `moov` atom (movie metadata)
2. Locates video track by checking for `hdlr` atom with `vide` handler type
3. Reads `stsz` (sample size table) atom to get frame count

This approach gives instant, accurate frame counts without playing the video.

## Algorithms

### Convex Hull (3D)
- **Input**: Array of 3D points `{x, y, z}` or `{x, y, t}`
- **Method**: Facet enumeration - tests all possible triangles as potential hull faces
- **Output**: Array of face indices `[i, j, k]` representing hull triangles

### Hull Slicing
- **Input**: 3D hull faces and slice time `T`
- **Method**: Find line segments where each face intersects the plane `z = T`
- **Output**: 2D polygon vertices sorted by angle for rendering

## Performance Notes

- MP4 parsing is O(n) file scan but very fast for typical video sizes
- Hull algorithm is O(n³) but acceptable for interactive point counts (<100)
- Frame-accurate seeking uses minimal memory with DataView parsing
- Canvas rendering optimized with requestAnimationFrame and conditional redraws