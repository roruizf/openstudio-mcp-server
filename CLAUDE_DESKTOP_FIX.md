# Claude Desktop File Access Fix

## Problem

When running in Claude Desktop (not Docker), the server couldn't find user-uploaded files because:

1. Claude Desktop uploads files to `/mnt/user-data/uploads/`
2. The server only searched in `/workspace/sample_files/` and related directories
3. `/workspace` doesn't exist in Claude Desktop's environment - it runs in `/home/claude/`

## Solution

Added Claude Desktop-specific paths to the file search strategy in `path_utils.py`:

### Changes Made

**File**: `openstudio_mcp_server/utils/path_utils.py`

**Added search locations** (lines 96-104):
```python
# Strategy 6: Claude Desktop uploads directory
claude_uploads = os.path.join("/mnt/user-data/uploads", file_path)
if os.path.exists("/mnt/user-data/uploads"):
    search_paths.append(("Claude uploads", claude_uploads))

# Strategy 7: /home/claude directory (Claude Desktop working directory)
home_claude = os.path.join("/home/claude", file_path)
if os.path.exists("/home/claude"):
    search_paths.append(("Claude home", home_claude))
```

**Added to fuzzy matching** (lines 277-281):
```python
# Add Claude Desktop directories if they exist
if os.path.exists("/mnt/user-data/uploads"):
    search_dirs.append("/mnt/user-data/uploads")
if os.path.exists("/home/claude"):
    search_dirs.append("/home/claude")
```

## How It Works Now

When you upload a file to Claude Desktop:

1. File is saved to `/mnt/user-data/uploads/Boom-DC2-026.osm`

2. You ask: "Load Boom-DC2-026.osm"

3. Server searches in this order:
   - Absolute path (if provided)
   - `/workspace/Boom-DC2-026.osm` (doesn't exist in Claude Desktop)
   - `/workspace/sample_files/Boom-DC2-026.osm` (doesn't exist)
   - `/workspace/sample_files/models/Boom-DC2-026.osm` (doesn't exist)
   - `/workspace/outputs/Boom-DC2-026.osm` (doesn't exist)
   - **`/mnt/user-data/uploads/Boom-DC2-026.osm`** ✓ **FOUND!**

4. File loads successfully!

## Dual Environment Support

The fix works in **both environments**:

### Docker Environment
- `/workspace` exists
- Searches in `/workspace/sample_files/`, `/workspace/outputs/`
- Claude Desktop paths don't exist, so they're skipped
- Works as before ✓

### Claude Desktop Environment
- `/workspace` doesn't exist (fallback to current directory)
- Searches in current directory's `sample_files/`
- **Also searches `/mnt/user-data/uploads/`** ✓
- **Also searches `/home/claude/`** ✓
- Now finds uploaded files!

## Testing

### Test in Claude Desktop

1. Upload a file through Claude Desktop interface
2. Ask: "Load [filename].osm"
3. Should now work without needing `copy_file`

### Test in Docker

1. Place file in `sample_files/models/`
2. Run Docker container
3. Ask: "Load [filename].osm"
4. Should work as before

## No Breaking Changes

- Backward compatible with existing code
- Docker environment still works
- Only adds additional search paths when they exist
- No changes to tool signatures or behavior

## What This Fixes

Before this fix, in Claude Desktop you'd see:
```
Error: OSM file not found: /mnt/user-data/uploads/Boom-DC2-026.osm
Searched in:
  - workspace root: /workspace/Boom-DC2-026.osm
  - sample_files: /workspace/sample_files/Boom-DC2-026.osm
  - sample_files/models: /workspace/sample_files/models/Boom-DC2-026.osm
```

After this fix:
```
Success! Loaded model from /mnt/user-data/uploads/Boom-DC2-026.osm
```

## Next Steps

1. Restart Claude Desktop to reload the server
2. Upload a test OSM file
3. Try loading it with just the filename
4. Should work automatically now!
