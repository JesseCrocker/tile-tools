#!/usr/bin/env python3
import os
import sys


def file_sizes_and_paths(directory):
    file_data = []  # List to store tuples of (file size in KB, file path)
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path):
                size = os.path.getsize(path) / 1024  # Convert bytes to kilobytes
                file_data.append((size, path))
    return file_data


def calculate_stats(file_data):
    if not file_data:
        return (0, ""), (0, ""), 0

    min_file = min(file_data, key=lambda x: x[0])
    max_file = max(file_data, key=lambda x: x[0])
    avg_size = sum(size for size, _ in file_data) / len(file_data)

    return min_file, max_file, avg_size


def main(directory):
    file_data = file_sizes_and_paths(directory)
    min_file, max_file, avg_size = calculate_stats(file_data)

    print(f"Minimum Size: {min_file[0]:.2f} KB, File: {min_file[1]}")
    print(f"Maximum Size: {max_file[0]:.2f} KB, File: {max_file[1]}")
    print(f"Average Size: {avg_size:.2f} KB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python file_size_stats.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)
