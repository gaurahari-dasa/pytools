import os
import sys
from datetime import datetime

PAGE_SIZE = 25


def normalize_excluded_paths(root, excluded_relative_paths):
    """
    Convert relative paths to normalized absolute paths for comparison.
    """
    excluded = set()
    for rel_path in excluded_relative_paths:
        if rel_path:
            full_path = os.path.normpath(os.path.join(root, rel_path))
            excluded.add(full_path)
    return excluded


def collect_files_recursively(root_folder, excluded_paths):
    files = []

    for current_root, dirnames, filenames in os.walk(root_folder):
        current_root_norm = os.path.normpath(current_root)

        # Skip excluded directories
        if any(
            current_root_norm == ex or current_root_norm.startswith(ex + os.sep)
            for ex in excluded_paths
        ):
            dirnames[:] = []  # Do not descend further
            continue

        for filename in filenames:
            full_path = os.path.join(current_root, filename)
            try:
                mtime = os.path.getmtime(full_path)
                files.append((full_path, mtime))
            except OSError:
                # Skip inaccessible files
                continue

    return files


def list_files_by_mtime_recursively(folder_path, excluded_relative_paths):
    excluded_paths = normalize_excluded_paths(
        folder_path, excluded_relative_paths
    )

    entries = collect_files_recursively(folder_path, excluded_paths)

    if not entries:
        print("No files found (after applying exclusions).")
        return

    # Sort by modification time (most recent first)
    entries.sort(key=lambda x: x[1], reverse=True)

    total = len(entries)
    index = 0

    while index < total:
        end = min(index + PAGE_SIZE, total)

        for full_path, mtime in entries[index:end]:
            # ✅ Convert to relative path
            relative_path = os.path.relpath(full_path, folder_path)

            mod_time_str = datetime.fromtimestamp(mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            print(f"{mod_time_str}  {relative_path}")

        index = end

        if index < total:
            choice = input("\nContinue listing? (y/n): ").strip().lower()
            if choice != "y":
                break
        else:
            print("\nEnd of file list.")


def main():
    folder_path = input("Enter the path to the root folder: ").strip()

    if not os.path.isdir(folder_path):
        print("Error: The provided path is not a valid directory.")
        sys.exit(1)

    print(
        "\nEnter folders to exclude (relative paths),"
        "\none per line. Press Enter on an empty line to finish:"
    )

    excluded_relative_paths = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        excluded_relative_paths.append(line)

    list_files_by_mtime_recursively(folder_path, excluded_relative_paths)


if __name__ == "__main__":
    main()