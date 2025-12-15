"""
Path resolution utilities for OpenStudio MCP Server.

This module provides intelligent file path resolution with fuzzy matching,
similar to the EnergyPlus MCP server implementation.
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Tuple
import difflib

logger = logging.getLogger(__name__)


def resolve_path(
    config,
    file_path: str,
    file_types: Optional[List[str]] = None,
    description: str = "file",
    must_exist: bool = True,
    default_dir: Optional[str] = None,
    enable_fuzzy_matching: bool = False,
) -> str:
    """
    Resolve a file path with intelligent fallback searching.

    This function tries multiple strategies to find the file:
    1. If absolute path, validate it directly
    2. Check in workspace root
    3. Check in sample_files directory
    4. Check in models subdirectory
    5. Check in outputs directory (for output files)
    6. If enabled, perform fuzzy matching to find similar files

    Args:
        config: Configuration object with paths
        file_path: Path to resolve (can be absolute, relative, or just filename)
        file_types: Optional list of valid extensions (e.g., ['.osm', '.idf'])
        description: Description for error messages (e.g., "OSM file")
        must_exist: If True, file must exist; if False, creates valid path for new files
        default_dir: Default directory for filename-only paths when must_exist=False
        enable_fuzzy_matching: If True, suggest similar files when exact match fails

    Returns:
        Resolved absolute path

    Raises:
        FileNotFoundError: If file not found and must_exist=True
        ValueError: If file extension doesn't match file_types
    """
    original_path = file_path
    logger.debug(f"Resolving path: {file_path} (must_exist={must_exist})")

    # ---------------------------------------------------------
    # AUTOMATIC DOCKER PATH TRANSLATION (Windows Host Support)
    # ---------------------------------------------------------
    # If we receive a Windows path (e.g., "C:\Users\...") and we are running in Linux (Docker),
    # automatically translate it to the mounted volume path ("/mnt/c/Users/...").

    # 1. Normalize separators (Windows \ to Linux /)
    if "\\" in file_path:
        file_path = file_path.replace("\\", "/")

    # 2. Detect Drive Letter (C:/...) and map to /mnt/c/
    # Note: We assume the standard Docker mount "-v C:\:/mnt/c" is active.
    if file_path.lower().startswith("c:/"):
        # Remove "c:/" (3 chars) and prepend "/mnt/c/"
        original_win_path = file_path
        file_path = f"/mnt/c/{file_path[3:]}"
        logger.info(f"Auto-translated Windows path to Docker path: {original_win_path} -> {file_path}")

    # Validate file extension if specified
    if file_types:
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext and file_ext not in [ft.lower() for ft in file_types]:
            raise ValueError(
                f"{description} must have one of these extensions: {', '.join(file_types)}. "
                f"Got: {file_ext}"
            )

    # Strategy 1: If absolute path, check directly
    if os.path.isabs(file_path):
        if must_exist:
            if os.path.exists(file_path):
                logger.debug(f"Found at absolute path: {file_path}")
                return file_path
        else:
            # For output files, ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            return file_path

    # For relative paths or filenames, try multiple locations
    # IMPORTANT: Search paths are checked in ORDER - user files have PRIORITY
    # Following EnergyPlus MCP pattern: only add directories that exist
    search_paths = []

    # Strategy 2: Claude Desktop uploads (FIRST PRIORITY for user files)
    # Only add if directory exists (user may not have uploaded files yet)
    if os.path.exists("/mnt/user-data/uploads"):
        search_paths.append(("Claude uploads", "/mnt/user-data/uploads"))

    # Strategy 3: /home/claude directory (Claude Desktop working directory)
    if os.path.exists("/home/claude"):
        search_paths.append(("Claude home", "/home/claude"))

    # Strategy 4: Models subdirectory (common location for sample files)
    models_dir = os.path.join(config.paths.sample_files_path, "models")
    if os.path.exists(models_dir):
        search_paths.append(("sample_files/models", models_dir))

    # Strategy 5: Sample files directory
    if os.path.exists(config.paths.sample_files_path):
        search_paths.append(("sample_files", config.paths.sample_files_path))

    # Strategy 6: Relative to output directory
    if hasattr(config.paths, 'output_dir') and os.path.exists(config.paths.output_dir):
        search_paths.append(("outputs", config.paths.output_dir))

    # Strategy 7: Relative to workspace root
    if os.path.exists(config.paths.workspace_root):
        search_paths.append(("workspace root", config.paths.workspace_root))

    # Try each search path (following EnergyPlus MCP pattern)
    for location, search_dir in search_paths:
        candidate_path = os.path.join(search_dir, file_path)
        if os.path.exists(candidate_path):
            logger.debug(f"Found {description} in {location}: {candidate_path}")
            return os.path.abspath(candidate_path)

    # Try as-is (relative to current directory) - EnergyPlus MCP pattern
    if os.path.exists(file_path):
        abs_path = os.path.abspath(file_path)
        logger.debug(f"Found {description} in current directory: {abs_path}")
        return abs_path

    # If must_exist=False, create a valid output path
    if not must_exist:
        # Use default_dir or output_dir
        target_dir = default_dir or getattr(config.paths, 'output_dir', config.paths.workspace_root)
        output_path = os.path.join(target_dir, os.path.basename(file_path))

        # Ensure directory exists
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        except (PermissionError, OSError):
            # If we can't create directory, just return the path
            pass

        logger.debug(f"Created output path: {output_path}")
        return output_path

    # File not found - try fuzzy matching if enabled
    if enable_fuzzy_matching:
        resolver = PathResolver(config)
        suggestions = resolver.suggest_similar_paths(file_path, file_types)

        if suggestions:
            suggestion_list = "\n  - ".join(suggestions[:5])
            raise FileNotFoundError(
                f"{description} not found: {original_path}\n"
                f"Did you mean one of these?\n  - {suggestion_list}"
            )

    # File not found and no suggestions
    searched_locations = "\n  - ".join([f"{loc}: {path}" for loc, path in search_paths])
    raise FileNotFoundError(
        f"{description} not found: {original_path}\n"
        f"Searched in:\n  - {searched_locations}"
    )


def resolve_osm_path(config, osm_path: str) -> str:
    """
    Resolve path to an OpenStudio Model (OSM) file.

    Args:
        config: Configuration object
        osm_path: Path to OSM file

    Returns:
        Resolved absolute path to OSM file

    Raises:
        FileNotFoundError: If file not found
    """
    return resolve_path(
        config,
        osm_path,
        file_types=['.osm'],
        description="OSM file",
        must_exist=True,
        enable_fuzzy_matching=True,
    )


def resolve_idf_path(config, idf_path: str) -> str:
    """
    Resolve path to an EnergyPlus IDF file.

    Args:
        config: Configuration object
        idf_path: Path to IDF file

    Returns:
        Resolved absolute path to IDF file

    Raises:
        FileNotFoundError: If file not found
    """
    return resolve_path(
        config,
        idf_path,
        file_types=['.idf'],
        description="IDF file",
        must_exist=True,
        enable_fuzzy_matching=True,
    )


def resolve_output_path(
    config,
    output_path: str,
    default_dir: Optional[str] = None,
    file_types: Optional[List[str]] = None,
) -> str:
    """
    Resolve path for an output file (can create new files).

    Args:
        config: Configuration object
        output_path: Desired output path
        default_dir: Default directory if only filename provided
        file_types: Optional list of valid extensions

    Returns:
        Resolved absolute path for output file
    """
    return resolve_path(
        config,
        output_path,
        file_types=file_types,
        description="output file",
        must_exist=False,
        default_dir=default_dir,
    )


class PathResolver:
    """
    Helper class for intelligent path resolution and fuzzy matching.
    """

    def __init__(self, config):
        """
        Initialize the PathResolver.

        Args:
            config: Configuration object with paths
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    def suggest_similar_paths(
        self,
        target_path: str,
        extensions: Optional[List[str]] = None,
        similarity_threshold: float = 0.3,
        max_suggestions: int = 10,
    ) -> List[str]:
        """
        Suggest similar file paths when exact match is not found.

        Uses fuzzy string matching to find files with similar names.

        Args:
            target_path: The path that wasn't found
            extensions: Optional list of file extensions to filter by
            similarity_threshold: Minimum similarity ratio (0.0 to 1.0)
            max_suggestions: Maximum number of suggestions to return

        Returns:
            List of suggested file paths, sorted by similarity
        """
        target_name = os.path.basename(target_path).lower()
        suggestions = []

        # Search directories
        search_dirs = [
            self.config.paths.workspace_root,
            self.config.paths.sample_files_path,
            os.path.join(self.config.paths.sample_files_path, "models"),
        ]

        if hasattr(self.config.paths, 'output_dir'):
            search_dirs.append(self.config.paths.output_dir)

        # Add Claude Desktop directories if they exist
        if os.path.exists("/mnt/user-data/uploads"):
            search_dirs.append("/mnt/user-data/uploads")
        if os.path.exists("/home/claude"):
            search_dirs.append("/home/claude")

        # Walk through directories
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue

            try:
                for root, dirs, files in os.walk(search_dir):
                    for filename in files:
                        # Filter by extension if specified
                        if extensions:
                            file_ext = os.path.splitext(filename)[1].lower()
                            if file_ext not in [ext.lower() for ext in extensions]:
                                continue

                        # Calculate similarity
                        similarity = difflib.SequenceMatcher(
                            None,
                            target_name,
                            filename.lower()
                        ).ratio()

                        if similarity >= similarity_threshold:
                            full_path = os.path.join(root, filename)
                            suggestions.append((similarity, full_path))
            except (PermissionError, OSError) as e:
                self.logger.debug(f"Cannot access directory {search_dir}: {e}")
                continue

        # Sort by similarity (descending) and return paths
        suggestions.sort(reverse=True, key=lambda x: x[0])
        return [path for _, path in suggestions[:max_suggestions]]

    def find_files_by_extension(
        self,
        extension: str,
        search_dirs: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Find all files with a specific extension.

        Args:
            extension: File extension to search for (e.g., '.osm')
            search_dirs: Optional list of directories to search

        Returns:
            List of file paths
        """
        if search_dirs is None:
            search_dirs = [
                self.config.paths.workspace_root,
                self.config.paths.sample_files_path,
            ]

        found_files = []
        extension = extension.lower()

        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue

            try:
                for root, dirs, files in os.walk(search_dir):
                    for filename in files:
                        if filename.lower().endswith(extension):
                            found_files.append(os.path.join(root, filename))
            except (PermissionError, OSError) as e:
                self.logger.debug(f"Cannot access directory {search_dir}: {e}")
                continue

        return found_files


def find_model_files_by_name(
    config,
    partial_name: str,
    extensions: Optional[List[str]] = None,
) -> List[str]:
    """
    Find model files matching a partial name (case-insensitive substring match).

    Args:
        config: Configuration object
        partial_name: Partial name to search for (e.g., "office")
        extensions: Optional list of extensions to filter by (e.g., ['.osm'])

    Returns:
        List of matching file paths, sorted by filename length
    """
    resolver = PathResolver(config)

    if extensions is None:
        extensions = ['.osm', '.idf']

    # Find all files with matching extensions
    all_files = []
    for ext in extensions:
        all_files.extend(resolver.find_files_by_extension(ext))

    # Filter by partial name match (case-insensitive)
    partial_lower = partial_name.lower()
    matches = []

    for file_path in all_files:
        filename = os.path.basename(file_path).lower()

        # Check if partial name is in filename
        if partial_lower in filename:
            matches.append(file_path)
            continue

        # Check word-based matching (e.g., "san francisco" matches "USA_CA_San.Francisco")
        words = partial_lower.split()
        if all(word in filename for word in words):
            matches.append(file_path)

    # Sort by filename length (shorter = more relevant)
    matches.sort(key=lambda x: len(os.path.basename(x)))

    return matches
