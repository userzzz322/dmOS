#!/bin/bash

echo "clearing vdisk (preserving files starting with '_')..."

for item in virtualdisk/*; do
    [ -e "$item" ] || continue
    
    filename=$(basename "$item")

    if [[ "$filename" != _* ]]; then
        rm -rf "$item"
        echo "deleted: $filename"
    else
        echo "skipped: $filename"
    fi
done

echo "cleanup complete!"
